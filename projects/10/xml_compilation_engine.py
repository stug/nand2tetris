from functools import wraps
from xml.etree import ElementTree

from tokenizer import Token
from tokenizer import KEYWORDS
from xml_util import format_xml
from xml_util import save_xml_to_file


TWO_NUMBER_OPERATORS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
UNARY_OPERATORS = {'-', '~'}
KEYWORD_CONSTANTS = {'true', 'false', 'null', 'this'}


class XmlCompilationException(Exception):
    def __init__(self, message, jack_file_path):
        self.message = message
        self.jack_file_path = jack_file_path


def _print_compilaton_exception_info(compilation_exception, current_non_terminal, current_element):
    print(
        'Exception while compiling {} in {}: {}'.format(
            current_non_terminal,
            compilation_exception.jack_file_path,
            compilation_exception.message,
        )
    )
    print('Current element XML:\n{}'.format(format_xml(current_element)))


def handle_compilation_exceptions(non_terminal_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):  # assumes this is a bound method
            parent_element = kwargs.pop('parent_element', None)
            if not parent_element:
                args = [arg for arg in args]
                parent_element = args.pop(-1)

            current_element = ElementTree.SubElement(parent_element, non_terminal_name)
            try:
                func(self, current_element, *args, **kwargs)
            except XmlCompilationException as e:
                _print_compilation_exception_info(
                    compilation_exception=e,
                    current_non_terminal=non_terminal_name,
                    current_element=current_element,
                )
                raise  # leads to exceptions getting raised many times...
        return wrapper
    return decorator


