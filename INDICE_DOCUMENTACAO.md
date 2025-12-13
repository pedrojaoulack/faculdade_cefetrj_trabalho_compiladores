# 📚 Índice Completo da Documentação - RoboLang

## 📖 Guias Principais

### 1. [README.md](README.md) - Documentação Geral
**O que é:** Documentação completa do projeto e interpretador RoboLang
**Contém:**
- 📋 Visão geral do projeto
- 🌟 Lista de características
- 🚀 Instruções de instalação
- 💻 Guia de uso (modo interativo e arquivo)
- 📊 Análise léxica, sintática e semântica
- 🌳 Exemplos de árvores de derivação
- 🔧 Estrutura do projeto
- 📁 Exemplos de código
- ⚙️ Tecnologias utilizadas

**Para quem:** Desenvolvedores, estudantes, anyone wanting complete overview

---

### 2. [USANDO_DERIVACOES.md](USANDO_DERIVACOES.md) - Análise de Derivações ✨
**O que é:** Guia detalhado sobre como usar a análise real de derivações leftmost
**Contém:**
- 📊 O que são derivações leftmost
- 🌲 O que são árvores de derivação
- 💻 Como usar em modo REPL (interativo)
- 📁 Como usar com arquivos `.robo`
- 🧠 Explicação de cada parte da saída
- 📈 Exemplos práticos progressivos
- 🎓 Propósito educacional
- 🐛 Troubleshooting

**Para quem:** Estudantes de compiladores, pessoas aprendendo sobre parsing

**Comece aqui se:** Você quer entender como o compilador processa seu código

---

## 🎯 Recursos de Aprendizado

### Por Objetivo

