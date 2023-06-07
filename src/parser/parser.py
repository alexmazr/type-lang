from ply.yacc import yacc
from .lexer import *
from ..ast import ast

name = ''
typeParser = None


def parse(programName, input):
    global name, tyepParser
    name = programName
    lexer = lex()
    typeParser = yacc()
    return typeParser.parse(input)


def p_program(p):
    'program : compound_statements'
    global name
    p[0] = ast.Program(name, p[1])


def p_compound_statements(p):
    '''
    compound_statements :
               | compound_statement
               | compound_statements compound_statement
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_compound_statement(p):
    '''
    compound_statement : type_definition
                       | function_definition
                       | use_statement
                       | annotation
    '''
    p[0] = p[1]


def p_use_statement(p):
    'use_statement : USE'
    path = p[1].split()[1][:-1]
    astPath = ast.RelLocator(path) if path[0] == '.' else ast.AbsLocator(path)
    p[0] = ast.Use(astPath)


def p_function_definition(p):
    '''
    function_definition : FN NAME LPAREN arguments RPAREN block
                        | FN NAME LPAREN arguments RPAREN typename block
    '''
    if len(p) == 8:
        p[0] = ast.FnDef(p[2], p[4], p[6], p[7])
    else:
        p[0] = ast.FnDef(p[2], p[4], ast.Void(), p[5])


def p_arguments(p):
    '''
    arguments :
              | argument
              | arguments COMMA argument
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_argument(p):
    'argument : typename NAME'
    p[0] = ast.Argument(p[1], p[2])


def p_annotation(p):
    '''
    annotation : AT pre
               | AT post
    '''
    p[0] = p[2]


def p_pre(p):
    'pre : PRE LPAREN expression RPAREN'
    p[0] = ast.Pre(p[3])


def p_post(p):
    'post : POST LPAREN expression RPAREN'
    p[0] = ast.Post(p[3])


def p_block(p):
    'block : LCURLY statements RCURLY'
    p[0] = p[2]


def p_statements(p):
    '''
    statements :
               | statement
               | statements statement
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_statement(p):
    '''
    statement : compound_statement
              | simple_statement
    '''
    p[0] = p[1]


def p_simple_statement(p):
    '''
    simple_statement : declaration
                     | return
    '''
    p[0] = p[1]


def p_return(p):
    'return : RETURN expression SEMICOLON'
    p[0] = ast.Return(p[2])


def p_declaration(p):
    'declaration : typename NAME ASSIGN expression SEMICOLON'
    p[0] = ast.Declare(p[1], p[2], p[4])


def p_expression(p):
    'expression : sum'
    p[0] = p[1]


def p_sum(p):
    '''
    sum : term
        | sum SUB term
        | sum ADD term
    '''
    if len(p) == 4:
        if p[2] == '+':
            p[0] = ast.Add(p[1], p[3])
        elif p[2] == '-':
            p[0] = ast.Sub(p[1], p[3])
    else:
        p[0] = p[1]


def p_term(p):
    '''
    term : unary
         | term DIV unary
         | term MUL unary
    '''
    if len(p) == 4:
        if p[2] == '*':
            p[0] = ast.Mul(p[1], p[3])
        elif p[2] == '/':
            p[0] = ast.Div(p[1], p[3])
    else:
        p[0] = p[1]


def p_unary(p):
    '''
    unary : value
          | SUB value
    '''
    if len(p) == 3:
        p[0] = ast.USub(p[2])
    else:
        p[0] = p[1]


def p_value(p):
    '''
    value : ref
          | integer
          | group
    '''
    p[0] = p[1]


def p_group(p):
    'group : LPAREN expression RPAREN'
    p[0] = p[2]


def p_ref(p):
    'ref : NAME'
    p[0] = ast.Ref(p[1])


def p_integer(p):
    'integer : INTEGER'
    p[0] = ast.Integer(p[1])


def p_type_definition(p):
    '''
    type_definition : TYPE typename IS base_type SEMICOLON
    '''
    p[0] = ast.TypeDef(p[2], p[4])


def p_base_type(p):
    '''
    base_type : unsigned
              | typename
    '''
    p[0] = p[1]


def p_unsigned(p):
    'unsigned : UNSIGNED LT integer GT'
    p[0] = ast.Unsigned(p[3])


def p_typename(p):
    '''
    typename : NAME
             | NAME QUESTION
             | NAME BANG
             | NAME QUESTION BANG
    '''
    if len(p) == 2:
        p[0] = ast.TypeName(p[1], False, False)
    elif len(p) == 3:
        if p[2] == '?':
            p[0] = ast.TypeName(p[1], True, False)
        elif p[2] == '!':
            p[0] = ast.TypeName(p[1], False, True)
    else:
        p[0] = ast.TypeName(p[1], True, True)


def p_error(p):
    global typeParser
    if p:
        if p.type == 'NEWLINE':
        # Ignore any newline characters that are unhandled in our grammar
            typeParser.errok()
            return typeParser.token()
        raise SystemExit(f"Syntax error: '{p.value}' on line: {p.lineno}, {p.lexpos}")
    raise SystemExit(f"An unknown error occured while parsing")
