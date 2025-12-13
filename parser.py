# parser.py - Analisador Sintático e Semântico para RoboLang
# ===== MODIFICAÇÃO PRINCIPAL: Implementação do Parser com PLY =====
# Gerador de Analisadores: PLY (Python Lex-Yacc)
# Referência: https://www.dabeaz.com/ply/
# 
# Este arquivo implementa:
# 1. ANÁLISE SINTÁTICA (Yacc) - Análise da estrutura gramatical
# 2. AÇÕES SEMÂNTICAS - Interpretação e execução do código RoboLang
# 3. TABELAS LALR - Geradas automaticamente pelo PLY
# 4. GERADORES: Usa expressões regulares do LEXER (lexer.py) como entrada
# ======================================================================

import ply.yacc as yacc
from lexer import tokens
from tree_visualizer import TreeNode, ParseTreeVisualizer
import sys

# ===== MODIFICAÇÃO: Definição da Classe de Ambiente do Robô =====
# Esta classe armazena o estado do robô durante a interpretação
# Inclui: posição, direção, inventário e variáveis globais
# (MODIFICADO - criado para armazenar estado do robô)
class RobotEnvironment:
    def __init__(self):
        self.position = [5, 5]  # [x, y] - Posição inicial no meio do mapa
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

# ===== MODIFICAÇÃO: Função para re-executar árvores (para repeat) =====
def re_execute_tree(node):
    """Re-executa um TreeNode (para loops como repeat)"""
    if node is None:
        return
    
    if isinstance(node, TreeNode):
        # Verifica o tipo de nó
        if node.label == 'move_stmt' and hasattr(node, 'direction'):
            robot.move(node.direction)
        elif node.label == 'turn_stmt' and hasattr(node, 'direction'):
            robot.turn(node.direction)
        elif node.label == 'statement_list':
            # Re-executa cada statement na lista
            for child in node.children:
                re_execute_tree(child)
        elif node.label == 'statement':
            # Re-executa o statement
            for child in node.children:
                re_execute_tree(child)
        else:
            # Re-executa os filhos
            for child in node.children:
                re_execute_tree(child)

# ===== MODIFICAÇÃO: Definição de Precedência de Operadores =====
# A precedência resolva ambiguidades na gramática (exemplo: 2+3*4 = 14 ou 20?)
# Regras de precedência (do menor para o maior):
# 1. left: associação à esquerda
# 2. PLUS, MINUS: operadores de mesmo nível (soma e subtração)
# 3. MULTIPLY, DIVIDE: precedência maior que soma/subtração
# (MODIFICADO - definida para evitar ambiguidade)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('nonassoc', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL'),
    ('nonassoc', 'EQUALS', 'NOTEQUALS'),
)

# ===== MODIFICAÇÃO: REGRAS GRAMATICAIS E AÇÕES SEMÂNTICAS =====
# Cada função p_NOME define uma produção gramatical
# A string docstring contém a regra BNF
# O código define a ação semântica (interpretação da regra)
# Exemplo: p_expression_binop implementa: expression → expression OPERATOR expression
# (MODIFICADO - criadas para RoboLang)

# Regra inicial
# AÇÃO SEMÂNTICA: Exibe mensagem de conclusão e estado final do robô
# p[0] = resultado, p[1] = statement_list
def p_program(p):
    '''program : statement_list'''
    # ===== MODIFICAÇÃO: Capturar árvore de derivação =====
    tree = TreeNode('program')
    if isinstance(p[1], TreeNode):
        tree.add_child(p[1])
    elif isinstance(p[1], list):
        # Se p[1] é lista de statements, criar nó statement_list
        stmt_list = TreeNode('statement_list')
        for stmt in p[1]:
            if isinstance(stmt, TreeNode):
                stmt_list.add_child(stmt)
        tree.add_child(stmt_list)
    
    ParseTreeVisualizer.set_parse_tree(tree)
    p[0] = ('PROGRAM', p[1])
    print("\n✅ Programa executado com sucesso!")
    print(f"📍 Posição final do robô: {robot.position}")
    print(f"🧭 Direção final: {robot.direction}")
    print(f"🎒 Inventário: {robot.inventory}")

# Lista de statements
# AÇÃO SEMÂNTICA: Acumula statements em uma lista
# Produção recursiva à esquerda para melhor performance (LALR)
def p_statement_list(p):
    '''statement_list : statement_list statement
                     | statement'''
    # ===== MODIFICAÇÃO: Criar nó de árvore =====
    stmt_list_node = TreeNode('statement_list')
    
    if len(p) == 3:
        # statement_list statement
        if isinstance(p[1], TreeNode) and p[1].label == 'statement_list':
            # p[1] já é um nó statement_list
            stmt_list_node = p[1]
        elif isinstance(p[1], list):
            # p[1] é uma lista de statements (compatibilidade)
            for stmt in p[1]:
                if isinstance(stmt, TreeNode):
                    stmt_list_node.add_child(stmt)
        elif isinstance(p[1], TreeNode):
            stmt_list_node.add_child(p[1])
        
        # Adiciona novo statement
        if isinstance(p[2], TreeNode):
            stmt_list_node.add_child(p[2])
        elif isinstance(p[2], tuple):
            stmt_node = TreeNode(p[2][0])
            stmt_list_node.add_child(stmt_node)
        
        p[0] = stmt_list_node
    else:
        # Apenas statement
        if isinstance(p[1], TreeNode):
            stmt_list_node.add_child(p[1])
            p[0] = stmt_list_node
        else:
            # Retorna lista para compatibilidade
            p[0] = [p[1]]

