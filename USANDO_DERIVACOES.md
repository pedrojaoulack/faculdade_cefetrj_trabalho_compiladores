# 🌳 Guia: Usando Análise de Derivações no RoboLang

## Visão Geral

O interpretador RoboLang agora captura **verdadeiras derivações leftmost** do seu código, mostrando:
- 📊 A sequência de passos de derivação (production rules aplicadas)
- 🌲 A árvore de sintaxe em formato ASCII
- 🔍 Análise completa de como seu programa foi parseado

## Como Usar

### 1️⃣ Modo Interativo (REPL)

Abra o interpretador e execute um comando seguido de `derivation`:

```bash
python main.py
```

Exemplo de sessão:

```
robo> move up;
🤖 Robô moveu para up. Posição atual: [5, 6]
✅ Programa executado com sucesso!

robo> derivation
🌳 ANÁLISE REAL DE DERIVAÇÃO (Leftmost Derivation)
📝 Código parseado: move up;

📊 Derivação (Leftmost Derivation):
   1. program
   2. program ⇒ statement_list
   3. statement_list ⇒ statement
   4. statement ⇒ move_stmt
   5. move_stmt ⇒ MOVE direction SEMICOLON
   6. direction ⇒ up

🌲 Árvore de Derivação (formato ASCII):

[program]
└── [statement_list]
    └── [statement]
        └── [move_stmt]
            ├── MOVE
            ├── [direction]
            │   └── up
            └── SEMICOLON
```

### 2️⃣ Modo Arquivo

Ao executar um arquivo `.robo`, o interpretador automaticamente exibe a derivação:

```bash
python main.py exemplo.robo
```

Exemplo de saída (para `move up; turn right;`):

```
🌳 ANÁLISE REAL DE DERIVAÇÃO (Leftmost Derivation)

📝 Código parseado: move up; turn right;

📊 Derivação (Leftmost Derivation):
   1. program
   2. program ⇒ statement_list
   3. statement_list ⇒ statement_list statement
   4. statement_list ⇒ statement_list move_stmt
   5. statement_list ⇒ statement_list MOVE direction SEMICOLON
   6. statement_list ⇒ statement_list MOVE up SEMICOLON
   7. statement_list statement ⇒ statement_list move_stmt MOVE up SEMICOLON
   8. statement_list ⇒ statement_list turn_stmt
   ... (mais derivações)

🌲 Árvore de Derivação (formato ASCII):

[program]
└── [statement_list]
    ├── [statement_list]
    │   └── [statement]
    │       └── [move_stmt]
    │           ├── MOVE
    │           ├── [direction]
    │           │   └── up
    │           └── SEMICOLON
    └── [statement]
        └── [turn_stmt]
            ├── TURN
            ├── [direction]
            │   └── RIGHT
            └── SEMICOLON
```

## Entendendo a Saída

### 📊 Derivação Leftmost

Uma **derivação leftmost** mostra passo a passo como o parser reduz seu código até o símbolo inicial `program`.

Cada linha representa uma etapa:

```
1. program                              ← Começamos aqui
2. program ⇒ statement_list             ← Aplicamos regra: program → statement_list
3. statement_list ⇒ statement           ← Aplicamos regra: statement_list → statement
4. statement ⇒ move_stmt                ← Aplicamos regra: statement → move_stmt
5. move_stmt ⇒ MOVE direction SEMICOLON ← Aplicamos regra: move_stmt → MOVE direction SEMICOLON
6. direction ⇒ up                       ← Aplicamos regra: direction → up (terminal)
```

### 🌲 Árvore de Derivação

A árvore mostra a **estrutura hierárquica** do seu programa:

```
[program]                    ← Símbolo inicial
└── [statement_list]         ← Contém uma lista de statements
    └── [statement]          ← Um único statement
        └── [move_stmt]      ← É um movimento (move_stmt)
            ├── MOVE         ← Token: MOVE
            ├── [direction]  ← Não-terminal: direção
            │   └── up       ← Token: up
            └── SEMICOLON    ← Token: ;
```

**Notação:**
- `[label]` = Não-terminal (regra da gramática)
- `label` = Terminal (token/palavra-chave)

## Comandos REPL Relacionados

