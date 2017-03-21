import ply.lex as lex

states = (
   ('ccomment','exclusive'),
)

# List of keywords. Each keyword will be return as a token of a specific
# type, which makes it easier to match it in grammatical rules.
keywords = {'array': 'ARRAY',
            'break': 'BREAK',
            'do': 'DO',
            'else': 'ELSE',
            'end': 'END',
            'for': 'FOR',
            'function': 'FUNCTION',
            'if': 'IF',
            'in': 'IN',
            'let': 'LET',
            'nil': 'NIL',
            'of': 'OF',
            'then': 'THEN',
            'to': 'TO',
            'type': 'TYPE',
            'var': 'VAR',
            'while': 'WHILE'}

#Liste of reserved words
reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'let': 'LET',
   'in': 'IN',
   'end': 'END',
   'var': 'VAR',
   'function': 'FUNCTION',
   'int': 'INT',
   'while': 'WHILE',
   'do': 'DO',
   'for': 'FOR',
   'to': 'TO',
}

# List of tokens that can be recognized and are handled by the current
# grammar rules.
tokens = ('PLUS', 'MINUS', 'TIMES', 'DIV', 'OR', 'AND',
          'INF', 'SUP', 'INFEQU', 'SUPEQU', 'EQU', 'DIFF',
          'COMMA', 'SEMICOLON',
          'LPAREN', 'RPAREN',
          'NUMBER', 'ID',
          'COLON', 'ASSIGN') + tuple(reserved.values())

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIV       = r'\/'
t_OR        = r'\|'
t_AND       = r'\&'
t_INF       = r'\<'
t_SUP       = r'\>'
t_INFEQU    = r'\<\='
t_SUPEQU    = r'\>\='
t_EQU       = r'\='
t_DIFF      = r'\<\>'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COLON     = r':'
t_SEMICOLON = r';'
t_ASSIGN    = r':='
t_COMMA     = r','

t_IF       = r'if'
t_THEN     = r'then'
t_ELSE     = r'else'
t_LET      = r'let'
t_IN       = r'in'
t_END      = r'end'
t_VAR      = r'var'
t_FUNCTION = r'function'
t_INT      = r'int'
t_WHILE    = r'while'
t_DO       = r'do'
t_FOR      = r'for'
t_TO       = r'to'

t_ignore = ' \t'

# Count lines when newlines are encountered
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Distinguish between identifier and keyword. If the keyword is not also
# in the tokens list, this is a syntax error pure and simple since we do
# not know what to do about it.
def t_ID(t):
    r'[A-Za-z][A-Za-z\d_]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    if t.value in keywords:
        t.type = keywords.get(t.value)
        if t.type not in tokens:
            raise lex.LexError("unhandled keyword %s" % t.value, t.type)
    return t

# Recognize number - no leading 0 are allowed
def t_NUMBER(t):
    r'[1-9]\d*|0'
    t.value = int(t.value)
    return t

def t_error(t):
    raise lex.LexError("unknown token %s" % t.value, t.value)

def t_ligne_comment(t):
    r'(//.*)'

def t_ANY_begin_ccomment(t):
    r'/\*'
    t.lexer.push_state('ccomment')

def t_ANY_end_ccomment(t):
    r'\*/'
    t.lexer.pop_state()

def t_ccomment_eof(t):
    r'\0'
    raise lex.LexError("ccomment not close %s" % t.value, t.value)

t_ccomment_ignore = " \t\n"

def t_ccomment_error(t):
    t.lexer.skip(1)

lexer = lex.lex()
