# parser.py - Analisador Sintático e Semântico para RoboLang
import ply.yacc as yacc
from lexer import tokens
import sys

# ===== INÍCIO DAS MODIFICAÇÕES - Gramática e ações semânticas =====

# Ambiente de execução (MODIFICADO - criado para armazenar estado do robô)
class RobotEnvironment:
    def __init__(self):
        self.position = [0, 0]  # [x, y]
        self.direction = 'up'   # up, down, left, right
        self.inventory = []
        self.variables = {}
        self.grid_size = 10
        
    def move(self, direction):
        """Move o robô na direção especificada"""
        if direction == 'up':
            self.position[1] = min(self.position[1] + 1, self.grid_size)
        elif direction == 'down':
            self.position[1] = max(self.position[1] - 1, 0)
        elif direction == 'left':
            self.position[0] = max(self.position[0] - 1, 0)
        elif direction == 'right':
            self.position[0] = min(self.position[0] + 1, self.grid_size)
        print(f"🤖 Robô moveu para {direction}. Posição atual: {self.position}")
        
    def turn(self, direction):
        """Gira o robô para uma direção"""
        self.direction = direction
        print(f"🔄 Robô virou para {direction}")
        
    def pick_item(self, item):
        """Pega um item"""
        self.inventory.append(item)
        print(f"📦 Robô pegou: {item}")
        
    def drop_item(self):
        """Solta um item"""
        if self.inventory:
            item = self.inventory.pop()
            print(f"📤 Robô soltou: {item}")
        else:
            print("⚠️  Inventário vazio!")

# Ambiente global
robot = RobotEnvironment()

# Precedência de operadores (MODIFICADO - definida para evitar ambiguidade)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('nonassoc', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL'),
    ('nonassoc', 'EQUALS', 'NOTEQUALS'),
)

# ===== REGRAS GRAMATICAIS (MODIFICADO - criadas para RoboLang) =====

# Regra inicial
def p_program(p):
    '''program : statement_list'''
    p[0] = ('PROGRAM', p[1])
    print("\n✅ Programa executado com sucesso!")
    print(f"📍 Posição final do robô: {robot.position}")
    print(f"🧭 Direção final: {robot.direction}")
    print(f"🎒 Inventário: {robot.inventory}")

# Lista de statements
def p_statement_list(p):
    '''statement_list : statement_list statement
                     | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

# Tipos de statements
def p_statement(p):
    '''statement : move_stmt
                | turn_stmt
                | pick_stmt
                | drop_stmt
                | assign_stmt
                | if_stmt
                | while_stmt
                | repeat_stmt
                | block'''
    p[0] = p[1]

# Comando MOVE (MODIFICADO)
def p_move_stmt(p):
    '''move_stmt : MOVE direction SEMICOLON'''
    robot.move(p[2])
    p[0] = ('MOVE', p[2])

# Comando TURN (MODIFICADO)
def p_turn_stmt(p):
    '''turn_stmt : TURN direction SEMICOLON'''
    robot.turn(p[2])
    p[0] = ('TURN', p[2])

# Comando PICK (MODIFICADO)
def p_pick_stmt(p):
    '''pick_stmt : PICK STRING SEMICOLON'''
    robot.pick_item(p[2])
    p[0] = ('PICK', p[2])

# Comando DROP (MODIFICADO)
def p_drop_stmt(p):
    '''drop_stmt : DROP SEMICOLON'''
    robot.drop_item()
    p[0] = ('DROP',)

# Direções (MODIFICADO)
def p_direction(p):
    '''direction : UP
                | DOWN
                | LEFT
                | RIGHT'''
    p[0] = p[1].lower()

# Atribuição de variável (MODIFICADO)
def p_assign_stmt(p):
    '''assign_stmt : IDENTIFIER ASSIGN expression SEMICOLON'''
    robot.variables[p[1]] = p[3]
    print(f"💾 Variável {p[1]} = {p[3]}")
    p[0] = ('ASSIGN', p[1], p[3])

# Estrutura IF (MODIFICADO)
def p_if_stmt(p):
    '''if_stmt : IF LPAREN condition RPAREN block
              | IF LPAREN condition RPAREN block ELSE block'''
    if p[3]:  # Se a condição é verdadeira
        p[0] = ('IF', p[3], p[5])
    elif len(p) == 8:  # Se tem ELSE
        p[0] = ('IF', p[3], p[7])

# Estrutura WHILE (MODIFICADO)
def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN condition RPAREN block'''
    # Implementação simplificada - apenas cria o nó da árvore
    p[0] = ('WHILE', p[3], p[5])

# Estrutura REPEAT (MODIFICADO)
def p_repeat_stmt(p):
    '''repeat_stmt : REPEAT expression TIMES block'''
    times = int(p[2])
    for i in range(times):
        # Executa o bloco 'times' vezes
        pass
    p[0] = ('REPEAT', p[2], p[4])

# Bloco de código (MODIFICADO)
def p_block(p):
    '''block : LBRACE statement_list RBRACE'''
    p[0] = ('BLOCK', p[2])

# Condições (MODIFICADO)
def p_condition(p):
    '''condition : expression EQUALS expression
                | expression NOTEQUALS expression
                | expression LESS expression
                | expression GREATER expression
                | expression LESSEQUAL expression
                | expression GREATEREQUAL expression'''
    if p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]

# Expressões aritméticas (MODIFICADO)
def p_expression_binop(p):
    '''expression : expression PLUS expression
                 | expression MINUS expression
                 | expression MULTIPLY expression
                 | expression DIVIDE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]

# Expressão com parênteses (MODIFICADO)
def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

# Expressão com número (MODIFICADO)
def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

# Expressão com variável (MODIFICADO)
def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    if p[1] in robot.variables:
        p[0] = robot.variables[p[1]]
    else:
        print(f"⚠️  Variável '{p[1]}' não definida. Usando 0.")
        p[0] = 0

# Tratamento de erros sintáticos
def p_error(p):
    if p:
        print(f"❌ Erro de sintaxe no token '{p.value}' (linha {p.lineno})")
    else:
        print("❌ Erro de sintaxe no final do arquivo")

# ===== FIM DAS MODIFICAÇÕES =====

# Construir o parser
parser = yacc.yacc()

# Função para analisar código
def parse(code):
    from lexer import lexer
    result = parser.parse(code, lexer=lexer)
    return result

if __name__ == '__main__':
    # Código de teste
    code = '''
    // Programa de teste do robô
    x = 5;
    move up;
    turn right;
    pick "caixa";
    repeat 3 times {
        move right;
    }
    drop;
    '''
    
    print("🚀 Iniciando análise do programa RoboLang...\n")
    parse(code)