# TODO: this works but is kind of ugly.  Thoughts for improvements:
#   - This currently does a lot of passing a parent element into a sub element,
#       which is gross.  One way to mitigate this would be to stop using
#       ElementTree and have each compilation method print its start and end
#       tags directly (with helper methods that know the indentation level).
#   - Currently can't backtrack, which leads to situations where we have to
#       check what the current tag is to determine which method to call --
#       ideally we'd be able to try each of the methods that we might want to
#       call, and then backtrack if they fail.  This would require rethinking
#       the tokens generator (maybe wrap it with something that keeps track of
#       the recent tokens).  In this, each element method would have to also
#       keep track of the position in the token stream when it starts so that
#       it can fall back.
#   - To be really ambitious, it probably wouldn't be too hard to make each
#       xml element correspond to a class which knows what its sub elements are.
#       Then we could pass the tokens (probably would need a proxy object) to
#       each of them, asking them to compilate.  This would return an XML
#       element that could be added as a subelement of the current class's
#       element.  This would use the backtracking described above.  It would
#       also need to be able to specify when something is optional, or when
#       there is a choice among several next element types
class XmlCompilationEngine:

    def __init__(self, tokens, jack_file_path):
        self.tokens = tokens
        self.jack_file_path = jack_file_path
        self.output_file_path = self._get_output_file_path(self.jack_file_path)
        self.current_token = None

    def _get_output_file_path(self, jack_file_path):
        return '{}_parse_tree.xml'.format(
            jack_file_path[:-5],  # remove .jack
        )

    def _advance_token(self):
        self.current_token = self.tokens.__next__()

    def generate_code(self):
        self._advance_token()  # get first token
        element_tree = self._compile_class()
        save_xml_to_file(element_tree, self.output_file_path)
        
    def _compile_class(self):
        # TODO: would be nice if tokens contained their line number for better
        # error messages
        root = ElementTree.Element('class')
        try:
            self._compile_keyword('class', root)
            self._compile_identifier(root)
            self._compile_symbol('{', root)

            while (
                self.current_token.type == 'keyword'
                and self.current_token.value in ('static', 'field')
            ):
                self._compile_classVarDec(root)
            while (
                self.current_token.type == 'keyword'
                and self.current_token.value in (
                    'constructor', 'function', 'method'
                )
            ):
                self._compile_subroutineDec(root)

            self._compile_final_closing_curly_brace(root)
            return root
        except XmlCompilationException as e:
            _print_parse_exception_info(
                parse_exception=e,
                current_non_terminal='class',
                current_element=root,
            )
            raise

    def _compile_possible_keywords(self, allowed_keywords, parent_element):
        """Check that next token is one of several possible keywords"""
        if not (
            self.current_token.type == 'keyword'
            and self.current_token.value in allowed_keywords
        ):
            raise XmlCompilationException(
                message='Expected keyword in {}, got {}'.format(
                    allowed_keywords,
                    self.current_token,
                ),
                jack_file_path=self.jack_file_path,
            )

        element = ElementTree.SubElement(
            parent_element,
            self.current_token.type,
        )
        element.text = self.current_token.value
        self._advance_token()

    def _compile_keyword(self, keyword, parent_element):
        self._compile_possible_keywords([keyword], parent_element)

    def _compile_identifier(self, parent_element):
        if not self.current_token.type == 'identifier':
            raise XmlCompilationException(
                message='Expected identifier, got {}'.format(self.current_token),
                jack_file_path=self.jack_file_path,
            )
    
        element = ElementTree.SubElement(
            parent_element,
            self.current_token.type
        )
        element.text = self.current_token.value
        self._advance_token()

    def _compile_possible_symbols(self, allowed_symbols, parent_element):
        if not (
            self.current_token.type == 'symbol'
            and self.current_token.value in allowed_symbols
        ):
            raise XmlCompilationException(
                message='Expected symbol in {}, got {}'.format(
                    allowed_symbols,
                    self.current_token,
                ),
                jack_file_path=self.jack_file_path,
            )

        element = ElementTree.SubElement(
            parent_element,
            self.current_token.type
        )
        element.text = self.current_token.value
        self._advance_token()

    def _compile_symbol(self, symbol, parent_element):
        self._compile_possible_symbols([symbol], parent_element)

    # TODO: better way to do this?  Feels weird to expect the exception
    def _compile_final_closing_curly_brace(self, parent_element):
        try:
            self._compile_symbol('}', parent_element)
        except StopIteration:
            return
        
        raise XmlCompilationException(
            message='Found tokens after what should be final }:\n{}'.format(
                list(self.tokens),
            ),
            jack_file_path=self.jack_file_path,
        )

    def _compile_integer_constant(self, parent_element):
        if not self.current_token.type == 'integerConstant':
            raise XmlCompilationException(
                message='Expected an integer, got {}'.format(
                    self.current_token,
                ),
                jack_file_path=self.jack_file_path,
            )
        element = ElementTree.SubElement(
            parent_element,
            self.current_token.type,
        )
        element.text = self.current_token.value
        self._advance_token()

    def _compile_string_constant(self, parent_element):
        if not self.current_token.type == 'stringConstant':
            raise XmlCompilationException(
                message='Expected a string, got {}'.format(
                    self.current_token,
                ),
                jack_file_path=self.jack_file_path,
            )

        element = ElementTree.SubElement(
            parent_element,
            self.current_token.type,
        )
        element.text = self.current_token.value
        self._advance_token()

    @handle_compilation_exceptions(non_terminal_name='classVarDec')
    def _compile_classVarDec(self, classVarDec_element):
        self._compile_possible_keywords(['static', 'field'], classVarDec_element)
        self._compile_type_varName(classVarDec_element)
        while self.current_token == Token('symbol', ','):
            self._compile_symbol(',', classVarDec_element)
            self._compile_identifier(classVarDec_element)  # varName
        self._compile_symbol(';', classVarDec_element)

    def _compile_type_varName(self, parent_element):
        self._compile_type(parent_element)
        self._compile_identifier(parent_element)  # varName

    def _compile_type(self, parent_element):
        try:
            self._compile_possible_keywords(
                ['int', 'char', 'boolean'],
                parent_element
            )
            return
        except XmlCompilationException:
            pass

        self._compile_identifier(parent_element)

    @handle_compilation_exceptions(non_terminal_name='subroutineDec')
    def _compile_subroutineDec(self, subroutineDec_element):
        self._compile_possible_keywords(
            ['constructor', 'function', 'method'],
            subroutineDec_element,
        )

        try:
            self._compile_keyword('void', subroutineDec_element)
        except XmlCompilationException:
            self._compile_type(subroutineDec_element)

        self._compile_identifier(subroutineDec_element)  # subroutineName
        self._compile_symbol('(', subroutineDec_element)
        self._compile_parameterList(subroutineDec_element)
        self._compile_symbol(')', subroutineDec_element)
        self._compile_subroutineBody(subroutineDec_element)

    @handle_compilation_exceptions(non_terminal_name='parameterList')
    def _compile_parameterList(self, parameterList_element):
        if self.current_token == Token('symbol', ')'):
            return
        self._compile_type_varName(parameterList_element)
        while self.current_token == Token('symbol', ','):
            self._compile_symbol(',', parameterList_element)
            self._compile_type_varName(parameterList_element)

    @handle_compilation_exceptions(non_terminal_name='subroutineBody')
    def _compile_subroutineBody(self, subroutineBody_element):
        self._compile_symbol('{', subroutineBody_element)

        while self.current_token == Token('keyword', 'var'):
            self._compile_varDec(subroutineBody_element)

        self._compile_statements(subroutineBody_element)
        self._compile_symbol('}', subroutineBody_element)

    @handle_compilation_exceptions(non_terminal_name='varDec')
    def _compile_varDec(self, varDec_element):
        self._compile_keyword('var', varDec_element)
        self._compile_type_varName(varDec_element)
        while self.current_token == Token('symbol', ','):
            self._compile_symbol(',', varDec_element)
            self._compile_identifier(varDec_element)  # varName
        self._compile_symbol(';', varDec_element)

    @handle_compilation_exceptions(non_terminal_name='statements')
    def _compile_statements(self, statements_element):
        while (
            self.current_token.type == 'keyword'
            and self.current_token.value in (
                'let', 'if', 'while', 'do', 'return'
            )
        ):
            if self.current_token == Token('keyword', 'let'):
                self._compile_letStatement(statements_element)
            elif self.current_token == Token('keyword', 'if'):
                self._compile_ifStatement(statements_element)
            elif self.current_token == Token('keyword', 'while'):
                self._compile_whileStatement(statements_element)
            elif self.current_token == Token('keyword', 'do'):
                self._compile_doStatement(statements_element)
            else:
                self._compile_returnStatement(statements_element)

    @handle_compilation_exceptions(non_terminal_name='letStatement')
    def _compile_letStatement(self, letStatement_element):
        self._compile_keyword('let', letStatement_element)
        self._compile_identifier(letStatement_element)

        if self.current_token == Token('symbol', '['):
            self._compile_symbol('[', letStatement_element)
            self._compile_expression(letStatement_element)
            self._compile_symbol(']', letStatement_element)

        self._compile_symbol('=', letStatement_element)
        self._compile_expression(letStatement_element)
        self._compile_symbol(';', letStatement_element)

    @handle_compilation_exceptions(non_terminal_name='ifStatement')
    def _compile_ifStatement(self, ifStatement_element):
        self._compile_keyword('if', ifStatement_element)
        self._compile_symbol('(', ifStatement_element)
        self._compile_expression(ifStatement_element)
        self._compile_symbol(')', ifStatement_element)
        self._compile_symbol('{', ifStatement_element)
        self._compile_statements(ifStatement_element)
        self._compile_symbol('}', ifStatement_element)

        if self.current_token == Token('keyword', 'else'):
            self._compile_keyword('else', ifStatement_element)
            self._compile_symbol('{', ifStatement_element)
            self._compile_statements(ifStatement_element)
            self._compile_symbol('}', ifStatement_element)

    @handle_compilation_exceptions(non_terminal_name='whileStatement')
    def _compile_whileStatement(self, whileStatement_element):
        self._compile_keyword('while', whileStatement_element)
        self._compile_symbol('(', whileStatement_element)
        self._compile_expression(whileStatement_element)
        self._compile_symbol(')', whileStatement_element)
        self._compile_symbol('{', whileStatement_element)
        self._compile_statements(whileStatement_element)
        self._compile_symbol('}', whileStatement_element)

    @handle_compilation_exceptions(non_terminal_name='doStatement')
    def _compile_doStatement(self, doStatement_element):
        self._compile_keyword('do', doStatement_element)

        # this could either be the subroutineName or a varName or className
        self._compile_identifier(doStatement_element)
        self._compile_subroutineCall_after_first_identifier(doStatement_element)
        self._compile_symbol(';', doStatement_element)

    def _compile_subroutineCall_after_first_identifier(self, parent_element):
        # TODO: ughhh this is ugly, but necessary for handling term elements,
        # since it's hard to distinguish between variable names and subroutine
        # calls.  Ideally we'd backtrack to handle this, but that's not trivial
        # given the current implementation
        if self.current_token == Token('symbol', '.'):
            self._compile_symbol('.', parent_element)
            self._compile_identifier(parent_element)  # subroutineName

        self._compile_symbol('(', parent_element)
        self._compile_expressionList(parent_element)
        self._compile_symbol(')', parent_element)

    @handle_compilation_exceptions(non_terminal_name='returnStatement')
    def _compile_returnStatement(self, returnStatement_element):
        self._compile_keyword('return', returnStatement_element)
        if self.current_token != Token('symbol', ';'):
            self._compile_expression(returnStatement_element)

        self._compile_symbol(';', returnStatement_element)

    @handle_compilation_exceptions(non_terminal_name='expression')
    def _compile_expression(self, expression_element):
        self._compile_term(expression_element)
        while (
            self.current_token.type == 'symbol'
            and self.current_token.value in TWO_NUMBER_OPERATORS
        ):
            self._compile_possible_symbols(TWO_NUMBER_OPERATORS, expression_element)
            self._compile_term(expression_element)

    @handle_compilation_exceptions(non_terminal_name='term')
    def _compile_term(self, term_element):
        if self.current_token.type == 'integerConstant':
            self._compile_integer_constant(term_element)
        elif self.current_token.type == 'stringConstant':
            self._compile_string_constant(term_element)
        elif self.current_token == Token('symbol', '('):
            self._compile_symbol('(', term_element)
            self._compile_expression(term_element)
            self._compile_symbol(')', term_element)
        elif (
            self.current_token.type == 'keyword'
            and self.current_token.value in KEYWORD_CONSTANTS
        ):
            # keywordConstant
            self._compile_possible_keywords(KEYWORD_CONSTANTS, term_element)
        elif (
            self.current_token.type == 'symbol'
            and self.current_token.value in UNARY_OPERATORS
        ):
            self._compile_possible_symbols(UNARY_OPERATORS, term_element)
            self._compile_term(term_element)
        elif self.current_token.type == 'identifier':
            self._compile_varName_or_subroutineCall(term_element)
        else:
            raise ParseError(
                message='Expected an int, string, (, -, ~, keywordConstant, '
                    'or identifier',
                jack_file_path = self.jack_file_path,
            )

    def _compile_varName_or_subroutineCall(self, parent_element):
        self._compile_identifier(parent_element)
        if self.current_token in (Token('symbol', '('), Token('symbol', '.')):
            self._compile_subroutineCall_after_first_identifier(parent_element)
        elif self.current_token == Token('symbol', '['):
            # array access
            self._compile_symbol('[', parent_element)
            self._compile_expression(parent_element)
            self._compile_symbol(']', parent_element)

    @handle_compilation_exceptions(non_terminal_name='expressionList')
    def _compile_expressionList(self, expressionList_element):
        if self.current_token == Token('symbol', ')'):
            return

        self._compile_expression(expressionList_element)
        while self.current_token == Token('symbol', ','):
            self._compile_symbol(',', expressionList_element)
            self._compile_expression(expressionList_element)
