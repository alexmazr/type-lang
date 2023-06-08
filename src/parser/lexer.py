from ply.lex import lex


def test(data):
    lexer = lex()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)


reserved_words = {
    'use': 'USE',
    'type': 'TYPE',
    'is': 'IS',
    'fn': 'FN',
    'return': 'RETURN',
    'pre': 'PRE',
    'post': 'POST',
    'mut': 'MUT',
    'give': 'GIVE',
    'take': 'TAKE',
    'new': 'NEW',
    'shared': 'SHARED',
    'unsigned': 'UNSIGNED'
}

tokens = ('USE', 'TYPE', 'IS', 'UNSIGNED', 'NAME', 'INTEGER', 'LT', 'GT',
          'SEMICOLON', 'ADD', 'SUB', 'MUL', 'DIV', 'ASSIGN', 'RETURN',
          'LPAREN', 'RPAREN', 'FN', 'LCURLY', 'RCURLY', 'COMMA', 'BANG',
          'QUESTION', 'AT', 'PRE', 'POST', 'MUT', 'GIVE', 'TAKE', 'DOT',
          'NEW', 'STRING', 'SHARED')


# ignore comments
def t_COMMENT(t):
    r'\/\/+.*'
    pass


def t_USE(t):
    r'use (.*);'
    t.type = 'USE'
    return t


def t_STRING(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]
    return t


# match any word, it could be a reserved word so check it
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_words.get(t.value, 'NAME')
    return t


# match any integer literal
def t_INTEGER(t):
    r'\d+'
    return t

# todo: add support for other literal types


# match newlines only increments line number, throw them out
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    pass


# Double length tokens, matched before single length
# t_RSHIFT = r'>>'
# t_LSHIFT = r'<<'
# t_GTE = r'>='
# t_LTE = r'<='
# t_EQ = r'=='

# Single length tokens, matched last
t_ignore = ' \t'
# t_BITXOR = r'\^'
# t_BITAND = r'&'
# t_BITOR = r'\|'
# t_MOD = r'%'
t_AT = r'@'
t_BANG = r'!'
t_QUESTION = r'\?'
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_ASSIGN = r'='
t_DOT = r'\.'
t_COMMA = r','
t_LT = r'<'
t_GT = r'>'
t_SEMICOLON = r';'
# t_INV = r'~'


def t_error(t):
    raise SystemExit("Illegal character: ",
                     f"{t.value[0]} at: {t.lineno}, {t.lexpos}")
