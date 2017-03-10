class CommandType(object):

    A_COMMAND = 'a_command'
    C_COMMAND = 'c_command'
    LABEL = 'label'


def base10_to_binary(base10):
    return bin(int(base10))[2:]