# Tipos de statements
# AÇÃO SEMÂNTICA: Agrupa diferentes tipos de comando
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
    # ===== MODIFICAÇÃO: Criar nó statement =====
    stmt_node = TreeNode('statement')
    if isinstance(p[1], TreeNode):
        stmt_node.add_child(p[1])
    p[0] = stmt_node

# ===== MODIFICAÇÃO: Comandos de Movimento do Robô =====
# Comando MOVE: move_stmt → MOVE direction SEMICOLON
# AÇÃO SEMÂNTICA: Executa movimento do robô e retorna nó AST
def p_move_stmt(p):
    '''move_stmt : MOVE direction SEMICOLON'''
    # ===== MODIFICAÇÃO: Capturar árvore =====
    direction_tuple = p[2]  # (TreeNode, valor_string)
    if isinstance(direction_tuple, tuple):
        direction_node, direction_value = direction_tuple
        robot.move(direction_value)
    else:
        # Compatibilidade com código antigo
        robot.move(p[2])
        direction_node = TreeNode('direction')
        direction_node.add_child(TreeNode(p[2].upper(), p[2]))
    
    move_node = TreeNode('move_stmt')
    move_node.add_child(TreeNode('MOVE', 'move'))
    move_node.add_child(direction_node)
    move_node.add_child(TreeNode('SEMICOLON', ';'))
    # Armazena a direção para re-execução
    move_node.direction = direction_value if isinstance(direction_tuple, tuple) else p[2]
    p[0] = move_node

# Comando TURN: turn_stmt → TURN direction SEMICOLON
# AÇÃO SEMÂNTICA: Gira robô para nova direção
def p_turn_stmt(p):
    '''turn_stmt : TURN direction SEMICOLON'''
    # ===== MODIFICAÇÃO: Capturar árvore =====
    direction_tuple = p[2]  # (TreeNode, valor_string)
    if isinstance(direction_tuple, tuple):
        direction_node, direction_value = direction_tuple
        robot.turn(direction_value)
    else:
        # Compatibilidade com código antigo
        robot.turn(p[2])
        direction_node = TreeNode('direction')
        direction_node.add_child(TreeNode(p[2].upper(), p[2]))
    
    turn_node = TreeNode('turn_stmt')
    turn_node.add_child(TreeNode('TURN', 'turn'))
    turn_node.add_child(direction_node)
    turn_node.add_child(TreeNode('SEMICOLON', ';'))
    # Armazena a direção para re-execução
    turn_node.direction = direction_value if isinstance(direction_tuple, tuple) else p[2]
    p[0] = turn_node

# Comando PICK: pick_stmt → PICK STRING SEMICOLON
# AÇÃO SEMÂNTICA: Adiciona item ao inventário
def p_pick_stmt(p):
    '''pick_stmt : PICK STRING SEMICOLON'''
    robot.pick_item(p[2])
    p[0] = ('PICK', p[2])

# Comando DROP: drop_stmt → DROP SEMICOLON
# AÇÃO SEMÂNTICA: Remove item do inventário
def p_drop_stmt(p):
    '''drop_stmt : DROP SEMICOLON'''
    robot.drop_item()
    p[0] = ('DROP',)

# Direções: direction → UP | DOWN | LEFT | RIGHT
# AÇÃO SEMÂNTICA: Converte token para string em minúsculas
def p_direction(p):
    '''direction : UP
                | DOWN
                | LEFT
                | RIGHT'''
    # ===== MODIFICAÇÃO: Retorna tupla (nó, valor string) =====
    direction_node = TreeNode('direction')
    p_value = p[1].lower()
    direction_node.add_child(TreeNode(p[1], p_value))
    # Retorna tupla para compatibilidade
    p[0] = (direction_node, p_value)

# ===== MODIFICAÇÃO: Variáveis e Expressões =====
# Atribuição: assign_stmt → IDENTIFIER ASSIGN expression SEMICOLON
# AÇÃO SEMÂNTICA: Armazena valor em variável global
def p_assign_stmt(p):
    '''assign_stmt : IDENTIFIER ASSIGN expression SEMICOLON'''
    robot.variables[p[1]] = p[3]  # Armazena na tabela de símbolos
    print(f"💾 Variável {p[1]} = {p[3]}")
    p[0] = ('ASSIGN', p[1], p[3])

