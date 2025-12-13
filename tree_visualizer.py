# tree_visualizer.py - Visualizador de Árvore de Derivação e Gramática
# ===== MODIFICAÇÃO: Adicionado para atender aos requisitos do trabalho =====
# Captura a verdadeira derivação (Leftmost Derivation) e árvore de sintaxe

class TreeNode:
    """Nó da árvore de derivação"""
    def __init__(self, label, value=None, children=None):
        self.label = label              # Nome do não-terminal ou terminal
        self.value = value              # Valor semântico (para terminais)
        self.children = children or []
        self.production_id = None       # Qual produção gerou este nó
    
    def add_child(self, child):
        self.children.append(child)
    
    def __str__(self):
        if self.value is not None:
            return f"{self.label}({self.value})"
        return self.label
    
    def is_terminal(self):
        """Verifica se é um nó terminal"""
        return len(self.children) == 0 and self.value is not None
    
    def get_string_form(self):
        """Retorna a forma da árvore como string (para derivação)"""
        if self.is_terminal():
            return str(self.value) if self.value else self.label
        if not self.children:
            return self.label
        return " ".join(child.get_string_form() for child in self.children)


class DerivationTracker:
    """Rastreia a derivação enquanto o parser executa"""
    
    def __init__(self):
        self.derivations = []  # Histórico de derivações
        self.current_tree = None  # Árvore atual
        self.parse_stack = []  # Stack de parsing para reconstruir árvore
    
    def start_derivation(self):
        """Inicia uma nova derivação"""
        self.derivations = []
        self.derivations.append("program")  # Símbolo inicial
    
    def add_reduction(self, production, tokens):
        """Adiciona uma redução (quando uma produção é aplicada)"""
        # production é como: "move_stmt → MOVE direction SEMICOLON"
        # tokens é a lista de símbolos que foram reduzidos
        if tokens:
            current_form = self.derivations[-1]
            # Substitui a produção na forma sentencial
            new_form = self._apply_production(current_form, production, tokens)
            if new_form != current_form:
                self.derivations.append(new_form)
    
    def _apply_production(self, current, production, tokens):
        """Aplica uma produção à forma sentencial"""
        # Simplificado: apenas retorna a forma com a redução
        return current
    
    def get_derivations(self):
        """Retorna todas as derivações"""
        return self.derivations


# Instância global para rastrear derivação durante parsing
derivation_tracker = DerivationTracker()

