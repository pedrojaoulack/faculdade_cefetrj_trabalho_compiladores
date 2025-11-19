# lexer.py - Analisador Léxico para RoboLang
import ply.lex as lex

# ===== INÍCIO DAS MODIFICAÇÕES - Tokens personalizados =====

# Lista de tokens (MODIFICADO - tokens criados para RoboLang)
tokens = (
    # Comandos do robô
    'MOVE',
    'TURN',
    'PICK',
    'DROP',
    
    # Estruturas de controle
    'IF',
    'ELSE',
    'WHILE',
    'REPEAT',
    'TIMES',
    
    # Operadores e comparadores
    'ASSIGN',
    'EQUALS',
    'NOTEQUALS',
    'LESS',
    'GREATER',
    'LESSEQUAL',
    'GREATEREQUAL',
    
    # Direções
    'UP',
    'DOWN',
    'LEFT',
    'RIGHT',
    
    # Tipos e literais
    'NUMBER',
    'IDENTIFIER',
    'STRING',
    
    # Delimitadores
    'LBRACE',
    'RBRACE',
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'COMMA',
    
    # Operadores aritméticos
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
)

# Palavras reservadas (MODIFICADO - criadas para RoboLang)
reserved = {
    'move': 'MOVE',
    'turn': 'TURN',
    'pick': 'PICK',
    'drop': 'DROP',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'repeat': 'REPEAT',
    'times': 'TIMES',
    'up': 'UP',
    'down': 'DOWN',
    'left': 'LEFT',
    'right': 'RIGHT',
}

# Expressões regulares para tokens simples (MODIFICADO)
t_ASSIGN = r'='
t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_LESS = r'<'
t_GREATER = r'>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'

# Regra para números (MODIFICADO - aceita inteiros e decimais)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Regra para strings (MODIFICADO - strings entre aspas)
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Regra para identificadores e palavras reservadas (MODIFICADO)
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t

# Regra para contar linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espaços e tabs
t_ignore = ' \t'

# Regra para comentários (MODIFICADO - comentários com //)
def t_COMMENT(t):
    r'//.*'
    pass  # Ignora comentários

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# ===== FIM DAS MODIFICAÇÕES =====

# Construir o lexer
lexer = lex.lex()

# Função para testar o lexer
if __name__ == '__main__':
    data = '''
    move up;
    x = 10;
    repeat 5 times {
        turn right;
    }
    '''
    
    lexer.input(data)
    for tok in lexer:
        print(tok)