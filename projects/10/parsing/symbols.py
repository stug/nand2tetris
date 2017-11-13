from parsing.terminals import Symbol


class OpenCurlyBrace(Symbol):
    expected_symbol = '{'


class CloseCurlyBrace(Symbol):
    expected_symbol = '}'


class OpenParen(Symbol):
    expected_symbol = '('


class CloseParen(Symbol):
    expected_symbol = ')'


class OpenSquareBracket(Symbol):
    expected_symbol = '['


class CloseSquareBracket(Symbol):
    expected_symbol = ']'


class Period(Symbol):
    expected_symbol = '.'


class Comma(Symbol):
    expected_symbol = ','


class Semicolon(Symbol):
    expected_symbol = ';'


class Plus(Symbol):
    expected_symbol = '+'


class Minus(Symbol):
    expected_symbol = '-'


class Asterix(Symbol):
    expected_symbol = '*'


class Slash(Symbol):
    expected_symbol = '/'


class Ampersand(Symbol):
    expected_symbol = '&'


class Pipe(Symbol):
    expected_symbol = '|'


class OpenAngleBracket(Symbol):
    expected_symbol = '<'


class CloseAngleBracket(Symbol):
    expected_symbol = '>'


class Equals(Symbol):
    expected_symbol = '='


class Tilde(Symbol):
    expected_symbol = '~'
