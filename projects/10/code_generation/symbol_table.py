from collections import defaultdict
from collections import namedtuple


SymbolInfo = namedtuple('SymbolInfo', ['type', 'kind', 'offset'])


class SymbolTable:

    subroutine_scope_kinds = {'var', 'arg'}

    def __init__(self):
        self.class_symbols = {}
        self.subroutine_symbols = {}
        self.symbol_kind_to_next_offset = defaultdict(int)

    def add_symbol(self, name, type_, kind):
        symbol_info = SymbolInfo(type_, kind, self.symbol_kind_to_next_offset[kind])
        self.symbol_kind_to_next_offset[kind] += 1

        if kind in self.subroutine_scope_kinds:
            self.subroutine_symbols[name] = symbol_info
        else:
            self.class_symbols[name] = symbol_info

    def reset_subroutine_table(self):
        self.subroutine_symbols.clear()

        for subroutine_scope_kind in self.subroutine_scope_kinds:
            self.symbol_kind_to_next_offset[subroutine_scope_kind] = 0

    def get_count_of_symbol_kind(self, kind):
        return self.symbol_kind_to_next_offset[kind]

    def lookup_symbol(self, symbol_name):
        if symbol_name in self.subroutine_symbols:
            return self.subroutine_symbols[symbol_name]
        elif symbol_name in self.class_symbols:
            return self.class_symbols[symbol_name]
        else:
            return None
