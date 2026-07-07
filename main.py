"""
Relógio da Fala — Main
Linguagem de Comunicação Alternativa e Aumentativa (CAA)

Ponto de entrada principal do aplicativo.
Permite executar testes, interface gráfica ou modo texto.
"""

import sys
import os

# Adicionar diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def modo_texto():
    """Modo interativo em texto (terminal)."""
    from gramatica import POSICOES_PLACA, COMBINACOES_VALIDAS
    from scanner import escanear_frase
    from parser import Parser

    print("=" * 60)
    print("RELÓGIO DA FALA — Modo Texto")
    print("=" * 60)
    print("\nComandos:")
    print("  Digite uma frase para validar")
    print("  'símbolos' — listar símbolos da placa")
    print("  'combinações' — listar combinações válidas")
    print("  'sair' — encerrar")
    print()

    while True:
        try:
            entrada = input("Relógio> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando...")
            break

        if not entrada:
            continue

        if entrada.lower() == "sair":
            break

        if entrada.lower() == "símbolos" or entrada.lower() == "simbolos":
            print("\nSímbolos da placa:")
            for pos, info in POSICOES_PLACA.items():
                print(f"  Posição {pos:2d}: {info['simbolo']:10s} [{info['categoria']}]")
            print()
            continue

        if entrada.lower() == "combinações" or entrada.lower() == "combinacoes":
            print("\nCombinações válidas:")
            for (s1, s2), frase in COMBINACOES_VALIDAS.items():
                print(f"  {s1:8s} + {s2:8s} → {frase}")
            print()
            continue

        # Validar frase
        try:
            tokens = escanear_frase(entrada)
            print(f"  Tokens: {tokens}")

            parser = Parser(tokens)
            parser.parse_frase()
            print("  Resultado: Frase VÁLIDA ✓\n")

        except RuntimeError as e:
            print(f"  Erro léxico: {e}\n")

        except SyntaxError as e:
            print(f"  Erro de sintaxe: {e}\n")


def modo_testes():
    """Executa a bateria de testes."""
    from testes.testar_tudo import (
        testar_scanner,
        testar_parser,
        testar_gramatica,
        testar_integracao,
    )

    print("Executando testes...\n")
    testar_scanner()
    testar_parser()
    testar_gramatica()
    testar_integracao()


def modo_interface():
    """Inicia a interface gráfica."""
    from interface import RelogioDaFala

    print("Iniciando interface gráfica...")
    app = RelogioDaFala()
    app.executar()


def main():
    """Função principal com menu de opções."""
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        if comando == "testes":
            modo_testes()
        elif comando == "interface" or comando == "gui":
            modo_interface()
        elif comando == "texto":
            modo_texto()
        else:
            print(f"Comando desconhecido: {comando}")
            print("Uso: python main.py [testes|interface|texto]")
    else:
        print("=" * 60)
        print("RELÓGIO DA FALA")
        print("Linguagem de CAA com Dois Ponteiros")
        print("=" * 60)
        print("\nOpções:")
        print("  1. Modo Texto (interativo)")
        print("  2. Executar Testes")
        print("  3. Interface Gráfica")
        print("  0. Sair")

        try:
            opcao = input("\nEscolha: ").strip()
        except (EOFError, KeyboardInterrupt):
            return

        if opcao == "1":
            modo_texto()
        elif opcao == "2":
            modo_testes()
        elif opcao == "3":
            modo_interface()
        else:
            print("Encerrando...")


if __name__ == "__main__":
    main()
