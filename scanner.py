"""
Scanner (Analisador Léxico) — Relógio da Fala
Linguagem de Comunicação Alternativa e Aumentativa (CAA)

Transforma o texto de entrada em uma lista de tokens,
seguindo as definições da gramática BNF/EBNF.

Referência: Hopcroft, Motwani, Ullman (2006)
"""

import re


# ============================================================
# DEFINIÇÃO DOS TIPOS DE TOKENS
# ============================================================

TOKEN_TYPES = [
    # Ordem é importante! Tokens mais longos primeiro.
    ("SUJEITO", r"eu|voce"),
    ("VERBO", r"quero|preciso|comer|beber"),
    ("OBJETO", r"agua|comida|banheiro|sair"),
    ("EMOCAO", r"feliz|triste|dor|ajuda"),
    ("CONFIRMACAO", r"sim|s"),
    ("NEGACAO", r"nao|n"),
    ("SKIP", r"[ \t\n]+"),
    ("MISMATCH", r"."),
]

# Compila a regex unificada
TOKEN_REGEX = "|".join(
    "(?P<%s>%s)" % (name, pattern) for name, pattern in TOKEN_TYPES
)


# ============================================================
# FUNÇÃO PRINCIPAL DO SCANNER
# ============================================================

def lexical_analyzer(source_code: str) -> list:
    """
    Analisador léxico: transforma texto de entrada em lista de tokens.

    Args:
        source_code: Texto de entrada (ex: "Eu quero agua")

    Returns:
        Lista de tuplas (tipo_token, valor_token)

    Raises:
        RuntimeError: Se encontrar caractere inválido
    """
    tokens = []

    for match in re.finditer(TOKEN_REGEX, source_code):
        token_type = match.lastgroup
        token_value = match.group(token_type)

        if token_type == "SKIP":
            continue

        if token_type == "MISMATCH":
            raise RuntimeError(
                f"Erro léxico: Caractere inesperado '{token_value}' "
                f"na posição {match.start()}"
            )

        tokens.append((token_type, token_value))

    return tokens


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def normalizar_texto(texto: str) -> str:
    """
    Normaliza o texto de entrada para o scanner.

    Args:
        texto: Texto original

    Returns:
        Texto normalizado (minúsculas, sem acentos simples)
    """
    texto = texto.lower().strip()
    # Substituições para aceitar variações
    texto = texto.replace("você", "voce")
    texto = texto.replace("á", "a")
    texto = texto.replace("é", "e")
    texto = texto.replace("ã", "a")
    texto = texto.replace("õ", "o")
    return texto


def escanear_frase(texto: str) -> list:
    """
    Função de alto nível: normaliza e escaneia uma frase.

    Args:
        texto: Frase em linguagem natural

    Returns:
        Lista de tokens
    """
    texto_normalizado = normalizar_texto(texto)
    return lexical_analyzer(texto_normalizado)


# ============================================================
# TESTES
# ============================================================

def testar_scanner():
    """Executa testes do scanner com frases válidas e inválidas."""
    testes = [
        # (entrada, esperado_válido)
        ("Eu quero agua", True),
        ("Eu quero comida", True),
        ("sim", True),
        ("n", True),
        ("triste ajuda", True),
        ("dor banheiro", True),
        ("feliz comer", True),
        ("preciso banheiro", True),
        ("Eu agua quero", True),  # Válido léxico, mas inválido sintático
        ("Eu @#$%", False),  # Erro léxico esperado
    ]

    print("=" * 60)
    print("TESTES DO SCANNER")
    print("=" * 60)

    for entrada, esperado_valido in testes:
        print(f"\nEntrada: '{entrada}'")
        try:
            tokens = escanear_frase(entrada)
            print(f"  Tokens: {tokens}")
            if esperado_valido:
                print("  ✓ OK")
            else:
                print("  ✗ Era esperado erro léxico")
        except RuntimeError as e:
            print(f"  Erro: {e}")
            if not esperado_valido:
                print("  ✓ OK (erro esperado)")
            else:
                print("  ✗ Erro inesperado")


if __name__ == "__main__":
    testar_scanner()
