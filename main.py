# main.py - Programa Principal do Interpretador RoboLang
from parser import parse, robot
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
""")

def run_file(filename):
    """Executa um arquivo .robo"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        print(f"📄 Executando arquivo: {filename}\n")
        parse(code)
    except FileNotFoundError:
        print(f"❌ Arquivo '{filename}' não encontrado!")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")

def run_interactive():
    """Modo interativo (REPL)"""
    print("💬 Modo Interativo (digite 'sair' para encerrar)")
    print("Digite 'help' para ver os comandos disponíveis\n")
    
    while True:
        try:
            line = input("robo> ")
            
            if line.strip().lower() == 'sair':
                print("👋 Até mais. Encerrando...")
                break
            elif line.strip().lower() == 'help':
                print_help()
                continue
            elif line.strip().lower() == 'status':
                print(f"📍 Posição: {robot.position}")
                print(f"🧭 Direção: {robot.direction}")
                print(f"🎒 Inventário: {robot.inventory}")
                print(f"💾 Variáveis: {robot.variables}")
                continue
            elif line.strip() == '':
                continue
                
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