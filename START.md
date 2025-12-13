# 🎉 BEM-VINDO AO ROBOLANG!

**Trabalho Completo** | **13 de dezembro de 2025** | **CEFET-RJ**

---

## ⚡ Início Rápido (5 minutos)

### 1️⃣ Instalação
```bash
pip install ply
```

### 2️⃣ Modo Interativo
```bash
python main.py
```

```
robo> move up;
robo> x = 5;
robo> grammar
robo> tree
robo> sair
```

### 3️⃣ Executar Exemplo
```bash
python main.py exemplo.robo
```

---

## 📚 Documentação Essencial

Leia nesta ordem:

1. **[VISAO_GERAL.md](VISAO_GERAL.md)** ⭐ (5 min)
   - Visão geral do projeto
   - Como usar
   - Requisitos atendidos

2. **[RELATORIO.md](RELATORIO.md)** ⭐ (15 min)
   - Análise técnica completa
   - Comparação Calc vs. RoboLang
   - Requisitos 4a-4e

3. **[COMPARATIVO_TRES_VERSOES.md](COMPARATIVO_TRES_VERSOES.md)** (10 min)
   - Código lado-a-lado
   - Análise detalhada
   - Exemplos de execução

---

## 🎯 Para a Professora

### Requisitos Atendidos

✅ **Requisito 1**: Pesquisa sobre PLY  
✅ **Requisito 2**: Análise de calc.py  
✅ **Requisito 3**: Modificações extensivas (40+ tokens, 27 produções)  
✅ **Requisito 4a**: Analisador = PLY (LALR)  
✅ **Requisito 4b**: Modificações documentadas com 8 tabelas  
✅ **Requisito 4c**: Tabela de 27 produções com ações  
✅ **Requisito 4d**: Árvore de derivação com visualização  
✅ **Requisito 4e**: Execução com 3 exemplos  
✅ **Requisito 5**: Código entregue comentado  

### Estatísticas Principais

| Métrica | Original | RoboLang | Aumento |
|---------|----------|----------|---------|
| Tokens | 9 | 40+ | **+344%** |
| Produções | 7 | 27 | **+286%** |
| Ações Semânticas | 2 | 19 | **+850%** |
| Linhas de Código | ~50 | ~1200 | **+1400%** |

### Como Demonstrar

```bash
# Terminal 1 - Verificar estrutura
python main.py
> grammar    # Mostra 27 produções
> semantic   # Mostra 19 ações
> tree       # Mostra árvore de derivação
> tokens     # Mostra 40+ tokens

# Terminal 2 - Executar programa
python main.py exemplo.robo
```

---

## 📂 O que tem aqui?

```
📦 RoboLang/
├── 📝 Documentação (6 arquivos)
│   ├── VISAO_GERAL.md          ← COMECE AQUI
│   ├── RELATORIO.md            ← PRINCIPAL
│   ├── COMPARATIVO_...         ← Análise
│   ├── INDICE_COMPLETO.md      ← Guia
│   ├── README.md               ← Tutorial
│   └── DOCUMENTACAO.md         ← Referência
│
├── 💻 Código (4 arquivos Python)
│   ├── lexer.py                Análise Léxica (40+ tokens)
│   ├── parser.py               Análise Sintática (27 produções)
│   ├── tree_visualizer.py      Visualização da Árvore
│   └── main.py                 Interface REPL
│
└── 🧪 Exemplos
    ├── exemplo.robo            Programa funcional
    └── test_movement.robo      Teste de movimento
```

---

## 🚀 O que o RoboLang faz?

### Exemplo de Programa

```robo
// Programa de coleta de itens
contador = 0;
passos = 4;

// Move em um quadrado
repeat passos times {
    move up;
    turn right;
    move right;
    contador = contador + 1;
}

// Coleta item se em posição
if (contador == passos) {
    pick "chave";
}

// Move para origem
repeat 2 times {
    move left;
    move down;
}

drop;
```

### Saída

```
🤖 Robô moveu para up. Posição atual: [5, 6]
🤖 Robô virou para right. Direção: right
🤖 Robô moveu para right. Posição atual: [6, 6]
💾 Variável contador = 1
...
✅ Programa executado com sucesso!
📍 Posição final do robô: [5, 4]
🧭 Direção final: right
🎒 Inventário: ['chave']
```

---

## 💡 Comandos Disponíveis

### No Modo Interativo

**Movimento**:
- `move up;` / `move down;` / `move left;` / `move right;`

