import sys
from .parser import parser
from .parser.lexer import *

if __name__ == '__main__':
    if sys.argv[1] == 'lex':
        with open(sys.argv [2], 'r') as file:
            test(file.read())
    else:
        with open('main.ty', 'r') as file:
            print(parser.parse('main', file.read()))