| Comando | Descrição |
|---------|-----------|
| `derivation` | ✨ Mostra verdadeira derivação do último código executado |
| `grammar` | Mostra toda a gramática de RoboLang |
| `semantic` | Mostra tabela de produções e ações semânticas |
| `tree` | Mostra exemplo de árvore (modo compatibilidade) |
| `tokens` | Lista todos os tokens da linguagem |
| `status` | Exibe estado atual do robô (posição, orientação, inventário) |

## Exemplos Práticos

### Exemplo 1: Movimento Simples

**Código:**
```robo
move right;
```

**Derivação:**
```
1. program
2. ⇒ statement_list
3. ⇒ statement
4. ⇒ move_stmt
5. ⇒ MOVE direction SEMICOLON
6. ⇒ right
```

### Exemplo 2: Múltiplos Comandos

**Código:**
```robo
move up;
turn left;
```

**Árvore:**
```
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
            │   └── LEFT
            └── SEMICOLON
```

Observe a **estrutura recursiva** de `statement_list`:
- Um `statement_list` pode conter outro `statement_list` + um `statement`
- Isso permite múltiplos comandos

### Exemplo 3: Bloco de Código

**Código:**
```robo
repeat 3 times {
  move forward;
  turn right;
}
```

**Árvore (simplificada):**
```
[program]
└── [statement_list]
    └── [statement]
        └── [repeat_stmt]
            ├── REPEAT
            ├── [expression]
            │   └── 3
            ├── TIMES
            └── [block]
                ├── LBRACE {
                ├── [statement_list]
                │   ├── [move_stmt]...
                │   └── [turn_stmt]...
                └── RBRACE }
```

## Propósito Educacional

As derivações ajudam a:

✅ **Entender parsing**: Veja como o compilador interpreta seu código
✅ **Aprender gramática**: Observe quais regras foram aplicadas
✅ **Debugar problemas**: Se algo não foi parseado corretamente, veja onde falhou
✅ **Compreender estrutura**: Visualize hierarquia de seu programa

## Conceitos-Chave

### Não-Terminal vs Terminal

| Tipo | Símbolo | Exemplos |
|------|---------|----------|
| **Não-Terminal** | `[label]` | `[program]`, `[statement_list]`, `[move_stmt]` |
| **Terminal** | Sem colchetes | `MOVE`, `TURN`, `up`, `;` |

Não-terminais correspondem a **regras gramaticais**.
Terminais correspondem a **palavras-chave e tokens**.

### Leftmost Derivation

A "leftmost" significa que **sempre expandimos o não-terminal mais à esquerda** primeiro:

```
program
⇒ statement_list          ← Expandimos "program" (único, à esquerda)
⇒ statement_list statement ← Expandimos primeiro "statement_list" (mais à esquerda)
⇒ move_stmt statement      ← Expandimos "move_stmt" (agora é o mais à esquerda)
...
```

## Troubleshooting

### "Nenhuma árvore parseada disponível"

**Causa:** Você usou `derivation` sem executar código antes.

**Solução:** Execute um comando primeiro, depois use `derivation`:
```
robo> move up;     ← Execute algo
robo> derivation   ← Então peça a derivação
```

### Derivação muito longa

Se o programa é complexo, a derivação pode ter muitas linhas. 
O sistema mostra as primeiras 15 linhas e indica quantas foram omitidas.

### Caracteres especiais não aparecem

Algumas árvores usam caracteres Unicode (└, ├, │, →, ⇒).
Se não aparecerem corretamente, seu terminal pode não suportar UTF-8.

**Solução:** Use um terminal moderno (Windows Terminal, VS Code Terminal, etc.)

## Implementação Técnica

Os componentes responsáveis:

- **`tree_visualizer.py`**: Captura árvores de parsing e reconstrói derivações
- **`parser.py`**: Cria `TreeNode` durante o parsing
- **`main.py`**: Fornece comando REPL `derivation` para exibir análise

A classe `ParseTreeVisualizer` fornece:
- `set_parse_tree()`: Armazena árvore após parsing
- `get_leftmost_derivation_from_tree()`: Reconstrói derivação
- `print_real_derivation()`: Formata e exibe análise
- `print_tree_ascii()`: Renderiza árvore em ASCII

---

**Desenvolvido para fins educacionais** 🎓

Veja também:
- [README.md](README.md) - Documentação geral
- [RELATORIO.md](RELATORIO.md) - Relatório técnico detalhado
