from parsing.terminals import Keyword


class Boolean(Keyword):
        expected_keyword = 'boolean'
    
    
class Char(Keyword):
        expected_keyword = 'char'
    
    
class ClassKeyword(Keyword):  # to distinguish from the Class ParseNode
        expected_keyword = 'class'
    
    
class Constructor(Keyword):
        expected_keyword = 'constructor'
    
    
class Do(Keyword):
        expected_keyword = 'do'
    
    
class Else(Keyword):
        expected_keyword = 'else'
    
    
class FalseKeyword(Keyword):
        expected_keyword = 'false'
    
    
class Field(Keyword):
        expected_keyword = 'field'
    
    
class Function(Keyword):
        expected_keyword = 'function'
    
    
class If(Keyword):
        expected_keyword = 'if'
    
    
class Int(Keyword):
        expected_keyword = 'int'
    
    
class Let(Keyword):
        expected_keyword = 'let'
    
    
class Method(Keyword):
        expected_keyword = 'method'


class Null(Keyword):
        expected_keyword = 'null'
    
    
class Return(Keyword):
        expected_keyword = 'return'
    
    
class Static(Keyword):
        expected_keyword = 'static'
    
    
class This(Keyword):
        expected_keyword = 'this'
    
    
class TrueKeyword(Keyword):
        expected_keyword = 'true'
    
    
class Var(Keyword):
        expected_keyword = 'var'
    
    
class Void(Keyword):
        expected_keyword = 'void'
    
    
class While(Keyword):
        expected_keyword = 'while'