#### "Quero entender como usar RoboLang"
1. Leia: [README.md - Características](README.md#-características)
2. Leia: [README.md - Uso](README.md#-uso)
3. Rode: `python main.py`
4. Tente: Digite `help` no REPL

#### "Quero aprender sobre compiladores"
1. Leia: [README.md - Documentação Técnica](README.md#-documentação-técnica)
2. Explore: `grammar`, `semantic`, `tokens` comandos no REPL
3. Leia: [USANDO_DERIVACOES.md](USANDO_DERIVACOES.md)
4. Rode: Exemplos e use o comando `derivation`

#### "Quero ver a verdadeira derivação de meu código"
1. Leia: [USANDO_DERIVACOES.md](USANDO_DERIVACOES.md) - Seção "Como Usar"
2. Execute seu código: `python main.py seu_programa.robo`
3. Ou em REPL: Execute código e depois use `derivation`

#### "Quero entender a estrutura de um compilador"
1. Leia: [README.md - Análise Léxica](README.md#1️⃣-análise-léxica-lexer)
2. Leia: [README.md - Análise Sintática](README.md#2️⃣-análise-sintática-parser)
3. Leia: [README.md - Análise Semântica](README.md#3️⃣-análise-semântica)
4. Estude: Os arquivos `lexer.py`, `parser.py`, `main.py`

---

## 📊 Comparação de Documentos

| Documento | Comprimento | Foco | Nível |
|-----------|-----------|------|-------|
| **README.md** | Longo (~30KB) | Visão geral completa | Iniciante → Avançado |
| **USANDO_DERIVACOES.md** | Médio (~8.5KB) | Derivações leftmost | Estudante/Compiladores |

---

## 🔑 Conceitos-Chave por Documento

### Em README.md encontrará:
- ✅ Sintaxe de RoboLang
- ✅ Tokens (33 tipos)
- ✅ Gramática livre de contexto completa
- ✅ 40 produções gramaticais
- ✅ Exemplos de árvores (estáticas)
- ✅ Classe RobotEnvironment
- ✅ Ações semânticas

### Em USANDO_DERIVACOES.md encontrará:
- ✅ O que é derivação leftmost
- ✅ O que é árvore de derivação
- ✅ **Como gerar derivações reais de seu código**
- ✅ Exemplos passo-a-passo
- ✅ Diferença entre não-terminal e terminal
- ✅ Troubleshooting

---

## 🎓 Plano de Aprendizado Recomendado

### Semana 1: Fundamentos
1. **Dia 1**: Leia [README.md - Características](README.md#-características)
2. **Dia 2**: Instale e execute `python main.py`
3. **Dia 3**: Estude [README.md - Tokens](README.md#tokens-definidos)
4. **Dia 4**: Explore os comandos `grammar` e `tokens` no REPL
5. **Dia 5**: Crie seus próprios programas `.robo`

### Semana 2: Análise Sintática
1. **Dia 1**: Leia [README.md - Gramática](README.md#gramática-livre-de-contexto)
2. **Dia 2**: Estude [README.md - Regras de Precedência](README.md#regras-de-precedência)
3. **Dia 3**: Use comando `semantic` no REPL
4. **Dia 4**: Estude a tabela de produções (P0-P39)
5. **Dia 5**: Comece a entender árvores sintáticas

### Semana 3: Derivações Leftmost ✨
1. **Dia 1**: Leia [USANDO_DERIVACOES.md - Visão Geral](USANDO_DERIVACOES.md#visão-geral)
2. **Dia 2**: Estude [USANDO_DERIVACOES.md - Entendendo a Saída](USANDO_DERIVACOES.md#entendendo-a-saída)
3. **Dia 3**: Rode exemplos simples e use `derivation`
4. **Dia 4**: Rode exemplos complexos e analise as derivações
5. **Dia 5**: Crie seus próprios exemplos e analise

---

## 🛠️ Referência Rápida

### Comandos REPL Mais Úteis para Aprendizado

```bash
python main.py              # Abre modo interativo

# No prompt robo>:
help                        # Mostra ajuda com todos os comandos
grammar                     # Exibe toda a gramática
semantic                    # Mostra tabela de produções
tokens                      # Lista os 33 tokens
tree                        # Mostra exemplo de árvore
derivation                  # ✨ Mostra derivação real do último código
status                      # Exibe estado do robô
```

### Exemplos Rápidos

```bash
# Modo arquivo
python main.py exemplo.robo              # Com derivação automática

# Modo interativo
python main.py
robo> move up;
robo> derivation                         # Ver a derivação
robo> sair
```

---

## 📝 Como Contribuir com Exemplos

Se você criar bons exemplos de derivações, considere:
1. Criar arquivo `exemploX.robo`
2. Documentar o comportamento esperado
3. Adicionar à seção de exemplos deste índice

---

## 🔗 Arquivos Relacionados

| Arquivo | Tipo | Propósito |
|---------|------|----------|
| `lexer.py` | Código | Análise léxica |
| `parser.py` | Código | Análise sintática e semântica |
| `main.py` | Código | Interface REPL e arquivo |
| `tree_visualizer.py` | Código | Captura e exibição de derivações |
| `exemplo.robo` | Exemplo | Programa teste básico |
| `parsetab.py` | Gerado | Tabela de parsing (auto-gerado) |
| `parser.out` | Gerado | Análise de parsing (auto-gerado) |

---

## 🎯 Checklist de Aprendizado

### Você aprendeu quando conseguir:

- [ ] Explicar o que é um token
- [ ] Listar os 33 tokens da linguagem
- [ ] Desenhar a árvore de sintaxe de `move up;`
- [ ] Escrever uma derivação leftmost manualmente
- [ ] Usar o comando `derivation` corretamente
- [ ] Entender a diferença entre não-terminal e terminal
- [ ] Explicar o que é uma "produção gramatical"
- [ ] Descrever as 3 fases de um compilador
- [ ] Escrever um programa `.robo` com 5+ instruções
- [ ] Analizar uma derivação complexa com estruturas de controle

---

## 💡 Dicas de Estudo

### Para Aprender Derivações:
1. **Comece simples**: `move up;` tem apenas 6 passos
2. **Aumente gradualmente**: Adicione mais comandos
3. **Estruturas de controle**: `if`, `while`, `repeat` têm derivações maiores
4. **Visualize**: Use o formato ASCII para entender a hierarquia

### Para Entender o Código:
1. **Leia comentários**: Procure por `# ===== MODIFICAÇÕES`
2. **Teste individualmente**: Rode cada exemplo separado
3. **Use os comandos**: `grammar`, `semantic`, `tokens` são seus amigos
4. **Estude casos de erro**: Tente código inválido para aprender

---

## 📞 Questões Frequentes

**P: Por onde começo?**
R: Comece com [README.md](README.md#-uso) e rode `python main.py`

**P: Como vejo a derivação do meu código?**
R: Leia [USANDO_DERIVACOES.md](USANDO_DERIVACOES.md#como-usar)

**P: Qual é a diferença entre árvore e derivação?**
R: Veja [USANDO_DERIVACOES.md - Entendendo a Saída](USANDO_DERIVACOES.md#entendendo-a-saída)

**P: Onde estão os arquivos de código?**
R: `lexer.py`, `parser.py`, `main.py` na raiz do projeto

**P: Posso criar meus próprios programas?**
R: Sim! Crie um arquivo `.robo` e execute com `python main.py seu_arquivo.robo`

---

## 📄 Histórico de Documentação

- **v1.0** (Inicial): Documentação básica em README.md
- **v2.0** (Atual): Adicionado USANDO_DERIVACOES.md e este índice
- **Futuro**: Mais exemplos, vídeos tutoriais, exercícios interativos

---

**Desenvolvido para fins educacionais** 🎓

Desenvolvido por: **Pedro Henrique Jaoulack de Carvalho** e **Flávio Silva Almeida**
CEFET-RJ - Compiladores 2025/2

---

*Última atualização: Dezembro 2024*
