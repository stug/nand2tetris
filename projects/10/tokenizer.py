import string
from collections import namedtuple


SYMBOLS = {
    '{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|',
    '<', '>', '=', '~',
}
KEYWORDS = {
    'class', 'constructor', 'function', 'method', 'field', 'static', 'var',
    'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let',
    'do', 'if', 'else', 'while', 'return',
}
ALLOWED_IDENTIFIER_CHARS = set(string.ascii_letters + string.digits + '_')
SYMBOLS_AND_WHITESPACE = SYMBOLS.union(set(string.whitespace))
MAX_INTEGER = 2**15 - 1


Token = namedtuple('Token', ['token_type', 'element'])


class TokenizerException(Exception): pass


class Tokenizer:

    def __init__(self, filepath):
        self.filepath = filepath
        self.jack_code = None
        self.tokens = []

    def yield_tokens(self):
        with open(self.filepath, 'r') as jack_file:
            self.jack_code = jack_file.read()
            yield from self._yield_tokens()

    # TODO: it would be nice to make this track line numbers
    def _yield_tokens(self):
        while not self.jack_code.isspace():
            self.jack_code = self.jack_code.lstrip()

            if self.jack_code.startswith('//'):
                self._cut_till_separator('\n')

            elif self.jack_code.startswith('/*'):
                self._cut_till_separator('*/')

            elif self.jack_code.startswith('"'):
                yield self._extract_string_constant()

            elif self.jack_code[0] in SYMBOLS:
                yield self._extract_symbol()

            # TODO: don't love this...maybe these methods should return the 
            # token instead so that this method can realize that it never got
            # a token and raise?
            else:
                yield self._try_extract_integer_keyword_or_identifier()

    def _cut_till_separator(self, separator):
        self.jack_code = self.jack_code.partition(separator)[2]

    def _separate_on_symbol_or_whitespace(self):
        for index, char in enumerate(self.jack_code):
            if char in SYMBOLS_AND_WHITESPACE:
                potential_token = self.jack_code[:index]
                self.jack_code = self.jack_code[index:]
                return potential_token

    def _extract_string_constant(self):
        string_constant, _, self.jack_code = self.jack_code[1:].partition('"')
        
        if not self.jack_code[0] in SYMBOLS_AND_WHITESPACE:
            raise TokenizerException(
                'Expected whitespace or symbobl after closing double quote '
                'for string {}'.format(string_constant),
            )

        return Token('stringConstant', string_constant)

    def _extract_symbol(self):
        symbol = self.jack_code[0]
        self.jack_code = self.jack_code[1:]
        return Token('symbol', symbol)

    def _try_extract_integer_keyword_or_identifier(self):
        potential_token = self._separate_on_symbol_or_whitespace()

        if potential_token[0].isdigit():
            return self._parse_integer_constant(potential_token)
        elif potential_token in KEYWORDS:
            return Token('keyword', potential_token)
        elif self._is_valid_identifier(potential_token):
            return Token('identifier', potential_token)
        else:
            raise TokenizerException(
                "Couldn't figure out what to do with string {}".format(
                    potential_token,
                ),
            )

    def _parse_integer_constant(self, integer_constant):
        try:
            integer_constant = int(integer_constant)
        except ValueError:
            raise TokenizerException(
                'Failed to extract integer from {}'.format(integer_constant),
            )
        
        if integer_constant > MAX_INTEGER:
            raise TokenizerException(
                'Integers must be between 0 and {} (got {})'.format(
                    MAX_INTEGER,
                    integer_constant,
                ),
            )

        return Token('integerConstant', integer_constant)

    def _is_valid_identifier(self, maybe_identifier):
        return (
            not maybe_identifier[0] in string.digits
            and set(maybe_identifier).issubset(ALLOWED_IDENTIFIER_CHARS)
        )
