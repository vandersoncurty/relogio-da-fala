"""
Testes — Relógio da Fala
Linguagem de Comunicação Alternativa e Aumentativa (CAA)

Bateria de testes para validar o scanner, parser e gramática.
"""

import sys
import os

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gramatica import obter_frase, listar_simbolos, listar_combinacoes, POSICOES_PLACA
from scanner import escanear_frase
from parser import Parser


# ============================================================
# TESTES DO SCANNER
# ============================================================

def testar_scanner():
    """Testa o analisador léxico."""
    print("=" * 60)
    print("TESTES DO SCANNER")
    print("=" * 60)

    testes = [
        ("Eu quero agua", True),
        ("Eu quero comida", True),
        ("sim", True),
        ("n", True),
        ("triste ajuda", True),
        ("dor banheiro", True),
        ("feliz comer", True),
        ("preciso banheiro", True),
        ("Eu comer", True),
        ("Eu beber", True),
    ]

    passaram = 0
    total = len(testes)

    for entrada, esperado in testes:
        try:
            tokens = escanear_frase(entrada)
            if esperado:
                print(f"  ✓ '{entrada}' → {tokens}")
                passaram += 1
            else:
                print(f"  ✗ '{entrada}' → Era esperado erro")
        except RuntimeError as e:
            if not esperado:
                print(f"  ✓ '{entrada}' → Erro correto: {e}")
                passaram += 1
            else:
                print(f"  ✗ '{entrada}' → Erro inesperado: {e}")

    print(f"\nResultado: {passaram}/{total} testes passaram")
    return passaram == total


# ============================================================
# TESTES DO PARSER
# ============================================================

def testar_parser():
    """Testa o analisador sintático."""
    print("\n" + "=" * 60)
    print("TESTES DO PARSER")
    print("=" * 60)

    validas = [
        "Eu quero agua",
        "Eu quero comida",
        "Eu preciso banheiro",
        "Eu quero sair",
        "sim",
        "n",
        "triste ajuda",
        "dor banheiro",
        "feliz comer",
        "Eu comer",
        "Eu beber",
    ]

    invalidas = [
        "quero Eu",
        "agua comida",
        "sair banheiro",
    ]

    passaram = 0
    total = len(validas) + len(invalidas)

    print("\n  >>> VÁLIDAS <<<")
    for frase in validas:
        try:
            tokens = escanear_frase(frase)
            parser = Parser(tokens)
            parser.parse_frase()
            print(f"  ✓ '{frase}' → Válida")
            passaram += 1
        except SyntaxError as e:
            print(f"  ✗ '{frase}' → Erro: {e}")

    print("\n  >>> INVÁLIDAS <<<")
    for frase in invalidas:
        try:
            tokens = escanear_frase(frase)
            parser = Parser(tokens)
            parser.parse_frase()
            print(f"  ✗ '{frase}' → Era esperado erro sintático")
        except SyntaxError:
            print(f"  ✓ '{frase}' → Erro correto")
            passaram += 1

    print(f"\nResultado: {passaram}/{total} testes passaram")
    return passaram == total


# ============================================================
# TESTES DA GRAMÁTICA
# ============================================================

def testar_gramatica():
    """Testa a gramática e combinações."""
    print("\n" + "=" * 60)
    print("TESTES DA GRAMÁTICA")
    print("=" * 60)

    print("\nSímbolos da placa:")
    listar_simbolos()

    print("\nCombinações válidas:")
    listar_combinacoes()

    # Testar função obter_frase
    print("\nTeste de obter_frase():")
    testes_frase = [
        (1, 5, "Eu quero"),
        (1, 9, "Eu quero água"),
        (14, 16, "Estou triste, preciso de ajuda"),
        (15, 16, "Estou com dor, preciso de ajuda"),
        (1, 1, "Combinação não reconhecida"),
    ]

    passaram = 0
    total = len(testes_frase)

    for pos1, pos2, esperado in testes_frase:
        resultado = obter_frase(pos1, pos2)
        if esperado in resultado:
            print(f"  ✓ Pos({pos1},{pos2}) → '{resultado}'")
            passaram += 1
        else:
            print(f"  ✗ Pos({pos1},{pos2}) → '{resultado}' (esperado: '{esperado}')")

    print(f"\nResultado: {passaram}/{total} testes passaram")
    return passaram == total


# ============================================================
# TESTE DE INTEGRAÇÃO
# ============================================================

def testar_integracao():
    """Testa a integração scanner → parser → gramática."""
    print("\n" + "=" * 60)
    print("TESTE DE INTEGRAÇÃO")
    print("=" * 60)

    frases = [
        "Eu quero agua",
        "triste ajuda",
        "dor banheiro",
        "sim",
    ]

    for frase in frases:
        print(f"\n  Frase: '{frase}'")
        tokens = escanear_frase(frase)
        print(f"    Tokens: {tokens}")

        parser = Parser(tokens)
        parser.parse_frase()
        print(f"    Sintaxe: Válida ✓")

    print("\nTodos os testes de integração passaram! ✓")
    return True


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

if __name__ == "__main__":
    print("RELÓGIO DA FALA — BATERIA DE TESTES")
    print("=" * 60)

    resultados = []
    resultados.append(("Scanner", testar_scanner()))
    resultados.append(("Parser", testar_parser()))
    resultados.append(("Gramática", testar_gramatica()))
    resultados.append(("Integração", testar_integracao()))

    print("\n" + "=" * 60)
    print("RESUMO DOS RESULTADOS")
    print("=" * 60)

    todos_passaram = True
    for nome, resultado in resultados:
        status = "✓ PASSOU" if resultado else "✗ FALHOU"
        print(f"  {nome:15s} {status}")
        if not resultado:
            todos_passaram = False

    print()
    if todos_passaram:
        print("TODOS OS TESTES PASSARAM! ✓")
    else:
        print("ALGUNS TESTES FALHARAM! ✗")
