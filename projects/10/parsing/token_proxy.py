# TODO: should this live here or a directory level up?

class TokensExhaustedException(Exception): pass


class TokenProxy:

    def __init__(self, tokens):
        self._tokens = tokens
        self.current_token_position = 0

    def get_next_token(self):
        if self.current_token_position >= len(self._tokens):
            raise TokensExhaustedException

        current_token = self._tokens[self.current_token_position]
        self.current_token_position += 1
        return current_token

    def set_token_position(self, token_position):
        self.current_token_position = token_position

    # ideally used only for error reporting and logging
    def get_current_token(self):
        try:
            return self._tokens[self.current_token_position]
        except IndexError:
            return None
