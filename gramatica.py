"""
Gramática BNF/EBNF — Relógio da Fala
Linguagem de Comunicação Alternativa e Aumentativa (CAA)

Formalização das regras gramaticais para a placa de comunicação
em formato de relógio com 16 símbolos e dois ponteiros.

Referência: ISO/IEC 14977:1996 — Extended Backus-Naur Form
"""

# ============================================================
# DEFINIÇÃO DA GRAMÁTICA EM BNF
# ============================================================

GRAMATICA_BNF = """
# ============================================================
# GRAMÁTICA BNF — RELÓGIO DA FALA
# Placa de CAA com 16 símbolos e dois ponteiros
# ============================================================

# Regra principal: uma frase é uma combinação de dois ponteiros
<frase> ::= <combinacao>

# Combinação: ponteiro1 + ponteiro2
<combinacao> ::= <ponteiro1> <ponteiro2>

# Ponteiro 1 (hora): seleciona sujeito ou emoção
<ponteiro1> ::= <SUJEITO> | <EMOCAO>

# Ponteiro 2 (minuto): seleciona verbo, objeto ou estado
<ponteiro2> ::= <VERBO> | <OBJETO> | <ESTADO>

# --- Terminais (Símbolos da Placa) ---

# Quadrante 1 — Sujeitos e Confirmação (Posições 1-4)
<SUJEITO> ::= "Eu" | "Você"
<CONFIRMACAO> ::= "sim" | "não"

# Quadrante 2 — Verbos e Ações (Posições 5-8)
<VERBO> ::= "quero" | "preciso" | "comer" | "beber"

# Quadrante 3 — Objetos e Necessidades (Posições 9-12)
<OBJETO> ::= "água" | "comida" | "banheiro" | "sair"

# Quadrante 4 — Emoções e Estados (Posições 13-16)
<EMOCAO> ::= "feliz" | "triste" | "dor" | "ajuda"
<ESTADO> ::= "sim" | "não"
"""

# ============================================================
# DEFINIÇÃO DOS TOKENS PARA O SCANNER
# ============================================================

TOKEN_TYPES = [
    # Sujeitos
    ("SUJEITO", r"Eu|Voce"),
    # Verbos
    ("VERBO", r"quero|preciso|comer|beber"),
    # Objetos
    ("OBJETO", r"agua|comida|banheiro|sair"),
    # Emoções
    ("EMOCAO", r"feliz|triste|dor|ajuda"),
    # Confirmação/Estado
    ("CONFIRMACAO", r"sim|s"),
    ("NEGACAO", r"nao|n"),
    # Pular espaços
    ("SKIP", r"[ \t\n]+"),
    # Erro léxico
    ("MISMATCH", r"."),
]

# ============================================================
# MAPA DE POSIÇÕES DA PLACA (Relógio com 16 posições)
# ============================================================

POSICOES_PLACA = {
    # Quadrante 1 — Sujeitos/Confirmação
    1: {"simbolo": "EU", "categoria": "SUJEITO", "cor": "azul"},
    2: {"simbolo": "VOCÊ", "categoria": "SUJEITO", "cor": "azul"},
    3: {"simbolo": "SIM", "categoria": "CONFIRMACAO", "cor": "azul"},
    4: {"simbolo": "NÃO", "categoria": "CONFIRMACAO", "cor": "azul"},
    # Quadrante 2 — Verbos/Ações
    5: {"simbolo": "QUERO", "categoria": "VERBO", "cor": "verde"},
    6: {"simbolo": "PRECISO", "categoria": "VERBO", "cor": "verde"},
    7: {"simbolo": "COMER", "categoria": "VERBO", "cor": "verde"},
    8: {"simbolo": "BEBER", "categoria": "VERBO", "cor": "verde"},
    # Quadrante 3 — Objetos/Necessidades
    9: {"simbolo": "ÁGUA", "categoria": "OBJETO", "cor": "laranja"},
    10: {"simbolo": "COMIDA", "categoria": "OBJETO", "cor": "laranja"},
    11: {"simbolo": "BANHEIRO", "categoria": "OBJETO", "cor": "laranja"},
    12: {"simbolo": "SAIR", "categoria": "OBJETO", "cor": "laranja"},
    # Quadrante 4 — Emoções/Estados
    13: {"simbolo": "FELIZ", "categoria": "EMOCAO", "cor": "roxo"},
    14: {"simbolo": "TRISTE", "categoria": "EMOCAO", "cor": "roxo"},
    15: {"simbolo": "DOR", "categoria": "EMOCAO", "cor": "roxo"},
    16: {"simbolo": "AJUDA", "categoria": "EMOCAO", "cor": "roxo"},
}

# ============================================================
# MAPA DE TRADUÇÃO (símbolo → texto falado)
# ============================================================

TRADUCAO = {
    "EU": "Eu",
    "VOCÊ": "Você",
    "SIM": "Sim",
    "NÃO": "Não",
    "QUERO": "quero",
    "PRECISO": "preciso",
    "COMER": "comer",
    "BEBER": "beber",
    "ÁGUA": "água",
    "COMIDA": "comida",
    "BANHEIRO": "banheiro",
    "SAIR": "sair",
    "FELIZ": "estou feliz",
    "TRISTE": "estou triste",
    "DOR": "estou com dor",
    "AJUDA": "preciso de ajuda",
}

