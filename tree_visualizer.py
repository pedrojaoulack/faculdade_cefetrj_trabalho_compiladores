# tree_visualizer.py - Visualizador de Árvore de Derivação e Gramática
# ===== MODIFICAÇÃO: Adicionado para atender aos requisitos do trabalho =====

class TreeNode:
    """Nó da árvore de derivação"""
    def __init__(self, label, children=None):
        self.label = label
        self.children = children or []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __str__(self):
        return self.label

class ParseTreeVisualizer:
    """Classe para visualizar a árvore de derivação e gramática"""
    
    # Gramática da linguagem RoboLang
    GRAMMAR_RULES = [
        "program → statement_list",
        "statement_list → statement_list statement | statement",
        "statement → move_stmt | turn_stmt | pick_stmt | drop_stmt | assign_stmt | if_stmt | while_stmt | repeat_stmt | block",
        "move_stmt → MOVE direction SEMICOLON",
        "turn_stmt → TURN direction SEMICOLON",
        "pick_stmt → PICK STRING SEMICOLON",
        "drop_stmt → DROP SEMICOLON",
        "direction → UP | DOWN | LEFT | RIGHT",
        "assign_stmt → IDENTIFIER ASSIGN expression SEMICOLON",
        "if_stmt → IF LPAREN condition RPAREN block | IF LPAREN condition RPAREN block ELSE block",
        "while_stmt → WHILE LPAREN condition RPAREN block",
        "repeat_stmt → REPEAT expression TIMES block",
        "block → LBRACE statement_list RBRACE",
        "condition → expression EQUALS expression | expression NOTEQUALS expression |",
        "           → expression LESS expression | expression GREATER expression |",
        "           → expression LESSEQUAL expression | expression GREATEREQUAL expression",
        "expression → expression PLUS expression | expression MINUS expression |",
        "           → expression MULTIPLY expression | expression DIVIDE expression",
        "expression → LPAREN expression RPAREN | NUMBER | IDENTIFIER",
    ]
    
    # Tabela de Produções e Ações Semânticas
    SEMANTIC_ACTIONS = [
        ("program → statement_list", "Inicia o programa e exibe posição final do robô"),
        ("move_stmt → MOVE direction SEMICOLON", "Executa movimento do robô usando robot.move()"),
        ("turn_stmt → TURN direction SEMICOLON", "Gira o robô para direção especificada"),
        ("pick_stmt → PICK STRING SEMICOLON", "Adiciona item ao inventário do robô"),
        ("drop_stmt → DROP SEMICOLON", "Remove item do inventário"),
        ("assign_stmt → IDENTIFIER ASSIGN expression SEMICOLON", "Atribui valor a variável: robot.variables[id] = expr"),
        ("if_stmt → IF LPAREN condition RPAREN block", "Executa bloco se condição verdadeira"),
        ("while_stmt → WHILE LPAREN condition RPAREN block", "Executa bloco repetidamente enquanto condição verdadeira"),
        ("repeat_stmt → REPEAT expression TIMES block", "Executa bloco N vezes"),
        ("condition → expression EQUALS expression", "Retorna True se p[1] == p[3]"),
        ("condition → expression LESS expression", "Retorna True se p[1] < p[3]"),
        ("expression → expression PLUS expression", "Retorna p[1] + p[3]"),
        ("expression → expression MINUS expression", "Retorna p[1] - p[3]"),
        ("expression → expression MULTIPLY expression", "Retorna p[1] * p[3]"),
        ("expression → expression DIVIDE expression", "Retorna p[1] / p[3]"),
        ("expression → NUMBER", "Retorna valor numérico"),
        ("expression → IDENTIFIER", "Retorna valor da variável ou 0 se não definida"),
    ]
    
    @staticmethod
    def print_grammar():
        """Imprime a gramática da linguagem"""
        print("\n" + "="*70)
        print("📋 GRAMÁTICA DA LINGUAGEM ROBOLANG")
        print("="*70)
        for i, rule in enumerate(ParseTreeVisualizer.GRAMMAR_RULES, 1):
            print(f"  {i:2d}. {rule}")
        print("="*70)
    
    @staticmethod
    def print_semantic_table():
        """Imprime tabela de produções e ações semânticas"""
        print("\n" + "="*70)
        print("📊 TABELA DE PRODUÇÕES E AÇÕES SEMÂNTICAS")
        print("="*70)
        print(f"{'Produção':<45} {'Ação Semântica':<25}")
        print("-"*70)
        for production, action in ParseTreeVisualizer.SEMANTIC_ACTIONS:
            # Truncar se muito longo
            action_display = action[:24] if len(action) <= 24 else action[:21] + "..."
            print(f"{production:<45} {action_display:<25}")
        print("="*70)
    
    @staticmethod
    def print_tree_ascii(node, prefix="", is_last=True):
        """Imprime árvore em formato ASCII"""
        if node is None:
            return
        
        # Simbolo de conexão
        connector = "└── " if is_last else "├── "
        print(prefix + connector + str(node))
        
        # Próximo prefixo
        new_prefix = prefix + ("    " if is_last else "│   ")
        
        # Imprimir filhos
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            ParseTreeVisualizer.print_tree_ascii(child, new_prefix, is_last_child)
    
    @staticmethod
    def create_example_tree():
        """Cria uma árvore de derivação de exemplo"""
        # Exemplo: move up; turn right;
        root = TreeNode("program")
        
        stmt_list = TreeNode("statement_list")
        root.add_child(stmt_list)
        
        # Primeiro statement: move up;
        stmt1 = TreeNode("statement")
        stmt_list.add_child(stmt1)
        
        move_stmt = TreeNode("move_stmt")
        stmt1.add_child(move_stmt)
        
        move_stmt.add_child(TreeNode("MOVE"))
        
        direction1 = TreeNode("direction")
        move_stmt.add_child(direction1)
        direction1.add_child(TreeNode("UP"))
        
        move_stmt.add_child(TreeNode("SEMICOLON"))
        
        # Segundo statement: turn right;
        stmt_list2 = TreeNode("statement_list")
        stmt_list.add_child(stmt_list2)
        
        stmt2 = TreeNode("statement")
        stmt_list2.add_child(stmt2)
        
        turn_stmt = TreeNode("turn_stmt")
        stmt2.add_child(turn_stmt)
        
        turn_stmt.add_child(TreeNode("TURN"))
        
        direction2 = TreeNode("direction")
        turn_stmt.add_child(direction2)
        direction2.add_child(TreeNode("RIGHT"))
        
        turn_stmt.add_child(TreeNode("SEMICOLON"))
        
        return root
    
    @staticmethod
    def print_derivation_example():
        """Imprime uma derivação de exemplo"""
        print("\n" + "="*70)
        print("🌳 EXEMPLO DE ÁRVORE DE DERIVAÇÃO")
        print("="*70)
        print("\nSentença de entrada: move up; turn right;")
        print("\nDerivação (Leftmost Derivation):")
        print("""
  1. program
  2. ⇒ statement_list
  3. ⇒ statement_list statement
  4. ⇒ move_stmt statement
  5. ⇒ MOVE direction SEMICOLON statement
  6. ⇒ MOVE UP SEMICOLON statement
  7. ⇒ MOVE UP SEMICOLON turn_stmt
  8. ⇒ MOVE UP SEMICOLON TURN direction SEMICOLON
  9. ⇒ MOVE UP SEMICOLON TURN RIGHT SEMICOLON
        """)
        
        print("Árvore de Derivação (formato ASCII):")
        print()
        tree = ParseTreeVisualizer.create_example_tree()
        ParseTreeVisualizer.print_tree_ascii(tree)
        print()
        print("="*70)
    
    @staticmethod
    def print_tokens_info():
        """Imprime informações sobre os tokens da linguagem"""
        print("\n" + "="*70)
        print("🔤 TOKENS UTILIZADOS NA ANÁLISE LÉXICA")
        print("="*70)
        
        tokens_info = {
            "Comandos do Robô": ["MOVE", "TURN", "PICK", "DROP"],
            "Estruturas de Controle": ["IF", "ELSE", "WHILE", "REPEAT", "TIMES"],
            "Operadores e Comparadores": ["ASSIGN (=)", "EQUALS (==)", "NOTEQUALS (!=)", 
                                          "LESS (<)", "GREATER (>)", "LESSEQUAL (<=)", "GREATEREQUAL (>=)"],
            "Direções": ["UP", "DOWN", "LEFT", "RIGHT"],
            "Operadores Aritméticos": ["PLUS (+)", "MINUS (-)", "MULTIPLY (*)", "DIVIDE (/)"],
            "Tipos e Literais": ["NUMBER", "IDENTIFIER", "STRING"],
            "Delimitadores": ["LBRACE ({)", "RBRACE (})", "LPAREN (()", "RPAREN ())", "SEMICOLON (;)", "COMMA (,)"],
        }
        
        for category, items in tokens_info.items():
            print(f"\n  {category}:")
            for item in items:
                print(f"    • {item}")
        
        print("\n" + "="*70)

# ===== FIM DAS MODIFICAÇÕES =====
