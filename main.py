# main.py - Programa Principal do Interpretador RoboLang
# ===== MODIFICAÇÕES: Adicionadas visualizações de árvore, gramática e tabelas semânticas =====
from parser import parse, robot
from tree_visualizer import ParseTreeVisualizer
import sys


def print_banner():
    print("=" * 60)
    print("🤖 RoboLang Interpreter v1.0")
    print("=" * 60)
    print("Linguagem de programação para controle de Robô virtual")
    print("Desenvolvido por Pedro Henrique e Flávio Silva")
    print("=" * 60)
    print()


def print_help():
    print("""
📚 COMANDOS DISPONÍVEIS:

    Movimento:
    - move up/down/left/right;      // Move o robô
    - turn up/down/left/right;      // Gira o robô

    Inventário:
    - pick "item";                  // Pega um item
    - drop;                         // Solta um item

    Variáveis:
    - x = 10;                       // Atribui valor
    - y = x + 5;                    // Expressões

    Controle:
    - if (x > 5) { ... }           // Condicional
    - if (x == 0) { ... } else { ... }
    - while (x < 10) { ... }       // Loop
    - repeat 5 times { ... }       // Repetição

    Operadores:
    - Aritméticos: +, -, *, /
    - Comparação: ==, !=, <, >, <=, >=

    Comentários: // comentário

    Comandos REPL:
    - grammar                       // Mostra gramática da linguagem
    - semantic                      // Mostra tabela semântica
    - tree                          // Mostra exemplo de árvore
    - derivation                    // ✨ NOVO: Mostra verdadeira derivação do último código
    - tokens                        // Mostra tokens disponíveis
    - status                        // Mostra estado do robô
""")


# ===== MODIFICAÇÃO: Função para exibir relatório de análise =====
def print_analysis_report():
    """Exibe gramática, tabelas semânticas e árvore de derivação"""
    print("\n" + "🔍 ANÁLISE LÉXICA E SINTÁTICA CONCLUÍDA".center(70))

    # Exibir gramática
    ParseTreeVisualizer.print_grammar()

    # Exibir tokens
    ParseTreeVisualizer.print_tokens_info()

    # Exibir tabela semântica
    ParseTreeVisualizer.print_semantic_table()

    # Exibir exemplo de derivação
    ParseTreeVisualizer.print_derivation_example()


def run_file(filename):
    """Executa um arquivo .robo"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        print(f"📄 Executando arquivo: {filename}\n")
        parse(code)
        # ===== MODIFICAÇÃO: Exibir gramática e árvore após execução =====
        print_analysis_report()
    except FileNotFoundError:
        print(f"❌ Arquivo '{filename}' não encontrado!")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")


def run_interactive():
    """Modo interativo (REPL)"""
    print("💬 Modo Interativo (digite 'sair' para encerrar)")
    print("Digite 'help' para ver os comandos disponíveis\n")

    last_code = ""  # Armazena último código executado

    while True:
        try:
            line = input("robo> ")

            if line.strip().lower() == 'sair':
                print("👋 Até mais. Encerrando...")
                break
            elif line.strip().lower() == 'help':
                print_help()
                continue
            # ===== MODIFICAÇÃO: Adicionar comandos para visualizar análise =====
            elif line.strip().lower() == 'grammar':
                ParseTreeVisualizer.print_grammar()
                continue
            elif line.strip().lower() == 'semantic':
                ParseTreeVisualizer.print_semantic_table()
                continue
            elif line.strip().lower() == 'tree':
                # ===== MODIFICAÇÃO: Mostrar verdadeira derivação em vez de exemplo =====
                if last_code:
                    ParseTreeVisualizer.print_real_derivation(last_code)
                else:
                    ParseTreeVisualizer.print_derivation_example()
                continue
            elif line.strip().lower() == 'derivation':  # ===== NOVO =====
                if last_code:
                    ParseTreeVisualizer.print_real_derivation(last_code)
                else:
                    print("❌ Nenhum código executado ainda!")
                    print("   Execute algum código primeiro (ex: move up;)")
                continue
            elif line.strip().lower() == 'tokens':
                ParseTreeVisualizer.print_tokens_info()
                continue
            elif line.strip().lower() == 'status':
                print(f"📍 Posição: {robot.position}")
                print(f"🧭 Direção: {robot.direction}")
                print(f"🎒 Inventário: {robot.inventory}")
                print(f"💾 Variáveis: {robot.variables}")
                continue
            elif line.strip() == '':
                continue

            # ===== MODIFICAÇÃO: Armazenar código para análise de derivação =====
            last_code = line
            parse(line)
        except KeyboardInterrupt:
            print("\n👋 Até mais. Encerrando...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

def main():
    print_banner()

    if len(sys.argv) > 1:
        # Modo arquivo
        run_file(sys.argv[1])
    else:
        # Modo interativo
        run_interactive()


if __name__ == '__main__':
    main()
