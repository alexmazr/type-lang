import sys
from .parser import parser
from .parser import lexer
from .compiler import compiler
from .runtime import unchecked
from .logging import logger

if __name__ == '__main__':
    name = sys.argv[2].split('.')[0]
    if len(sys.argv) > 3:
        match sys.argv[3]:
            case '-d':
                print("setting log level debug")
                logger.level = logger.LogLevel.DEBUG
    if sys.argv[1] == 'lex':
        with open(sys.argv[2], 'r') as file:
            lexer.test(file.read())
    elif sys.argv[1] == 'build':
        with open(sys.argv[2], 'r') as file:
            compiler.compile(parser.parse(name, file.read()))
    elif sys.argv[1] == 'run':
        with open(sys.argv[2], 'r') as file:
            tyo = compiler.compile(parser.parse(name, file.read()))
            unchecked.run(tyo[0], tyo[1])
    elif sys.argv[1] == 'ast':
        with open(sys.argv[2], 'r') as file:
            lexer.test(file.read())
            print("========== ast ==========")
            print(parser.parse(name, file.read()))
    else:
        print('Invalid command')
