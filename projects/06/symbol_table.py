from util import base10_to_binary

class SymbolTable(object):

    def __init__(self):
        self.next_symbol_address = 16
        self.symbol_table = {
            'SP': base10_to_binary(0),
            'LCL': base10_to_binary(1),
            'ARG': base10_to_binary(2),
            'THIS': base10_to_binary(3),
            'THAT': base10_to_binary(4),
            'SCREEN': base10_to_binary(16384),
            'KBD': base10_to_binary(24576)
        }
        self.symbol_table.update({
            'R{}'.format(n): base10_to_binary(n) for n in xrange(16)
        })

    def add_label_symbol(self, symbol, instruction_address):
        self.symbol_table[symbol] = base10_to_binary(instruction_address)

    def get_or_add_variable_symbol(self, symbol):
        # Don't overwrite a previously written symbol
        if symbol not in self.symbol_table:
            self.symbol_table[symbol] = base10_to_binary(self.next_symbol_address)
            self.next_symbol_address += 1
            return self.symbol_table[symbol]
        else:
            return self.symbol_table[symbol]
