from code_generation.symbol_table import SymbolTable
from code_generation.vm_writer import VmWriter
from parsing import jack_non_terminals
from parsing import keywords
from parsing import symbols
from parsing.parse_node import NonTerminalParseNode
from parsing.terminals import Identifier
from parsing.terminals import IntegerConstant
from parsing.terminals import StringConstant


class CodeGenerationException(Exception): pass


class CodeGenerator:

    def __init__(self, parse_tree_root, jack_file_path):
        self.output_file_path = self._get_output_file_path(jack_file_path)
        self.parse_tree_root = parse_tree_root
        self.symbol_table = SymbolTable()

        self.class_name = None
        self.vm_writer = None

        self.arbitrary_number = 0  # for uniqueness of labels

    def _get_arbitrary_number(self):
        number = self.arbitrary_number
        self.arbitrary_number += 1
        return number
        
    def _get_output_file_path(self, jack_file_path):
        return '{}.vm'.format(jack_file_path[:-5])

    def generate_code(self):
        with VmWriter(self.output_file_path).open() as self.vm_writer:
            assert isinstance(self.parse_tree_root, jack_non_terminals.Class)
            self._compile_class(self.parse_tree_root)

    def _compile_class(self, class_node):
        # class structure is `class <name> { classVarDec* subroutineDec*}`
        self.class_name = class_node.child_nodes[1].token.value
        class_var_and_subroutine_decs = class_node.child_nodes[3:-1]
        class_var_decs, subroutine_decs = self._split_out_by_type(
            class_var_and_subroutine_decs,
            jack_non_terminals.ClassVarDec,
        )

        for class_var_dec in class_var_decs:
            self._add_var_dec_to_symbol_table(class_var_dec)

        for subroutine_dec in subroutine_decs:
            self._compile_subroutine_dec(subroutine_dec)

    def _split_out_by_type(self, parse_nodes, first_type):
        for i, dec_type in enumerate(parse_nodes):
            if not isinstance(dec_type, first_type):
                break
        return parse_nodes[:i], parse_nodes[i:]

    def _add_var_dec_to_symbol_table(self, var_dec):
        # Has form `kind type name1, name2, ...`
        kind = var_dec.child_nodes[0].token.value
        type_ = var_dec.child_nodes[1].child_nodes[0].token.value

        for child_node in var_dec.child_nodes[2:]:
            if isinstance(child_node, Identifier):
                name = child_node.token.value
                self.symbol_table.add_symbol(name, type_, kind)

    # TODO: a lot of this needs to share state...might be worth making a separate
    # class to handle (return statement should check type of returned value,
    # and would be nice to know function name for error messages). Then each
    # function could have its own symbol table vs clearing part of it.
    def _compile_subroutine_dec(self, subroutine_dec):
        self.symbol_table.reset_subroutine_table()
        child_nodes = subroutine_dec.child_nodes

        subroutine_type, return_type, name, _, param_list, __, body = child_nodes

        if subroutine_type.token.value == 'method':
            # this is actually a placeholder (methods access this through the
            # THIS pointer, not via the arg list), but is needed to make the
            # object's field indices work out in the symbol table (since all
            # callers will be passing a reference to the object as their first
            # argument
            # TODO: any way around this?
            self.symbol_table.add_symbol('this', self.class_name, 'arg')
        
        if param_list:
            self._add_param_list_to_symbol_table(param_list)

        var_decs, statements = self._get_var_decs_and_statements_from_subroutine_body(body)
        for var_dec in var_decs:
            self._add_var_dec_to_symbol_table(var_dec)

        self.vm_writer.write_function(
            name='{}.{}'.format(self.class_name, name.token.value),
            num_locals=self.symbol_table.get_count_of_symbol_kind('var')
        )
        if isinstance(subroutine_type, keywords.Constructor):
            self._compile_constructor_allocation()
        elif isinstance(subroutine_type, keywords.Method):
            self._compile_method_setup()

        self._compile_statements(statements)

    def _add_param_list_to_symbol_table(self, param_list):
        # keep grabbing the first two nodes (a type and variable name) from the
        # list until it's going
        child_nodes = param_list.child_nodes
        while child_nodes:
            type_, name = child_nodes[:2]
            self.symbol_table.add_symbol(
                name.token.value,
                type_.child_nodes[0].token.value,
                kind='arg'
            )

            # strip off the first three elements (includes the separating comma)
            child_nodes = child_nodes[3:]

    def _get_var_decs_and_statements_from_subroutine_body(self, subroutine_body):
        # has the form `{ var_dec* statements }`
        var_decs_and_statements = subroutine_body.child_nodes[1:-1]
            
        # a little confusing because var_decs is multiple VarDec nodes whereas
        # statements is a single node
        var_decs = var_decs_and_statements[:-1]
        statements = var_decs_and_statements[-1]

        return var_decs, statements

    def _compile_constructor_allocation(self):
        """Allocate space for the new object and set the this pointer to
        reference the new space
        """
        num_fields = self.symbol_table.get_count_of_symbol_kind('field')
        self.vm_writer.write_push('constant', num_fields)
        self.vm_writer.write_call(function_name='Memory.alloc', num_args=1)
        self.vm_writer.write_pop('pointer', 0)

    def _compile_method_setup(self):
        """Caller should have pushed the address of the object as the first
        argument, so set the this pointer to that address.
        """
        self.vm_writer.write_push('argument', 0)
        self.vm_writer.write_pop('pointer', 0)

    def _compile_statements(self, statements):
        statements = statements.child_nodes
        if not statements:
            raise CodeGenerationException('No statements in function def!')

        for statement in statements:
            self.vm_writer.write_newline()
            if isinstance(statement, jack_non_terminals.LetStatement):
                self._compile_let_statement(statement)
            elif isinstance(statement, jack_non_terminals.IfStatement):
                self._compile_if_statement(statement)
            elif isinstance(statement, jack_non_terminals.WhileStatement):
                self._compile_while_statement(statement)
            elif isinstance(statement, jack_non_terminals.DoStatement):
                self._compile_do_statement(statement)
            else:
                self._compile_return_statement(statement)

    # TODO: check return type?
    def _compile_return_statement(self, return_statement):
        # Has form `return (expression) ;`
        if isinstance(return_statement.child_nodes[1], jack_non_terminals.Expression):
            self._compile_expression(return_statement.child_nodes[1])
        else:
            self.vm_writer.write_push('constant', 0)

        self.vm_writer.write_return()

    def _compile_let_statement(self, let_statement):
        # has form `let VarNameWithOptionalArrayAccess = Expression;`
        expression_to_assign = let_statement.child_nodes[3]
        self._compile_expression(expression_to_assign)
        destination = let_statement.child_nodes[1]
        self._compile_pop_to_var_name_with_optional_array_access(destination)

    def _compile_if_statement(self, if_statement):
        # has form `if ( expression ) { statements } ?(else { statements })
        if_label_base = self._generate_label_base('if')
        end_if_label = '{}.end_if'.format(if_label_base)
        else_block_label = '{}.else_block'.format(if_label_base)

        condition_expression = if_statement.child_nodes[2]
        if_block = if_statement.child_nodes[5]

        self._compile_expression(condition_expression)
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_ifgoto(else_block_label)
        self._compile_statements(if_block)
        self.vm_writer.write_goto(end_if_label)

        self.vm_writer.write_label(else_block_label)
        if len(if_statement.child_nodes) > 7:  # better way to do this?
            else_block = if_statement.child_nodes[9]
            self._compile_statements(else_block)

        self.vm_writer.write_label(end_if_label)

    def _compile_while_statement(self, while_statement):
        # has form `while ( expression ) { statements }`
        while_label_base = self._generate_label_base('while')
        start_label = '{}.start'.format(while_label_base)
        end_label = '{}.end'.format(while_label_base)

        condition_expression = while_statement.child_nodes[2]
        statements = while_statement.child_nodes[5]

        self.vm_writer.write_label(start_label)
        self._compile_expression(condition_expression)
        self.vm_writer.write_arithmetic('not')
        self.vm_writer.write_ifgoto(end_label)
        self._compile_statements(statements)
        self.vm_writer.write_goto(start_label)
        self.vm_writer.write_label(end_label)

    def _generate_label_base(self, label_type):
        return '{class_name}.{label_type}.{arbitrary_number}'.format(
            class_name=self.class_name,
            label_type=label_type,
            arbitrary_number=self._get_arbitrary_number(),
        )

    def _compile_do_statement(self, do_statement):
        # has the form `do subroutine_call ;`
        subroutine_call = do_statement.child_nodes[1]
        self._compile_subroutine_call(subroutine_call)
        
        # Do statements don't use the return value, so just pop it off
        self.vm_writer.write_pop('temp', 0)
    
    # TODO: clean this up
    def _compile_subroutine_call(self, subroutine_call):
        # has form `([class|var].)subroutine_name(expression_list)`

        # TODO: maybe make this its own method?
        is_method = False

        maybe_obj_and_subroutine_name = subroutine_call.child_nodes[:-3]
        if len(maybe_obj_and_subroutine_name) == 1:
            self.vm_writer.write_push('pointer', 0)  # push pointer to this
            class_name = self.class_name
            subroutine_name = maybe_obj_and_subroutine_name[0].token.value
            is_method = True
        else:
            # If string before the period is in the symbol table, then it's
            # an instance, not a class, so we need to treat this as a method
            # and push a pointer to the instance onto the stack
            class_or_var_name = maybe_obj_and_subroutine_name[0].token.value
            symbol_info = self.symbol_table.lookup_symbol(class_or_var_name)
            if symbol_info:
                class_name = symbol_info.type
                self.vm_writer.write_push_from_symbol(symbol_info)
                is_method = True
            else:
                class_name = maybe_obj_and_subroutine_name[0].token.value

            subroutine_name = maybe_obj_and_subroutine_name[-1].token.value

        expression_list = subroutine_call.child_nodes[-2]
        expressions = [
            node for node in expression_list.child_nodes
            if isinstance(node, jack_non_terminals.Expression)
        ]
        for expression in expressions:
            self._compile_expression(expression)

        self.vm_writer.write_call(
            function_name='{}.{}'.format(class_name, subroutine_name),
            num_args=len(expressions) + (1 if is_method else 0),
        )

    def _compile_expression(self, expression):
        """Writes code that evaluates the expression and leaves the result on
        the stack.
        """
        self._compile_term(expression.child_nodes[0])
        remaining_nodes = expression.child_nodes[1:]
        while remaining_nodes:
            self._compile_term(remaining_nodes[1])
            self._compile_op(remaining_nodes[0])
            remaining_nodes = remaining_nodes[2:]

    def _compile_term(self, term):
        term = term.child_nodes[0]
        if isinstance(term, IntegerConstant):
            self.vm_writer.write_push('constant', term.token.value)
        elif isinstance(term, StringConstant):
            self._compile_string_constant(term)
        elif isinstance(term, jack_non_terminals.KeywordConstant):
            self._compile_keyword_constant(term)
        elif isinstance(term, jack_non_terminals.SubroutineCall):
            self._compile_subroutine_call(term)
        elif isinstance(term, jack_non_terminals.VarNameWithOptionalArrayAccess):
            self._compile_push_var_name_with_optional_array_access(term)
        elif isinstance(term, jack_non_terminals.UnaryOpTerm):
            self._compile_unary_op_term(term)
        else:
            # expression in parens
            self._compile_expression(term.child_nodes[1])

    def _compile_string_constant(self, string_constant):
        # Note that String.appendChar returns a pointer to the string, which we
        # are leaving on the stack at the end of this step
        string = string_constant.token.value
        self.vm_writer.write_push('constant', len(string))
        self.vm_writer.write_call(function_name='String.new', num_args=1)

        for char in string:
            # using the string pointer returned by String.new as our first
            # argument
            self.vm_writer.write_push('constant', ord(char))
            self.vm_writer.write_call(
                function_name='String.appendChar',
                num_args=2,
            )

    def _compile_keyword_constant(self, keyword_constant):
        keyword_constant_type = type(keyword_constant.child_nodes[0])
        if keyword_constant_type == keywords.This:
            # add pointer to current object to stack
            self.vm_writer.write_push('pointer', 0)
        elif keyword_constant_type == keywords.TrueKeyword:
            self.vm_writer.write_push('constant', 1)
            self.vm_writer.write_arithmetic('neg')
        else:   
            # null and False are both 0 
            self.vm_writer.write_push('constant', 0)

    def _compile_push_var_name_with_optional_array_access(self, parse_node):
        # has form VarName ?([Expression])
        var_name = parse_node.child_nodes[0].token.value
        var_symbol_info = self.symbol_table.lookup_symbol(var_name)
        self.vm_writer.write_push_from_symbol(var_symbol_info)

        if len(parse_node.child_nodes) > 1:
            expression = parse_node.child_nodes[2]
            self._compile_expression(expression)
            self.vm_writer.write_arithmetic('add')
            self.vm_writer.write_pop('pointer', 1)
            self.vm_writer.write_push('that', 0)

    def _compile_pop_to_var_name_with_optional_array_access(self, parse_node):
        var_name = parse_node.child_nodes[0].token.value
        var_symbol_info = self.symbol_table.lookup_symbol(var_name)

        if len(parse_node.child_nodes) > 1:
            expression = parse_node.child_nodes[2]
            self.vm_writer.write_push_from_symbol(var_symbol_info)
            self._compile_expression(expression)
            self.vm_writer.write_arithmetic('add')
            self.vm_writer.write_pop('pointer', 1)
            self.vm_writer.write_pop('that', 0)
        else:
            self.vm_writer.write_pop_to_symbol(var_symbol_info)

    op_to_vm_command = {
        symbols.Plus: 'add',
        symbols.Minus: 'sub',
        symbols.Ampersand: 'and',
        symbols.Pipe: 'or',
        symbols.OpenAngleBracket: 'lt',
        symbols.CloseAngleBracket: 'gt',
        symbols.Equals: 'eq'
    }
    op_to_function_call = {
        symbols.Asterix: 'Math.multiply',
        symbols.Slash: 'Math.divide',
    }

    def _compile_op(self, op):
        op_type = type(op.child_nodes[0])
        if op_type in self.op_to_vm_command:
            self.vm_writer.write_arithmetic(self.op_to_vm_command[op_type])
        else:
            self.vm_writer.write_call(
                function_name=self.op_to_function_call[op_type],
                num_args=2,
            )

    unary_op_to_vm_command = {
        symbols.Minus: 'neg',
        symbols.Tilde: 'not',
    }

    def _compile_unary_op_term(self, unary_op_term):
        unary_op = unary_op_term.child_nodes[0]
        unary_op_type = type(unary_op.child_nodes[0])
        term = unary_op_term.child_nodes[1]

        self._compile_term(term)
        self.vm_writer.write_arithmetic(
            self.unary_op_to_vm_command[unary_op_type],
        )