# ============================================================
# COMBINAÇÕES VÁLIDAS
# ============================================================

COMBINACOES_VALIDAS = {
    # Sujeito + Verbo
    ("EU", "QUERO"): "Eu quero",
    ("EU", "PRECISO"): "Eu preciso",
    ("EU", "COMER"): "Eu quero comer",
    ("EU", "BEBER"): "Eu quero beber",
    ("VOCÊ", "QUERO"): "Você quer",
    ("VOCÊ", "PRECISO"): "Você precisa",
    # Sujeito + Objeto
    ("EU", "ÁGUA"): "Eu quero água",
    ("EU", "COMIDA"): "Eu quero comida",
    ("EU", "BANHEIRO"): "Eu preciso de banheiro",
    ("EU", "SAIR"): "Eu quero sair",
    # Sujeito + Emoção
    ("EU", "FELIZ"): "Eu estou feliz",
    ("EU", "TRISTE"): "Eu estou triste",
    ("EU", "DOR"): "Eu estou com dor",
    ("EU", "AJUDA"): "Eu preciso de ajuda",
    # Verbo + Objeto
    ("QUERO", "ÁGUA"): "Quero água",
    ("QUERO", "COMIDA"): "Quero comida",
    ("QUERO", "BANHEIRO"): "Preciso ir ao banheiro",
    ("QUERO", "SAIR"): "Quero sair",
    ("PRECISO", "ÁGUA"): "Preciso de água",
    ("PRECISO", "COMIDA"): "Preciso de comida",
    ("PRECISO", "BANHEIRO"): "Preciso ir ao banheiro",
    ("PRECISO", "SAIR"): "Preciso sair",
    ("COMER", "ÁGUA"): "Comer e beber água",
    ("COMER", "COMIDA"): "Comer comida",
    ("BEBER", "ÁGUA"): "Beber água",
    ("BEBER", "COMIDA"): "Beber e comer",
    # Emoção + Ação
    ("TRISTE", "COMER"): "Estou triste comendo",
    ("TRISTE", "BEBER"): "Estou triste bebendo",
    ("TRISTE", "ÁGUA"): "Não quero água",
    ("TRISTE", "COMIDA"): "Não quero comida",
    ("TRISTE", "BANHEIRO"): "Não quero ir ao banheiro",
    ("TRISTE", "SAIR"): "Não quero sair",
    ("DOR", "COMER"): "Estou com dor ao comer",
    ("DOR", "BEBER"): "Estou com dor ao beber",
    ("DOR", "ÁGUA"): "Estou com dor, preciso de água",
    ("DOR", "COMIDA"): "Estou com dor ao comer",
    ("DOR", "BANHEIRO"): "Estou com dor, preciso ir ao banheiro",
    ("DOR", "SAIR"): "Estou com dor, preciso sair",
    ("FELIZ", "COMER"): "Estou feliz comendo",
    ("FELIZ", "BEBER"): "Estou feliz bebendo",
    ("FELIZ", "ÁGUA"): "Estou feliz bebendo água",
    ("FELIZ", "COMIDA"): "Estou feliz comendo",
    ("FELIZ", "BANHEIRO"): "Estou feliz indo ao banheiro",
    ("FELIZ", "SAIR"): "Estou feliz saindo",
    # Ajuda + Necessidade
    ("AJUDA", "BANHEIRO"): "Preciso de ajuda para ir ao banheiro",
    ("AJUDA", "ÁGUA"): "Preciso de ajuda para pegar água",
    ("AJUDA", "COMIDA"): "Preciso de ajuda para comer",
    ("AJUDA", "SAIR"): "Preciso de ajuda para sair",
    ("AJUDA", "DOR"): "Preciso de ajuda, estou com dor",
    ("AJUDA", "TRISTE"): "Preciso de ajuda, estou triste",
    ("DOR", "AJUDA"): "Estou com dor, preciso de ajuda",
    ("TRISTE", "AJUDA"): "Estou triste, preciso de ajuda",
    # Confirmação + Verbo
    ("SIM", "QUERO"): "Sim, eu quero",
    ("SIM", "PRECISO"): "Sim, eu preciso",
    ("SIM", "COMER"): "Sim, quero comer",
    ("SIM", "BEBER"): "Sim, quero beber",
    ("NÃO", "QUERO"): "Não, eu não quero",
    ("NÃO", "PRECISO"): "Não, eu não preciso",
    ("NÃO", "COMER"): "Não, não quero comer",
    ("NÃO", "BEBER"): "Não, não quero beber",
    # Confirmação + Objeto
    ("SIM", "ÁGUA"): "Sim, quero água",
    ("SIM", "COMIDA"): "Sim, quero comida",
    ("SIM", "BANHEIRO"): "Sim, preciso ir ao banheiro",
    ("SIM", "SAIR"): "Sim, quero sair",
    ("NÃO", "ÁGUA"): "Não, não quero água",
    ("NÃO", "COMIDA"): "Não, não quero comida",
    ("NÃO", "BANHEIRO"): "Não, não preciso ir ao banheiro",
    ("NÃO", "SAIR"): "Não, não quero sair",
    # Confirmação + Emoção
    ("NÃO", "FELIZ"): "Não estou feliz",
    ("NÃO", "TRISTE"): "Não estou triste",
    ("NÃO", "DOR"): "Não estou com dor",
    ("NÃO", "AJUDA"): "Não preciso de ajuda",
    ("SIM", "FELIZ"): "Sim, estou feliz",
    ("SIM", "TRISTE"): "Sim, estou triste",
    ("SIM", "DOR"): "Sim, estou com dor",
    ("SIM", "AJUDA"): "Sim, preciso de ajuda",
    # Confirmação + Confirmação
    ("SIM", "SIM"): "Sim",
    ("NÃO", "NÃO"): "Não",
    # Perguntas (VOCÊ +)
    ("VOCÊ", "ÁGUA"): "Você quer água?",
    ("VOCÊ", "COMIDA"): "Você quer comida?",
    ("VOCÊ", "BANHEIRO"): "Você precisa ir ao banheiro?",
    ("VOCÊ", "SAIR"): "Você quer sair?",
    ("VOCÊ", "COMER"): "Você quer comer?",
    ("VOCÊ", "BEBER"): "Você quer beber?",
    ("VOCÊ", "FELIZ"): "Você está feliz?",
    ("VOCÊ", "TRISTE"): "Você está triste?",
    ("VOCÊ", "DOR"): "Você está com dor?",
    ("VOCÊ", "AJUDA"): "Você precisa de ajuda?",
    # Emoção + Emoção
    ("FELIZ", "TRISTE"): "Estou feliz e triste",
    ("FELIZ", "DOR"): "Estou feliz, mas com dor",
    ("FELIZ", "AJUDA"): "Estou feliz, preciso de ajuda",
    ("TRISTE", "DOR"): "Estou triste e com dor",
    ("TRISTE", "FELIZ"): "Estou triste e feliz",
    ("DOR", "TRISTE"): "Estou com dor e triste",
    ("DOR", "FELIZ"): "Estou com dor, mas feliz",
    ("DOR", "DOR"): "Estou com muita dor",
    ("AJUDA", "FELIZ"): "Preciso de ajuda, estou feliz",
    ("AJUDA", "TRISTE"): "Preciso de ajuda, estou triste",
    ("AJUDA", "DOR"): "Preciso de ajuda, estou com dor",
    ("AJUDA", "AJUDA"): "Preciso muito de ajuda",
    # Ajuda + Verbo
    ("AJUDA", "QUERO"): "Preciso de ajuda, eu quero",
    ("AJUDA", "PRECISO"): "Preciso muito de ajuda",
    ("AJUDA", "COMER"): "Preciso de ajuda para comer",
    ("AJUDA", "BEBER"): "Preciso de ajuda para beber",
}