# ===== MODIFICAÇÃO: Estruturas de Controle de Fluxo =====
# IF: if_stmt → IF LPAREN condition RPAREN block [ELSE block]
# AÇÃO SEMÂNTICA: Executa bloco se condição verdadeira, else opcional
def p_if_stmt(p):
    '''if_stmt : IF LPAREN condition RPAREN block
              | IF LPAREN condition RPAREN block ELSE block'''
    if p[3]:  # Se a condição é verdadeira
        p[0] = ('IF', p[3], p[5])
    elif len(p) == 8:  # Se tem ELSE (len=8: if, (, condition, ), block, else, block)
        p[0] = ('IF', p[3], p[7])

# WHILE: while_stmt → WHILE LPAREN condition RPAREN block
# AÇÃO SEMÂNTICA: Cria nó de loop enquanto (execução não implementada completamente)
def p_while_stmt(p):
    '''while_stmt : WHILE LPAREN condition RPAREN block'''
    # Implementação simplificada - apenas cria o nó da árvore
    p[0] = ('WHILE', p[3], p[5])

# REPEAT: repeat_stmt → REPEAT expression TIMES block
# AÇÃO SEMÂNTICA: Executa bloco N vezes
def p_repeat_stmt(p):
    '''repeat_stmt : REPEAT expression TIMES block'''
    times = int(p[2])
    block_content = p[4]
    
    # ===== MODIFICAÇÃO: Executar bloco múltiplas vezes =====
    # O bloco já foi parseado uma vez durante o parsing
    # Agora re-executamos as instruções (times - 1) vezes
    
    if isinstance(block_content, tuple) and block_content[0] == 'BLOCK':
        statements = block_content[1]
        
        # Re-executa (times - 1) vezes (a primeira execução já ocorreu)
        for iteration in range(times - 1):
            if isinstance(statements, TreeNode):
                # Re-executa a árvore de statements
                re_execute_tree(statements)
            elif isinstance(statements, list):
                # Re-executa lista de statements
                for stmt in statements:
                    if isinstance(stmt, TreeNode):
                        re_execute_tree(stmt)
    
    # ===== MODIFICAÇÃO: Criar TreeNode para repeat =====
    repeat_node = TreeNode('repeat_stmt')
    repeat_node.add_child(TreeNode('REPEAT', 'REPEAT'))
    
    # Adiciona expression
    expr_node = TreeNode('expression')
    expr_node.add_child(TreeNode('NUMBER', str(p[2])))
    repeat_node.add_child(expr_node)
    
    repeat_node.add_child(TreeNode('TIMES', 'TIMES'))
    
    # Adiciona block
    if isinstance(block_content, tuple):
        block_node = TreeNode('block')
        block_node.add_child(TreeNode('LBRACE', '{'))
        if block_content[0] == 'BLOCK':
            stmt_list = block_content[1]
            if isinstance(stmt_list, TreeNode):
                # Clona a estrutura para a árvore
                block_node.add_child(stmt_list)
        block_node.add_child(TreeNode('RBRACE', '}'))
        repeat_node.add_child(block_node)
    
    p[0] = repeat_node

# Bloco: block → LBRACE statement_list RBRACE
# AÇÃO SEMÂNTICA: Agrupa statements em um bloco
def p_block(p):
    '''block : LBRACE statement_list RBRACE'''
    p[0] = ('BLOCK', p[2])

# ===== MODIFICAÇÃO: Condições e Comparações =====
# Condições: condition → expression COMPARADOR expression
# AÇÃO SEMÂNTICA: Avalia expressão booleana
# Comparadores: ==, !=, <, >, <=, >=
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

# ===== MODIFICAÇÃO: Expressões Aritméticas =====
# Expressões binarias: expression → expression OPERADOR expression
# AÇÃO SEMÂNTICA: Realiza operação aritmética
# Operadores: +, -, *, /
# Precedência é resolvida pelas regras de precedence definidas acima
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

# Expressão com parênteses: expression → LPAREN expression RPAREN
# AÇÃO SEMÂNTICA: Retorna valor da expressão dentro de parênteses
def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

# Expressão com número: expression → NUMBER
# AÇÃO SEMÂNTICA: Retorna valor numérico (inteiro ou float)
def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]

# Expressão com variável: expression → IDENTIFIER
# AÇÃO SEMÂNTICA: Busca valor da variável na tabela de símbolos
def p_expression_identifier(p):
    '''expression : IDENTIFIER'''
    if p[1] in robot.variables:
        p[0] = robot.variables[p[1]]
    else:
        print(f"⚠️  Variável '{p[1]}' não definida. Usando 0.")
        p[0] = 0

# Tratamento de erros sintáticos
# Função chamada quando o parser encontra um erro
def p_error(p):
    if p:
        print(f"❌ Erro de sintaxe no token '{p.value}' (linha {p.lineno})")
    else:
        print("❌ Erro de sintaxe no final do arquivo")

# ===== FIM DAS MODIFICAÇÕES DO PARSER =====

# Construir o parser
# yacc.yacc() gera as tabelas LALR automaticamente
# Salva em parsetab.py (já pré-compilado)
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