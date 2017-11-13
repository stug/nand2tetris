from parsing import keywords
from parsing import symbols
from parsing.parse_node import any_of
from parsing.parse_node import optional
from parsing.parse_node import zero_or_more
from parsing.parse_node import NonTerminalParseNode
from parsing.terminals import Identifier
from parsing.terminals import IntegerConstant
from parsing.terminals import StringConstant


# Because Statements and Term are both involved in recursive definitions, they
# need to be defined without referring to the other definitions first so that
# other definitions can refer to them.  Only then can we add the subtypes
# (otherwise the python interpreter gets confused)
class Statements(NonTerminalParseNode):
    grammar_element_name = 'statements'
    statement_subtypes = []
    child_node_types = [
        zero_or_more([
            any_of(statement_subtypes),
        ]),
    ]


class Term(NonTerminalParseNode):
    grammar_element_name = 'term'
    term_subtypes = []
    child_node_types = [
        any_of(term_subtypes),
    ]


class Op(NonTerminalParseNode):
    child_node_types = [
        any_of([
            symbols.Plus, symbols.Minus, symbols.Asterix, symbols.Slash,
            symbols.Ampersand, symbols.Pipe, symbols.OpenAngleBracket,
            symbols.CloseAngleBracket, symbols.Equals,
        ])
    ]


class Expression(NonTerminalParseNode):
    grammar_element_name = 'expression'
    child_node_types = [
        Term,
        zero_or_more([
            Op,
            Term,
        ]),
    ]


class Type(NonTerminalParseNode):
    child_node_types = [
        any_of([
            keywords.Int, keywords.Char, keywords.Boolean,
            Identifier,  # className
        ])
    ]


class ClassVarDec(NonTerminalParseNode):
    grammar_element_name = 'classVarDec'
    child_node_types = [
        any_of([
            keywords.Static, keywords.Field,
        ]),
        Type,
        Identifier,  # varName
        zero_or_more([
            symbols.Comma,
            Identifier,  # varName
        ]),
        symbols.Semicolon,
    ]


class ParameterList(NonTerminalParseNode):
    grammar_element_name = 'parameterList'
    child_node_types = [
        optional([
            Type,
            Identifier,  # varName
            zero_or_more([
                symbols.Comma,
                Type,
                Identifier,  # varName
            ]),
        ]),
    ]


class VarDec(NonTerminalParseNode):
    grammar_element_name = 'varDec'
    child_node_types = [
        keywords.Var,
        Type,
        Identifier,  # varName
        zero_or_more([
            symbols.Comma,
            Identifier,  # varName
        ]),
        symbols.Semicolon,
    ]


class KeywordConstant(NonTerminalParseNode):
    child_node_types = [
        any_of([
            keywords.TrueKeyword,
            keywords.FalseKeyword,
            keywords.Null,
            keywords.This,
        ])
    ]


class VarNameWithOptionalArrayAccess(NonTerminalParseNode):
    child_node_types = [
        Identifier,
        optional([
            symbols.OpenSquareBracket,
            Expression,
            symbols.CloseSquareBracket,
        ]),
    ]


class UnaryOp(NonTerminalParseNode):
    child_node_types = [
        any_of([
            symbols.Minus,
            symbols.Tilde,
        ])
    ]


class UnaryOpTerm(NonTerminalParseNode):
    child_node_types = [
        UnaryOp,
        Term,
    ]


# not the best that this is needed, but would otherwise need to create an easy
# way to make unnamed non-terminals, which feels maybe to complicated
class ExpressionInParens(NonTerminalParseNode):
    child_node_types = [
        symbols.OpenParen,
        Expression,
        symbols.CloseParen,
    ]


class ExpressionList(NonTerminalParseNode):
    grammar_element_name = 'expressionList'
    child_node_types = [
        optional([
            Expression,
            zero_or_more([
                symbols.Comma,
                Expression,
            ]),
        ]),
    ]



