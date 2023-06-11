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
    else:
        p[0] = []


def p_compound_statement(p):
    '''
    compound_statement : type_definition
                       | function_definition
                       | use_statement
    '''
    p[0] = p[1]


def p_use_statement(p):
    'use_statement : USE'
    path = p[1].split()[1][:-1]
    astPath = ast.RelLocator(path) if path[0] == '.' else ast.AbsLocator(path)
    p[0] = ast.Use(astPath)


def p_function_definition(p):
    '''
    function_definition : annotations FN NAME LPAREN arguments RPAREN block
                        | annotations FN NAME LPAREN arguments RPAREN typename block
                        | annotations FN NAME LPAREN arguments RPAREN GIVE typename block
    '''
    if len(p) == 10:
        p[0] = ast.FnDef(p[3], p[1], p[5], True, p[8], p[9])
    elif len(p) == 9:
        p[0] = ast.FnDef(p[3], p[1], p[5], False, p[7], p[8])
    else:
        p[0] = ast.FnDef(p[3], p[1], p[5], False, ast.TypeData(ast.Void(), None, None), p[7])


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
    else:
        p[0] = []


def p_argument(p):
    '''
    argument : typename NAME
             | TAKE typename NAME
    '''
    if len(p) == 4:
        p[0] = ast.Argument(p[2], p[3], True)
    else:
        p[0] = ast.Argument(p[1], p[2], False)


def p_parameters(p):
    '''
    parameters :
               | parameter
               | parameters COMMA parameter
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]


def p_parameter(p):
    '''
    parameter : qualified_expression
              | GIVE qualified_expression
    '''
    if len(p) == 3:
        p[0] = ast.Parameter(p[2], True)
    else:
        p[0] = ast.Parameter(p[1], False)


def p_annotations(p):
    '''
    annotations :
                | annotation
                | annotations annotation
    '''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    elif len(p) == 2:
        p[0] = [p[1]]


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
                     | assign
                     | call SEMICOLON
    '''
    p[0] = p[1]


def p_declaration(p):
    'declaration : typename assign'
    p[0] = ast.Declare(p[1], p[2].name, p[2].expr)


def p_assign(p):
    'assign : NAME ASSIGN qualified_expression SEMICOLON'
    p[0] = ast.Assign(p[1], p[3])


def p_return(p):
    'return : RETURN qualified_expression SEMICOLON'
    p[0] = ast.Return(p[2])


def p_qualified_expression(p):
    '''
    qualified_expression : expression
                         | NEW expression
                         | SHARED expression
    '''
    if len(p) == 3:
        if p[1] == 'new':
            p[0] = ast.New(p[2])
        else:
            p[0] = ast.Shared(p[2])
    else:
        p[0] = p[1]


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
    unary : call
          | SUB call
    '''
    if len(p) == 3:
        p[0] = ast.USub(p[2])
    else:
        p[0] = p[1]


def p_call(p):
    '''
    call : call LPAREN parameters RPAREN
         | call DOT ref
         | value
    '''
    if len(p) == 5:
        p[0] = ast.Call(p[1], p[3])
    elif len(p) == 4:
        if not isinstance(p[1], list):
            p[1] = [p[1]]
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = p[1]


def p_value(p):
    '''
    value : ref
          | integer
          | string
          | group
    '''
    p[0] = p[1]


def p_group(p):
    'group : LPAREN expression RPAREN'
    p[0] = p[2]


def p_ref(p):
    'ref : NAME'
    p[0] = ast.Ref(p[1])


def p_string(p):
    'string : STRING'
    p[0] = ast.String(p[1])


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
             | NAME typepostfix
             | typeprefix NAME
             | typeprefix NAME typepostfix
    '''
    if len(p) == 2:
        p[0] = ast.TypeData(p[1], None, None)
    elif len(p) == 3:
        if '!' in p[2] or '?' in p[2]:  # is postfixed
            p[0] = ast.TypeData(p[1], None, p[2])
        else:
            p[0] = ast.TypeData(p[2], p[1], None)
    else:
        p[0] = ast.TypeData(p[2], p[1], p[3])


def p_typeprefix(p):
    '''
    typeprefix : MUT
    '''
    p[0] = p[1]


def p_typeportfix(p):
    '''
    typepostfix : BANG
                | QUESTION
                | BANG QUESTION
                | QUESTION BANG
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}{p[2]}"


def p_error(p):
    global typeParser
    if p:
        if p.type == 'NEWLINE':
        # Ignore any newline characters that are unhandled in our grammar
            typeParser.errok()
            return typeParser.token()
        raise SystemExit(f"Syntax error: '{p.value}' on line: {p.lineno}, {p.lexpos}, {p}")
    raise SystemExit(f"An unknown error occured while parsing")