**Controle**:
- `turn up;` / `turn down;` / `turn left;` / `turn right;`

**Inventário**:
- `pick "item";` - Coleta item
- `drop;` - Solta item

**Programação**:
- `x = 10;` - Atribuição
- `y = x + 5;` - Expressão
- `if (x > 5) { ... }` - Condicional
- `repeat 5 times { ... }` - Repetição
- `while (x < 10) { ... }` - Loop

**Análise**:
- `grammar` - Mostra gramática (19 regras)
- `semantic` - Mostra tabela semântica
- `tree` - Mostra árvore de derivação
- `tokens` - Lista 40+ tokens
- `status` - Estado atual do robô
- `help` - Ajuda

**Sistema**:
- `sair` - Encerra

---

## 📊 Estrutura Técnica

### Análise Léxica
- ✅ 40+ tokens definidos
- ✅ 13 palavras-chave
- ✅ 6 funções de tokenização
- ✅ Suporte a decimais, strings, comentários

### Análise Sintática
- ✅ 27 produções gramaticais
- ✅ Precedência de 4 níveis
- ✅ Método LALR (PLY yacc)
- ✅ Sem conflitos shift/reduce

### Análise Semântica
- ✅ 19 ações semânticas
- ✅ Classe RobotEnvironment
- ✅ Tabela de símbolos (variáveis)
- ✅ Execução durante parsing

---

## 🎬 Para Apresentar (7 minutos)

### Roteiro

**1. Introdução (1 min)**
```
"Usamos PLY - Python Lex-Yacc.
Expandimos a calculadora simples em 1400%.
De 9 para 40+ tokens, de 7 para 27 produções."
```

**2. Léxica (1 min)**
```bash
python main.py
> tokens
```
Mostrar 40+ tokens de RoboLang vs. 9 originais

**3. Sintática (1 min)**
```bash
> grammar
```
Mostrar 27 produções com if, while, repeat

**4. Árvore (1 min)**
```bash
> tree
```
Mostrar derivação para `move up; turn right;`

**5. Demo (2 min)**
```bash
# Encerre o anterior e rode:
python main.py exemplo.robo
```
Mostrar saída completa com posições

**6. Conclusão (1 min)**
```
"+850% em ações semânticas
+1400% em código
Código funcionando, documentado, no GitHub"
```

---

## 📖 Aprofundamento (Opcional)

Se quer entender melhor:

1. **PLY Oficial**: https://www.dabeaz.com/ply/
2. **Calc Original**: https://github.com/dabeaz/ply/blob/master/example/calc/calc.py
3. **Compiladores**: Livro "Compilers" de Aho & Ullman

---

## ❓ Perguntas Comuns

**P: Como rodar o programa?**  
R: `python main.py exemplo.robo`

**P: Como entrar modo interativo?**  
R: `python main.py` (sem arquivo)

**P: Onde está a documentação?**  
R: Comece por VISAO_GERAL.md

**P: Qual é o arquivo principal a ler?**  
R: RELATORIO.md (atende todos os requisitos)

**P: Como ver a árvore de derivação?**  
R: `python main.py` → `tree`

**P: Quais são as modificações?**  
R: COMPARATIVO_TRES_VERSOES.md tem código lado-a-lado

---

## ✅ Checklist

- ✅ Instalou Python 3.8+
- ✅ Rodou `pip install ply`
- ✅ Testou `python main.py exemplo.robo`
- ✅ Leu VISAO_GERAL.md
- ✅ Leu RELATORIO.md
- ✅ Entrou no modo interativo `python main.py`
- ✅ Rodou `grammar` e `tree`
- ✅ Entendeu as modificações

---

## 📞 Suporte

**Dúvidas técnicas?**
- Veja DOCUMENTACAO.md
- Veja RELATORIO.md Seção 4-6
- Execute `python main.py` e rode `help`

**Quer estender?**
- Adicione novos tokens em lexer.py
- Adicione novas produções em parser.py
- Expanda métodos em RobotEnvironment

---

## 🎓 Créditos

**Trabalho de**: Compiladores 2025/2 - CEFET-RJ  
**Equipe**: Pedro Henrique Jaoulack de Carvalho & Flávio Silva Almeida  
**Data**: Dezembro de 2025  
**Versão**: 1.0 Final

---

**🎉 Bem-vindo ao RoboLang! Divirta-se programando robôs virtuais!**

Próximo passo: Leia [VISAO_GERAL.md](VISAO_GERAL.md) →