class SubroutineCall(NonTerminalParseNode):
    child_node_types = [
        Identifier,  # either a subroutineName or a varName/className
        optional([
            symbols.Period,
            Identifier,  # subroutineName
        ]),
        symbols.OpenParen,
        ExpressionList,
        symbols.CloseParen,
    ]


# Add the list of term types
Term.term_subtypes.extend([
    IntegerConstant,
    StringConstant,
    KeywordConstant,

    # unfortunately SubroutineCall has to go before
    # VarNameWithOptionalArrayAccess since they both think they can parse
    # `thing.method(argument)`.  If VarNameWithOptionalArrayAccess goes first,
    # it will succeed, but the next token will be a period, which will likely
    # confuse whatever goes next.  Ideally the failure behavior would cause
    # us to return to this list of subtypes and try the next one so that the
    # order doesn't matter.  As it is, the Term node thinks it has succeeded
    # so it won't get control again to retry.

    # Another possible option would be preprocess the tree so that it is aware
    # of this ambiguity and knows that it needs to do some sort of check.
    SubroutineCall,
    VarNameWithOptionalArrayAccess,
    UnaryOpTerm,
    ExpressionInParens,
])


class LetStatement(NonTerminalParseNode):
    grammar_element_name = 'letStatement'
    child_node_types = [
        keywords.Let,
        VarNameWithOptionalArrayAccess,
        symbols.Equals,
        Expression,
        symbols.Semicolon,
    ]


class IfStatement(NonTerminalParseNode):
    grammar_element_name = 'ifStatement'
    child_node_types = [
        keywords.If,
        symbols.OpenParen,
        Expression,
        symbols.CloseParen,
        symbols.OpenCurlyBrace,
        Statements,
        symbols.CloseCurlyBrace,
        optional([
            keywords.Else,
            symbols.OpenCurlyBrace,
            Statements,
            symbols.CloseCurlyBrace,
        ]),
    ]


class WhileStatement(NonTerminalParseNode):
    grammar_element_name = 'whileStatement'
    child_node_types = [
        keywords.While,
        symbols.OpenParen,
        Expression,
        symbols.CloseParen,
        symbols.OpenCurlyBrace,
        Statements,
        symbols.CloseCurlyBrace,
    ]


class DoStatement(NonTerminalParseNode):
    grammar_element_name = 'doStatement'
    child_node_types = [
        keywords.Do,
        SubroutineCall,
        symbols.Semicolon,
    ]


class ReturnStatement(NonTerminalParseNode):
    grammar_element_name = 'returnStatement'
    child_node_types = [
        keywords.Return,
        optional([
            Expression,
        ]),
        symbols.Semicolon,
    ]


# Add the list of statement types
Statements.statement_subtypes.extend([
    LetStatement, IfStatement, WhileStatement, DoStatement, ReturnStatement,
])
    

class SubroutineBody(NonTerminalParseNode):
    grammar_element_name = 'subroutineBody'
    child_node_types = [
        symbols.OpenCurlyBrace,
        zero_or_more([
            VarDec,
        ]),
        Statements,
        symbols.CloseCurlyBrace,
    ]


class SubroutineDec(NonTerminalParseNode):
    grammar_element_name = 'subroutineDec'
    child_node_types = [
        any_of([
            keywords.Constructor, keywords.Function, keywords.Method,
        ]),
        any_of([
            keywords.Void, Type,
        ]),
        Identifier,  # subroutineName
        symbols.OpenParen,
        ParameterList,
        symbols.CloseParen,
        SubroutineBody,
    ]


class Class(NonTerminalParseNode):
    grammar_element_name = 'class'
    child_node_types = [
        keywords.ClassKeyword,
        Identifier,  # className
        symbols.OpenCurlyBrace,
        zero_or_more([
            ClassVarDec,
        ]),
        zero_or_more([
            SubroutineDec,
        ]),
        symbols.CloseCurlyBrace,
    ]
