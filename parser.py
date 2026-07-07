"""
Parser (Analisador Sintático) — Relógio da Fala
Linguagem de Comunicação Alternativa e Aumentativa (CAA)

Implementa análise descendente recursiva para validar
a estrutura sintática das frases, seguindo a gramática BNF/EBNF.

Referência: Hopcroft, Motwani, Ullman (2006)
"""

from scanner import escanear_frase, lexical_analyzer


# ============================================================
# CLASSE PRINCIPAL DO PARSER
# ============================================================

class Parser:
    """
    Analisador sintático descendente recursivo.
    Valida se a sequência de tokens obedece à gramática BNF.
    """

    def __init__(self, tokens: list):
        """
        Inicializa o parser com uma lista de tokens.

        Args:
            tokens: Lista de tuplas (tipo, valor)
        """
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token_type = tokens[0][0] if tokens else None
        self.current_token_value = tokens[0][1] if tokens else None

    def advance(self):
        """Move para o próximo token."""
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token_type = self.tokens[self.current_token_index][0]
            self.current_token_value = self.tokens[self.current_token_index][1]
        else:
            self.current_token_type = None
            self.current_token_value = None

    def consume(self, expected_type: str):
        """
        Verifica e consome o token esperado, ou lança erro.

        Args:
            expected_type: Tipo do token esperado

        Raises:
            SyntaxError: Se o token atual não for do tipo esperado
        """
        if self.current_token_type == expected_type:
            self.advance()
        else:
            raise SyntaxError(
                f"Erro de sintaxe: Esperado '{expected_type}', "
                f"mas encontrado '{self.current_token_type}' "
                f"('{self.current_token_value}')"
            )

    # ============================================================
    # REGRAS BNF COMO MÉTODOS
    # ============================================================

    def parse_frase(self):
        """
        <frase> ::= <combinacao>
        Regra principal: toda frase é uma combinação de dois ponteiros.
        """
        if self.current_token_type is None:
            raise SyntaxError("Erro: Frase vazia.")

        # Tentar combinação (ponteiro1 + ponteiro2)
        self.parse_combinacao()

        # Verificar se não há tokens extras
        if self.current_token_type is not None:
            raise SyntaxError(
                f"Erro: Token inesperado '{self.current_token_value}' "
                f"após o final da frase."
            )

    def parse_combinacao(self):
        """
        <combinacao> ::= <ponteiro1> <ponteiro2> [<complemento>]
        Combinação de dois ponteiros para formar uma frase.
        O complemento é opcional (ex: "Eu quero água" = 3 tokens).
        """
        self.parse_ponteiro1()
        self.parse_ponteiro2()
        # Complemento opcional para frases com 3 tokens
        self.parse_complemento()

    def parse_ponteiro1(self):
        """
        <ponteiro1> ::= <SUJEITO> | <EMOCAO>
        Primeiro ponteiro: seleciona sujeito ou emoção.
        """
        if self.current_token_type == "SUJEITO":
            self.consume("SUJEITO")
        elif self.current_token_type == "EMOCAO":
            self.consume("EMOCAO")
        elif self.current_token_type == "CONFIRMACAO":
            # "sim" e "não" também podem iniciar frases
            self.consume("CONFIRMACAO")
        elif self.current_token_type == "NEGACAO":
            self.consume("NEGACAO")
        else:
            raise SyntaxError(
                f"Erro: Esperado SUJEITO, EMOCAO, CONFIRMACAO ou NEGACAO, "
                f"mas encontrado '{self.current_token_type}' "
                f"('{self.current_token_value}')"
            )

    def parse_ponteiro2(self):
        """
        <ponteiro2> ::= <VERBO> | <OBJETO> | <ESTADO>
        Segundo ponteiro: seleciona verbo, objeto ou estado.
        """
        if self.current_token_type is None:
            # Fim da frase é aceitável (ex: "sim" sozinho)
            return

        if self.current_token_type == "VERBO":
            self.consume("VERBO")
        elif self.current_token_type == "OBJETO":
            self.consume("OBJETO")
        elif self.current_token_type == "CONFIRMACAO":
            self.consume("CONFIRMACAO")
        elif self.current_token_type == "NEGACAO":
            self.consume("NEGACAO")
        elif self.current_token_type == "EMOCAO":
            # Emoção pode aparecer como segundo ponteiro
            self.consume("EMOCAO")
        else:
            raise SyntaxError(
                f"Erro: Esperado VERBO, OBJETO ou ESTADO, "
                f"mas encontrado '{self.current_token_type}' "
                f"('{self.current_token_value}')"
            )

    def parse_complemento(self):
        """
        <complemento> ::= <OBJETO> | <VERBO> | <EMOCAO>
        Complemento opcional para frases com 3 tokens.
        Ex: "Eu quero água" = SUJEITO + VERBO + OBJETO
        """
        if self.current_token_type is None:
            # Fim da frase é aceitável
            return

        # Aceitar qualquer token restante como complemento
        if self.current_token_type in ["OBJETO", "VERBO", "EMOCAO", "CONFIRMACAO", "NEGACAO"]:
            self.advance()  # Consome o token restante


# ============================================================
# FUNÇÃO DE TESTE PRINCIPAL
# ============================================================

def testar_frase(texto_entrada: str):
    """
    Testa uma frase: escaneia, parsea e informa se é válida.

    Args:
        texto_entrada: Frase em linguagem natural
    """
    print(f"\n--- Testando: '{texto_entrada}' ---")
    try:
        tokens = escanear_frase(texto_entrada)
        print(f"  Tokens: {tokens}")

        parser = Parser(tokens)
        parser.parse_frase()
        print("  Resultado: Frase VÁLIDA ✓")

    except (RuntimeError, SyntaxError) as e:
        print(f"  Resultado: {e}")
        print("  Frase INVÁLIDA ✗")


# ============================================================
# BATERIA DE TESTES
# ============================================================

def executar_testes():
    """Executa bateria completa de testes do parser."""
    print("=" * 60)
    print("TESTES DO PARSER — RELÓGIO DA FALA")
    print("=" * 60)

    # Frases válidas
    print("\n>>> FRASES VÁLIDAS <<<")
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
    for frase in validas:
        testar_frase(frase)

    # Frases inválidas
    print("\n>>> FRASES INVÁLIDAS <<<")
    invalidas = [
        "Eu agua quero",
        "quero Eu",
        "agua comida",
        "sair banheiro",
        "Eu",
        "quero",
    ]
    for frase in invalidas:
        testar_frase(frase)


if __name__ == "__main__":
    executar_testes()
