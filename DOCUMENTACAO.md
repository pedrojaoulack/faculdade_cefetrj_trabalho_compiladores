# RoboLang - Interpretador de Linguagem para Controle de Robô Virtual

## 📋 Documentação do Projeto

### 1. **Gerador de Analisadores Escolhido**

- **Ferramenta**: PLY (Python Lex-Yacc)
- **Linguagem**: Python 3
- **Referência**: https://www.dabeaz.com/ply/
- **Descrição**: PLY é um gerador de analisadores léxicos (Lex) e sintáticos (Yacc) para Python, similar ao FLEX/BISON em C

### 2. **Estrutura do Projeto**

O projeto está organizado em três módulos principais:

#### **lexer.py** - Análise Léxica
- **Função**: Decompõe o código-fonte em tokens (símbolos terminais)
- **Arquivo do PLY**: `lex.lex()`
- **Tokens Definidos**: 40+ tipos (MOVE, TURN, PICK, DROP, IF, WHILE, etc.)
- **Expressões Regulares Utilizadas**:
  - `\d+(\.\d+)?` - Reconhece números inteiros e decimais
  - `"[^"]*"` - Reconhece strings entre aspas duplas
  - `[a-zA-Z_][a-zA-Z_0-9]*` - Reconhece identificadores e palavras-chave
  - `//.*` - Reconhece comentários de linha

#### **parser.py** - Análise Sintática e Semântica
- **Função**: Valida a estrutura gramatical e executa o código
- **Arquivo do PLY**: `yacc.yacc()`
- **Método de Análise**: LALR (Look-Ahead LR)
- **Tabelas Geradas**: Armazenadas em `parsetab.py`
- **Ações Semânticas**: 19 produções com ações de interpretação

#### **tree_visualizer.py** - Visualização de Estruturas
- **Função**: Exibe a gramática, tabelas semânticas e árvore de derivação
- **Conteúdo**: 
  - 19 regras gramaticais da linguagem
  - Tabela de produções com ações semânticas
  - Exemplo de derivação e árvore sintática

#### **main.py** - Interface do Interpretador
- **Modo Arquivo**: `python main.py exemplo.robo`
- **Modo Interativo**: `python main.py`
- **Comandos Interativos**: help, grammar, semantic, tree, tokens, status, sair

---

### 3. **Gramática da Linguagem RoboLang**

```
program → statement_list

statement_list → statement_list statement
               | statement

statement → move_stmt
          | turn_stmt
          | pick_stmt
          | drop_stmt
          | assign_stmt
          | if_stmt
          | while_stmt
          | repeat_stmt
          | block

move_stmt → MOVE direction SEMICOLON
turn_stmt → TURN direction SEMICOLON
pick_stmt → PICK STRING SEMICOLON
drop_stmt → DROP SEMICOLON

direction → UP | DOWN | LEFT | RIGHT

assign_stmt → IDENTIFIER ASSIGN expression SEMICOLON

if_stmt → IF LPAREN condition RPAREN block
        | IF LPAREN condition RPAREN block ELSE block

while_stmt → WHILE LPAREN condition RPAREN block
repeat_stmt → REPEAT expression TIMES block

block → LBRACE statement_list RBRACE

condition → expression EQUALS expression
          | expression NOTEQUALS expression
          | expression LESS expression
          | expression GREATER expression
          | expression LESSEQUAL expression
          | expression GREATEREQUAL expression

expression → expression PLUS expression
           | expression MINUS expression
           | expression MULTIPLY expression
           | expression DIVIDE expression
           | LPAREN expression RPAREN
           | NUMBER
           | IDENTIFIER
```

---

### 4. **Precedência de Operadores**

Definida em `parser.py` para resolver ambiguidades:

```python
precedence = (
    ('left', 'PLUS', 'MINUS'),           # Menor precedência
    ('left', 'MULTIPLY', 'DIVIDE'),      # Maior precedência
    ('nonassoc', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL'),
    ('nonassoc', 'EQUALS', 'NOTEQUALS'),
)
```

**Exemplo de Resolução**: `2 + 3 * 4` é avaliado como `2 + (3 * 4) = 14` (não como `(2+3)*4 = 20`)

---

### 5. **Tabela de Produções e Ações Semânticas**