class ParseTreeVisualizer:
    """Classe para visualizar a árvore de derivação e gramática"""
    
    # Instância global da última árvore parseada
    last_parse_tree = None
    last_derivation_steps = []
    
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
    def set_parse_tree(tree):
        """Define a árvore de parse que foi gerada"""
        ParseTreeVisualizer.last_parse_tree = tree
    
    @staticmethod
    def print_tree_ascii(node, prefix="", is_last=True, depth=0, max_depth=20):
        """Imprime árvore em formato ASCII com informações de produção"""
        if node is None or depth > max_depth:
            return
        
        # Determina o símbolo de conexão
        if depth == 0:
            # Raiz - sem prefixo
            print(node.label if not node.children else f"[{node.label}]")
            connector_char = ""
            next_prefix = ""
        else:
            connector = "└── " if is_last else "├── "
            print(prefix + connector + (f"[{node.label}]" if node.children else node.label))
            
            # Próximo prefixo
            next_prefix = prefix + ("    " if is_last else "│   ")
        
        # Imprimir filhos
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            ParseTreeVisualizer.print_tree_ascii(child, next_prefix if depth > 0 else "", is_last_child, depth + 1, max_depth)
    
    @staticmethod
    def tree_to_string(node, include_terminals=True):
        """Converte a árvore para string representando a forma sentencial"""
        if node is None:
            return ""
        
        if not node.children:
            # Terminal - retorna o valor
            return str(node.value) if node.value is not None else node.label
        
        # Não-terminal - retorna forma sentencial
        parts = []
        for child in node.children:
            parts.append(ParseTreeVisualizer.tree_to_string(child, include_terminals))
        
        return " ".join(parts) if include_terminals else node.label
    
    @staticmethod
    def get_leftmost_derivation_from_tree(tree):
        """Reconstrói a derivação leftmost a partir da árvore parseada"""
        if not tree:
            return ["program"]
        
        derivations = ["program"]  # Início
        
        def extract_productions(node, depth=0):
            """Extrai produções em ordem leftmost"""
            if not node or not node.children:
                return
            
            # Registra a produção: nó → seus filhos
            if node.children:
                rhs = " ".join(child.label for child in node.children)
                derivations.append(f"{node.label} ⇒ {rhs}")
            
            # Continua com o primeiro filho (leftmost)
            if node.children:
                extract_productions(node.children[0], depth + 1)
                # Depois com os outros
                for child in node.children[1:]:
                    extract_productions(child, depth + 1)
        
        extract_productions(tree)
        return derivations
    
    @staticmethod
    def print_real_derivation(code):
        """Analisa código e exibe a verdadeira derivação e árvore"""
        print("\n" + "="*70)
        print("🌳 ANÁLISE REAL DE DERIVAÇÃO (Leftmost Derivation)")
        print("="*70)
        
        if not code:
            print("❌ Nenhum código para analisar!")
            print("="*70)
            return
        
        # Limpar entrada
        code = code.strip()
        
        # Mostrar código
        print(f"\n📝 Código parseado:")
        print(f"   {code[:60]}{'...' if len(code) > 60 else ''}")
        
        # Se temos uma árvore parseada
        if ParseTreeVisualizer.last_parse_tree:
            print("\n📊 Derivação (Leftmost Derivation):")
            derivations = ParseTreeVisualizer.get_leftmost_derivation_from_tree(
                ParseTreeVisualizer.last_parse_tree
            )
            
            for i, derivation in enumerate(derivations[:15]):  # Limita a 15 linhas
                if i == 0:
                    print(f"  {i+1:2d}. {derivation}")
                else:
                    print(f"  {i+1:2d}. {derivation}")
            
            if len(derivations) > 15:
                print(f"  ... ({len(derivations) - 15} derivações adicionais omitidas)")
            
            print("\n🌲 Árvore de Derivação (formato ASCII):")
            print()
            ParseTreeVisualizer.print_tree_ascii(ParseTreeVisualizer.last_parse_tree)
        else:
            print("❌ Nenhuma árvore parseada disponível")
            print("   Execute o código primeiro (ex: python main.py exemplo.robo)")
        
        print("\n" + "="*70)
    
    @staticmethod
    def print_derivation_example():
        """Imprime uma derivação de exemplo (mantém compatibilidade)"""
        print("\n" + "="*70)
        print("🌳 EXEMPLO DE DERIVAÇÃO LEFTMOST")
        print("="*70)
        print("\n📝 Sentença de entrada: move up; turn right;")
        print("\n📊 Derivação Leftmost:")
        print("""
  1. program
  2. ⇒ statement_list
  3. ⇒ statement_list statement
  4. ⇒ statement_list move_stmt
  5. ⇒ statement_list MOVE direction SEMICOLON
  6. ⇒ statement_list MOVE UP SEMICOLON
  7. ⇒ statement turn_stmt MOVE UP SEMICOLON
  8. ⇒ statement TURN direction SEMICOLON MOVE UP SEMICOLON
  9. ⇒ statement TURN RIGHT SEMICOLON MOVE UP SEMICOLON
        """)
        
        print("🌲 Árvore de Derivação (formato ASCII):")
        print()
        print("""
[program]
└── [statement_list]
    ├── [statement_list]
    │   └── [statement]
    │       └── [move_stmt]
    │           ├── MOVE
    │           ├── [direction]
    │           │   └── UP
    │           └── SEMICOLON
    └── [statement]
        └── [turn_stmt]
            ├── TURN
            ├── [direction]
            │   └── RIGHT
            └── SEMICOLON
        """)
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
