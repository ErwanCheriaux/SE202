from ast.nodes import *
from . import tokenizer
import ply.yacc as yacc

tokens = tokenizer.tokens

precedence = (
    ('nonassoc', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'INF', 'SUP', 'EQU', 'DIFF', 'INFEQU', 'SUPEQU'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV')
)

def p_expression_ifthenelse(p):
    '''expression : IF expression THEN expression ELSE expression'''
    p[0] = IfThenElse(p[2], p[4], p[6])

def p_expression_binop(p):
    '''expression : expression OR expression
                  | expression AND expression
                  | expression INF expression
                  | expression SUP expression
                  | expression EQU expression
                  | expression DIFF expression
                  | expression INFEQU expression
                  | expression SUPEQU expression
                  | expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIV expression'''
    p[0] = BinaryOperator(p[2], p[1], p[3])

def p_expression_parentheses(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = IntegerLiteral(p[1])

def p_expression_identifier(p):
    'expression : ID'
    p[0] = Identifier(p[1])

def p_decls(p):
    '''decls : decl
             | decls decl'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_decl(p):
    '''decl : vardecl
            | fundecl'''
    p[0] = Decl(p[1])

def p_vardecl(p):
    '''vardecl : VAR ID ASSIGN expression'''
    p[0] = VarDecl(p[2], None, p[4])

def p_args(p):
    '''args :
            | argssome'''
    p[0] = p[1] if len(p) == 2 else []

def p_argssome(p):
    '''argssome : expression
                | argssome COMMA expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_error(p):
    import sys
    sys.stderr.write("no way to analyze %s\n" % p)
    sys.exit(1)

parser = yacc.yacc()

def parse(text):
    return parser.parse(text, lexer = tokenizer.lexer.clone())
