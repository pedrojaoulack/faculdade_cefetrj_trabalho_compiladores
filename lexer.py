# lexer.py - Analisador Léxico para RoboLang
# ===== MODIFICAÇÃO PRINCIPAL: Implementação do Lexer com PLY =====
# Gerador de Analisadores: PLY (Python Lex-Yacc) - Componente LEX
# Referência: https://www.dabeaz.com/ply/
#
# Este arquivo implementa:
# 1. ANÁLISE LÉXICA - Reconhecimento de tokens através de expressões regulares
# 2. TOKENS - Definição de todos os símbolos terminais da linguagem
# 3. PALAVRAS RESERVADAS - Mapeamento de identificadores para tokens especiais
# 4. FUNÇÕES DE TOKENIZAÇÃO - Regras customizadas para números, strings, comentários
# ======================================================================

import ply.lex as lex

# ===== MODIFICAÇÃO: Lista de Tokens Personalizados =====
# Cada token representa um símbolo terminal na gramática da linguagem
# (MODIFICADO - tokens criados para RoboLang)
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
# Cada linha define um padrão de reconhecimento simples para um token terminal
# Formato: t_NOME_TOKEN = r'padrão_regex'
t_ASSIGN = r'='         # Operador de atribuição
t_EQUALS = r'=='        # Comparador de igualdade
t_NOTEQUALS = r'!='     # Comparador de desigualdade
t_LESS = r'<'           # Comparador menor que
t_GREATER = r'>'        # Comparador maior que
t_LESSEQUAL = r'<='     # Comparador menor ou igual
t_GREATEREQUAL = r'>='  # Comparador maior ou igual
t_LBRACE = r'\{'        # Abre bloco
t_RBRACE = r'\}'        # Fecha bloco
t_LPAREN = r'\('        # Abre parêntese
t_RPAREN = r'\)'        # Fecha parêntese
t_SEMICOLON = r';'      # Terminador de sentença
t_COMMA = r','          # Separador de elementos
t_PLUS = r'\+'          # Operador adição
t_MINUS = r'-'          # Operador subtração
t_MULTIPLY = r'\*'      # Operador multiplicação
t_DIVIDE = r'/'         # Operador divisão

# Regra para números (MODIFICADO - aceita inteiros e decimais)
# Expressão regular: \d+(\.\d+)? reconhece números inteiros ou com ponto decimal
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Regra para strings (MODIFICADO - strings entre aspas duplas)
# Expressão regular: "[^"]*" reconhece conteúdo entre aspas duplas
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]  # Remove as aspas duplas dos extremos
    return t

# Regra para identificadores e palavras reservadas (MODIFICADO)
# Expressão regular: [a-zA-Z_][a-zA-Z_0-9]* reconhece nomes válidos em linguagens
# Verifica se é uma palavra reservada e atribui o token correspondente
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Busca na tabela de palavras reservadas
    return t

# Regra para contar linhas
# Quando encontra quebra de linha, incrementa o número de linhas do lexer
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espaços e tabs
# Estes caracteres não formam tokens, apenas separam outros tokens
t_ignore = ' \t'

# Regra para comentários (MODIFICADO - comentários com //)
# Expressão regular: //.*  reconhece // seguido de qualquer caractere até fim de linha
# A função 'pass' descarta o token, ignorando o comentário
def t_COMMENT(t):
    r'//.*'
    pass  # Ignora comentários - não retorna token

# Tratamento de erros
# Quando encontra um caractere não reconhecido, exibe mensagem de erro
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# ===== FIM DAS MODIFICAÇÕES DO LEXER =====

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