| Produção | Ação Semântica |
|----------|----------------|
| `program → statement_list` | Inicia o programa e exibe posição final do robô |
| `move_stmt → MOVE direction SEMICOLON` | Executa movimento do robô usando `robot.move()` |
| `turn_stmt → TURN direction SEMICOLON` | Gira o robô para direção especificada |
| `pick_stmt → PICK STRING SEMICOLON` | Adiciona item ao inventário do robô |
| `drop_stmt → DROP SEMICOLON` | Remove item do inventário |
| `assign_stmt → IDENTIFIER ASSIGN expression SEMICOLON` | Atribui valor a variável: `robot.variables[id] = expr` |
| `if_stmt → IF LPAREN condition RPAREN block` | Executa bloco se condição verdadeira |
| `if_stmt → ... ELSE block` | Executa bloco alternativo se falsa |
| `while_stmt → WHILE LPAREN condition RPAREN block` | Executa bloco repetidamente |
| `repeat_stmt → REPEAT expression TIMES block` | Executa bloco N vezes |
| `condition → expression EQUALS expression` | Retorna `True` se `p[1] == p[3]` |
| `condition → expression LESS expression` | Retorna `True` se `p[1] < p[3]` |
| `expression → expression PLUS expression` | Retorna `p[1] + p[3]` |
| `expression → expression MINUS expression` | Retorna `p[1] - p[3]` |
| `expression → expression MULTIPLY expression` | Retorna `p[1] * p[3]` |
| `expression → expression DIVIDE expression` | Retorna `p[1] / p[3]` |
| `expression → NUMBER` | Retorna valor numérico |
| `expression → IDENTIFIER` | Retorna valor da variável da tabela de símbolos |

---

### 6. **Exemplo de Árvore de Derivação**

**Sentença de entrada**: `move up; turn right;`

**Derivação (Leftmost Derivation)**:
```
 1. program
 2. ⇒ statement_list
 3. ⇒ statement_list statement
 4. ⇒ move_stmt statement
 5. ⇒ MOVE direction SEMICOLON statement
 6. ⇒ MOVE UP SEMICOLON statement
 7. ⇒ MOVE UP SEMICOLON turn_stmt
 8. ⇒ MOVE UP SEMICOLON TURN direction SEMICOLON
 9. ⇒ MOVE UP SEMICOLON TURN RIGHT SEMICOLON
```

**Árvore de Derivação (formato ASCII)**:
```
program
└── statement_list
    ├── statement
    │   └── move_stmt
    │       ├── MOVE
    │       ├── direction
    │       │   └── UP
    │       └── SEMICOLON
    └── statement_list
        └── statement
            └── turn_stmt
                ├── TURN
                ├── direction
                │   └── RIGHT
                └── SEMICOLON
```

---

### 7. **Tokens Utilizados**

#### Comandos do Robô
- `MOVE`, `TURN`, `PICK`, `DROP`

#### Estruturas de Controle
- `IF`, `ELSE`, `WHILE`, `REPEAT`, `TIMES`

#### Operadores
- Aritmética: `PLUS (+)`, `MINUS (-)`, `MULTIPLY (*)`, `DIVIDE (/)`
- Comparação: `EQUALS (==)`, `NOTEQUALS (!=)`, `LESS (<)`, `GREATER (>)`, `LESSEQUAL (<=)`, `GREATEREQUAL (>=)`
- Atribuição: `ASSIGN (=)`

#### Direções
- `UP`, `DOWN`, `LEFT`, `RIGHT`

#### Tipos e Literais
- `NUMBER` (inteiros e decimais)
- `IDENTIFIER` (nomes de variáveis)
- `STRING` (texto entre aspas)

#### Delimitadores
- `LBRACE ({)`, `RBRACE (})`, `LPAREN (()`, `RPAREN ())`, `SEMICOLON (;)`, `COMMA (,)`

---

### 8. **Execução Exemplo**

**Código em RoboLang** (`exemplo.robo`):
```
contador = 0;
passos = 4;

pick "chave";
pick "mapa";

repeat passos times {
    move up;
    turn right;
    move right;
    contador = contador + 1;
}

if (contador == passos) {
    move down;
    drop;
}
```

**Saída da Execução**:
```
💾 Variável contador = 0
💾 Variável passos = 4
📦 Robô pegou: chave
📦 Robô pegou: mapa
🤖 Robô moveu para up. Posição atual: [0, 1]
🔄 Robô virou para right
🤖 Robô moveu para right. Posição atual: [1, 1]
💾 Variável contador = 1
💾 Variável x_pos = 4
🤖 Robô moveu para down. Posição atual: [1, 0]
📤 Robô soltou: mapa

✅ Programa executado com sucesso!
📍 Posição final do robô: [0, 0]
🧭 Direção final: right
🎒 Inventário: []

[GRAMÁTICA EXIBIDA]
[TABELA SEMÂNTICA EXIBIDA]
[ÁRVORE DE DERIVAÇÃO EXIBIDA]
```

