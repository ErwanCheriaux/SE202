from ast.nodes import *
from . import tokenizer
import ply.yacc as yacc

tokens = tokenizer.tokens

precedence = (
    ('left', 'SEMICOLON'),
    ('nonassoc', 'THEN'),
    ('nonassoc', 'ELSE'),
    ('nonassoc', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'INF', 'SUP', 'EQU', 'DIFF', 'INFEQU', 'SUPEQU'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV'),
    ('right', 'UMINUS'),
)

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = BinaryOperator('-', IntegerLiteral(0), p[2])

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

def p_expression_assignment(p):
    '''expression : ID ASSIGN expression'''
    p[0] = Assignment(Identifier(p[1]), p[3])

def p_expression_ifthenelse(p):
    '''expression : IF expression THEN expression
                  | IF expression THEN expression ELSE expression'''
    if len(p) == 5:
        p[0] = IfThenElse(p[2], p[4], None)
    else:
        p[0] = IfThenElse(p[2], p[4], p[6])

def p_seqexp(p):
    '''seqexp :
              | seqexpsome
              | LPAREN RPAREN
              | LPAREN seqexpsome RPAREN'''
    if len(p) == 1 or len(p) == 3:
        p[0] = []
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_seqexpsome(p):
    '''seqexpsome : expression
                  | seqexpsome SEMICOLON expression'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = IntegerLiteral(p[1])

def p_expression_identifier(p):
    'expression : ID'
    p[0] = Identifier(p[1])

def p_expression_let(p):
    '''expression : LET decls IN seqexp END'''
    p[0] = Let(p[2], p[4])

def p_decls(p):
    '''decls : decl
             | decls decl'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[2]]

def p_decl(p):
    '''decl : vardecl
            | fundecl'''
    p[0] = p[1]

def p_vardecl(p):
    '''vardecl : VAR ID ASSIGN expression
               | VAR ID COLON type ASSIGN expression'''
    if len(p) == 5:
        p[0] = VarDecl(p[2], None, p[4])
    else:
        p[0] = VarDecl(p[2], p[4], p[6])

def p_fundecl(p):
    '''fundecl : FUNCTION ID LPAREN args RPAREN EQU seqexp
               | FUNCTION ID LPAREN args RPAREN COLON type EQU seqexp'''
    if len(p) == 8:
        p[0] = FunDecl(p[2], p[4], None, SeqExp(p[7]))
    else:
        p[0] = FunDecl(p[2], p[4], p[7], SeqExp(p[9]))

def p_args(p):
    '''args :
            | argssome'''
    p[0] = p[1] if len(p) == 2 else []

def p_argssome(p):
    '''argssome : arg
                | argssome COMMA arg'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_arg(p):
    '''arg : ID COLON type'''
    p[0] = VarDecl(p[1], p[3], None)

def p_type(p):
    '''type : INT'''
    p[0] = Type(p[1])

def p_expression_funcall(p):
    '''expression : ID LPAREN params RPAREN'''
    p[0] = FunCall(Identifier(p[1]), p[3])

def p_params(p):
    '''params :
              | paramssome'''
    p[0] = p[1] if len(p) == 2 else []

def p_paramssome(p):
    '''paramssome : param
                  | paramssome COMMA param'''
    p[0] = [p[1]] if len(p) == 2 else p[1] + [p[3]]

def p_param(p):
    '''param : expression'''
    p[0] = p[1]

def p_error(p):
    import sys
    sys.stderr.write("no way to analyze %s\n" % p)
    sys.exit(1)

parser = yacc.yacc()

def parse(text):
    return parser.parse(text, lexer = tokenizer.lexer.clone())
