# pcode_lexer.py  17/01/2016  D.J.Whale

keywords = (
'IF',           'THEN',         'ELSE',         'ENDIF',        'WHILE',
'ENDWHILE',     'CASE',         'OF',           'ENDCASE',      'FOR',
'TO',           'ENDFOR',       'REPEAT',       'UNTIL',        'FUNCTION',
'ENDFUNCTION',  'RETURN',       'PROCEDURE',    'ENDPROCEDURE', 'READLINE',
'WRITELINE',    'OUTPUT',       'USERINPUT',    'LEN',          'MOD',
'NOT',          'FALSE',        'TRUE',         'AND',          'OR',
'XOR',
'WHEN',         'USE',          'AT',           'AS'
)

tokens = keywords + (
'PLUS',         'MINUS',        'TIMES',        'DIVIDE',
'EQUAL',        'NOTEQUAL',     'LESS',         'LESSEQUAL',    'GREATER',
'GREATEREQUAL', 'ASSIGN',       'LPAREN',       'RPAREN',       'LSQUARE',
'RSQUARE',      'COMMA',        'COLON',

'ID',           'NUMBER',       'STRING'
)

# token definitions

t_PLUS          = r'\+'
t_MINUS         = r'\-'
t_TIMES         = r'\*'
t_DIVIDE        = r'/'
t_EQUAL         = r'='
t_NOTEQUAL      = r'<>'
t_LESS          = r'<'
t_LESSEQUAL     = r'<='
t_GREATER       = r'>'
t_GREATEREQUAL  = r'>='
t_ASSIGN        = r'<-'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'
t_LSQUARE       = r'\['
t_RSQUARE       = r'\]'
t_COMMA         = r'\,'
t_COLON         = r':'
t_AT            = r'@'

def t_comment(t):
    r"[ ]*\043[^\n]*"  # \043 is '#'
    pass #comments are stripped, they don't generate a lexval

def t_STRING(t):
    r'\".*?\"'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = t.value
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


# END




