from parsing.parse_node import ParseException
from parsing.parse_node import TerminalParseNode
from tokenizer import Token
from tokenizer import KEYWORDS
from tokenizer import SYMBOLS


class Keyword(TerminalParseNode):

    grammar_element_name = 'keyword'
    expected_keyword = None

    def parse_token(self, token):
        if token != Token('keyword', self.expected_keyword):
            raise ParseException('Expected keyword {}, got {}'.format(
                self.expected_keyword,
                token
            ))
        self.token = token
        return self


class Identifier(TerminalParseNode):

    grammar_element_name = 'identifier'

    def parse_token(self, token):
        if token.type != 'identifier':
            raise ParseException('Expected an identifier, got {}'.format(token))

        self.token = token
        return self


class Symbol(TerminalParseNode):

    grammar_element_name = 'symbol'
    expected_symbol = None

    def parse_token(self, token):
        if token != Token('symbol', self.expected_symbol):
            raise ParseException('Expected symbol {}, got {}'.format(
                self.expected_symbol,
                token
            ))
        self.token = token
        return self


class IntegerConstant(TerminalParseNode):

    grammar_element_name = 'integerConstant'

    def parse_token(self, token):
        if token.type != 'integerConstant':
            raise ParseException('Expected an integer, got {}'.format(token))

        self.token = token
        return self


class StringConstant(TerminalParseNode):

    grammar_element_name = 'stringConstant'

    def parse_token(self, token):
        if token.type != 'stringConstant':
            raise ParseException('Expected a string, got {}'.format(token))

        self.token = token
        return self