---

### 9. **Modificações Realizadas no Código**

#### **lexer.py**
- ✅ Definição de 40+ tokens terminais
- ✅ Criação de 8 palavras reservadas
- ✅ Expressões regulares para números, strings, identificadores
- ✅ Regra para comentários de linha (`//`)
- ✅ Todos os operadores e delimitadores

#### **parser.py**
- ✅ Classe `RobotEnvironment` para estado do robô
- ✅ 19 produções gramaticais com ações semânticas
- ✅ Precedência de operadores definida
- ✅ Interpretação de comandos (MOVE, TURN, PICK, DROP)
- ✅ Processamento de expressões e variáveis
- ✅ Estruturas de controle (IF, WHILE, REPEAT)
- ✅ Tabela de símbolos para variáveis

#### **tree_visualizer.py** (NOVO)
- ✅ Classe `ParseTreeVisualizer` com funções estáticas
- ✅ Exibição da gramática completa
- ✅ Tabela de produções e ações semânticas
- ✅ Exemplo de derivação leftmost
- ✅ Árvore de derivação em formato ASCII

#### **main.py**
- ✅ Importação do visualizador
- ✅ Função `print_analysis_report()` para exibir análise
- ✅ Comandos interativos: `grammar`, `semantic`, `tree`, `tokens`
- ✅ Exibição automática da análise ao executar arquivo

---

### 10. **Como Usar**

#### Modo Arquivo
```bash
python main.py exemplo.robo
```

#### Modo Interativo
```bash
python main.py
```

**Comandos Disponíveis**:
- `move up/down/left/right;` - Move o robô
- `turn up/down/left/right;` - Gira o robô
- `pick "item";` - Pega um item
- `drop;` - Solta um item
- `x = 10;` - Atribui valor a variável
- `if (x > 5) { ... }` - Condicional
- `while (x < 10) { ... }` - Loop
- `repeat 5 times { ... }` - Repetição
- `grammar` - Mostra gramática
- `semantic` - Mostra tabela semântica
- `tree` - Mostra exemplo de árvore
- `tokens` - Mostra tokens disponíveis
- `status` - Mostra estado do robô
- `help` - Mostra ajuda
- `sair` - Encerra o programa

---

### 11. **Requisitos Atendidos**

✅ **Requisito 1**: Pesquisa sobre geradores de analisadores
- PLY (Python Lex-Yacc) documentado com referências

✅ **Requisito 2**: Baixar, executar e analisar exemplo
- Projeto executável com exemplos de teste

✅ **Requisito 3**: Modificar exemplo com definições, regras e ações
- Código comentado explicitamente com "MODIFICAÇÃO"
- Léxico: expressões regulares e palavras reservadas
- Sintático: 19 produções com ações semânticas
- Semântico: interpretação completa do código

✅ **Requisito 4a**: Informar o gerador escolhido
- PLY em Python documentado

✅ **Requisito 4b**: Apresentar modificações e inclusões
- Código-fonte com comentários descritivos

✅ **Requisito 4c**: Mostrar tabela de produções e ações semânticas
- Tabela completa em `tree_visualizer.py` e saída executável

✅ **Requisito 4d**: Mostrar árvore de derivação
- Exemplo de derivação leftmost
- Árvore em formato ASCII visualizável

✅ **Requisito 4e**: Apresentar exemplo executando o código
- Arquivo `exemplo.robo` com saída completa

✅ **Código de Usuário**: Criado interpretador funcional RoboLang

---

### 12. **Arquivos do Projeto**

- `lexer.py` - Analisador léxico (MODIFICADO)
- `parser.py` - Analisador sintático (MODIFICADO)
- `tree_visualizer.py` - Visualizador de estruturas (NOVO)
- `main.py` - Interface principal (MODIFICADO)
- `exemplo.robo` - Arquivo de exemplo em RoboLang
- `parsetab.py` - Tabelas LALR (gerado automaticamente)
- `parser.out` - Relatório de análise (gerado automaticamente)
- `DOCUMENTACAO.md` - Este arquivo

---

**Data**: Dezembro 2025  
**Autores**: Pedro Henrique e Flávio Silva  
**Instituição**: CEFET-RJ - Centro Federal de Educação Tecnológica Celso Suckow da Fonseca
