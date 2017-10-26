import sys


def label_line_numbers(filename):
    """Add comments to provided asm file that indicate the line number as seen
    by the CPU emulator program provided by the course.  The CPU emulator
    removes all the comments and blank lines from the file, but comments and
    blank lines are nice for readability.
    """

    with open(filename, 'r') as asm_file:
        line_num = 0
        for line in asm_file.readlines():
            line = line.strip()
            if _should_label(line):
                print '{}\t\t\t// line {}'.format(line, line_num)
                line_num += 1
            else:
                print line


def _should_label(line):
    stripped = line.lstrip()
    return not (
        len(stripped) == 0
        or stripped.startswith('(')
        or stripped.startswith('//')
    )



if __name__ == '__main__':
    label_line_numbers(sys.argv[1])