def obter_frase(pos_ponteiro1: int, pos_ponteiro2: int) -> str:
    """
    Retorna a frase correspondente à combinação dos dois ponteiros.

    Args:
        pos_ponteiro1: Posição do ponteiro 1 (1-16)
        pos_ponteiro2: Posição do ponteiro 2 (1-16)

    Returns:
        Frase correspondente ou mensagem de erro
    """
    if pos_ponteiro1 not in POSICOES_PLACA:
        return f"Erro: Posição {pos_ponteiro1} inválida para ponteiro 1"
    if pos_ponteiro2 not in POSICOES_PLACA:
        return f"Erro: Posição {pos_ponteiro2} inválida para ponteiro 2"

    simbolo1 = POSICOES_PLACA[pos_ponteiro1]["simbolo"]
    simbolo2 = POSICOES_PLACA[pos_ponteiro2]["simbolo"]

    chave = (simbolo1, simbolo2)
    if chave in COMBINACOES_VALIDAS:
        return COMBINACOES_VALIDAS[chave]
    else:
        return f"Combinação não reconhecida: {simbolo1} + {simbolo2}"


def listar_simbolos():
    """Lista todos os símbolos organizados por quadrante."""
    for pos, info in POSICOES_PLACA.items():
        print(f"  Posição {pos:2d}: {info['simbolo']:10s} [{info['categoria']:12s}] {info['cor']}")


def listar_combinacoes():
    """Lista todas as combinações válidas."""
    for (s1, s2), frase in COMBINACOES_VALIDAS.items():
        print(f"  {s1:8s} + {s2:8s} → {frase}")


if __name__ == "__main__":
    print("=" * 60)
    print("GRAMÁTICA BNF — RELÓGIO DA FALA")
    print("=" * 60)
    print()
    print("SÍMBOLOS DA PLACA:")
    print("-" * 60)
    listar_simbolos()
    print()
    print("COMBINAÇÕES VÁLIDAS:")
    print("-" * 60)
    listar_combinacoes()
    print()
    print("GRAMÁTICA BNF:")
    print("-" * 60)
    print(GRAMATICA_BNF)
