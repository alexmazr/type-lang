import sys
from .parser import parser
from .parser import lexer
from .compiler import compiler
from .runtime import unchecked

if __name__ == '__main__':
    if sys.argv[1] == 'lex':
        with open(sys.argv[2], 'r') as file:
            lexer.test(file.read())
    elif sys.argv[1] == 'build':
        with open(sys.argv[2], 'r') as file:
            print(compiler.compile(parser.parse(sys.argv[2], file.read())))
    elif sys.argv[1] == 'run':
        with open(sys.argv[2], 'r') as file:
            tyo = compiler.compile(parser.parse(sys.argv[2], file.read()))
            unchecked.run(tyo[0], tyo[1])
    elif sys.argv[1] == 'ast':
        with open(sys.argv[2], 'r') as file:
            print(parser.parse(sys.argv[2], file.read()))
    else:
        print('Invalid command')
