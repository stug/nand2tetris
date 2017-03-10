class CCommandBuilder(object):

    C_COMMAND_PREFIX = '111'
    JUMP_TO_BITS = {
        '': '000',
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111'
    }
    DEST_TO_BITS = {
        '': '000',
        'M': '001',
        'D': '010',
        'MD': '011',
        'A': '100',
        'AM': '101',
        'AD': '110',
        'AMD': '111'
    }
    COMP_TO_BITS = {
        '0': '101010',
        '1': '111111',
        '-1': '111010',
        'D': '001100',
        'A': '110000',
        '!D': '001101',
        '!A': '110001',
        '-D': '001111',
        '-A': '110011',
        'D+1': '011111',
        'A+1': '110111',
        'D-1': '001110',
        'A-1': '110010',
        'D+A': '000010',
        'D-A': '010011',
        'A-D': '000111',
        'D&A': '000000',
        'D|A': '010101'
    }

    @classmethod
    def build_c_command(cls, sanitized_line):
        """sanitized line is expected to be in the form dest=comp;jump"""
        dest, comp, jump = cls.split_components(sanitized_line)

        if 'M' in comp:
            a_bit = '1'
            comp = comp.replace('M', 'A')
        else:
            a_bit = '0'

        return '{prefix}{a}{comp}{dest}{jump}'.format(
            prefix=cls.C_COMMAND_PREFIX,
            a=a_bit,
            comp=cls.COMP_TO_BITS[comp],
            dest=cls.DEST_TO_BITS[dest],
            jump=cls.JUMP_TO_BITS[jump]
        )

    @classmethod
    def split_components(cls, sanitized_line):
        dest, comp_jump = cls.split_dest(sanitized_line)
        comp, jump = cls.split_comp_jump(comp_jump)
        return dest, comp, jump

    @classmethod
    def split_dest(self, dest_comp_jump):
        equals_index = dest_comp_jump.find('=')
        if equals_index == -1:
            return '', dest_comp_jump
        else:
            return dest_comp_jump[:equals_index], dest_comp_jump[equals_index+1:]

    @classmethod
    def split_comp_jump(self, comp_jump):
        semicolon_index = comp_jump.find(';')
        if semicolon_index == -1:
            return comp_jump, ''
        else:
            return comp_jump[:semicolon_index], comp_jump[semicolon_index+1:]
