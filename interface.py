"""
Interface Digital — Relógio da Fala
Linguagem de Comunicação Alternativa e Aumentativa (CAA)

Aplicação visual com ponteiros arrastáveis que permite
ao usuário selecionar símbolos na placa circular.

Dependências: pygame-ce (pip install pygame-ce)
"""

import math
import sys

try:
    import pygame
except ImportError:
    print("Instale pygame: pip install pygame-ce")
    sys.exit(1)

from gramatica import POSICOES_PLACA, COMBINACOES_VALIDAS, TRADUCAO
from scanner import escanear_frase
from parser import Parser
from voz import criar_sintese


# ============================================================
# CONFIGURAÇÕES
# ============================================================

LARGURA = 800
ALTURA = 800
CENTRO = (LARGURA // 2, ALTURA // 2)
RAIO_EXTERNO = 320
RAIO_INTERNO = 100
RAIO_SIMBOLOS = 260
RAIO_PONTEIRO1 = 180
RAIO_PONTEIRO2 = 250

# Cores
COR_FUNDO = (30, 30, 40)
COR_CIRCULO = (50, 50, 70)
COR_TEXTO = (255, 255, 255)
COR_PONTEIRO1 = (0, 120, 255)  # Azul
COR_PONTEIRO2 = (255, 60, 60)  # Vermelho
COR_VALIDA = (0, 200, 100)  # Verde
COR_INVALIDA = (255, 50, 50)  # Vermelho
COR_DESTAQUE = (255, 255, 0)  # Amarelo

CORES_CATEGORIA = {
    "SUJEITO": (70, 130, 200),
    "CONFIRMACAO": (70, 130, 200),
    "VERBO": (70, 180, 100),
    "OBJETO": (220, 150, 50),
    "EMOCAO": (160, 80, 200),
}


# ============================================================
# CLASSE PRINCIPAL
# ============================================================

class RelogioDaFala:
    """Interface gráfica do Relógio da Fala."""

    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Relógio da Fala — CAA")
        self.fonte = pygame.font.SysFont("Arial", 18)
        self.fonte_grande = pygame.font.SysFont("Arial", 24, bold=True)
        self.fonte_titulo = pygame.font.SysFont("Arial", 32, bold=True)

        # Posições dos ponteiros (em graus)
        self.angulo_ponteiro1 = 0  # Ponteiro curto (azul)
        self.angulo_ponteiro2 = 90  # Ponteiro longo (vermelho)

        # Seleção atual
        self.pos_ponteiro1 = 1
        self.pos_ponteiro2 = 5
        self.mensagem = ""
        self.valida = False

        # Arrastando
        self.arrastando = None

        # Síntese de voz
        self.sintese = criar_sintese()

        self.atualizar_selecao()

    def calcular_posicao_simbolo(self, pos: int) -> tuple:
        """Calcula a posição (x, y) de um símbolo na placa."""
        angulo_graus = (pos - 1) * (360 / 16) - 90
        angulo_rad = math.radians(angulo_graus)
        x = CENTRO[0] + RAIO_SIMBOLOS * math.cos(angulo_rad)
        y = CENTRO[1] + RAIO_SIMBOLOS * math.sin(angulo_rad)
        return (int(x), int(y))

    def calcular_angulo_posicao(self, pos: int) -> float:
        """Calcula o ângulo em graus para uma posição."""
        return (pos - 1) * (360 / 16) - 90

    def posicao_para_angulo(self, angulo: float) -> int:
        """Converte um ângulo em graus para a posição mais próxima."""
        angulo = angulo % 360
        pos = round((angulo + 90) / (360 / 16)) % 16
        if pos == 0:
            pos = 16
        return pos

    def atualizar_selecao(self):
        """Atualiza a mensagem com base nos ponteiros selecionados."""
        simbolo1 = POSICOES_PLACA[self.pos_ponteiro1]["simbolo"]
        simbolo2 = POSICOES_PLACA[self.pos_ponteiro2]["simbolo"]

        # Tentar ambas as ordens da combinação
        chave1 = (simbolo1, simbolo2)
        chave2 = (simbolo2, simbolo1)

        if chave1 in COMBINACOES_VALIDAS:
            self.mensagem = COMBINACOES_VALIDAS[chave1]
            self.valida = True
        elif chave2 in COMBINACOES_VALIDAS:
            self.mensagem = COMBINACOES_VALIDAS[chave2]
            self.valida = True
        else:
            self.mensagem = f"{simbolo1} + {simbolo2}"
            self.valida = False

    def falar_mensagem(self):
        """Fala a mensagem atual usando síntese de voz."""
        if self.mensagem and self.valida:
            self.sintese.falar(self.mensagem)

    def desenhar_placa(self):
        """Desenha a placa circular com os símbolos."""
        # Fundo
        self.tela.fill(COR_FUNDO)

        # Círculo externo
        pygame.draw.circle(self.tela, COR_CIRCULO, CENTRO, RAIO_EXTERNO, 3)

        # Marcadores de posição
        for pos in range(1, 17):
            angulo = self.calcular_angulo_posicao(pos)
            angulo_rad = math.radians(angulo)
            x1 = CENTRO[0] + (RAIO_EXTERNO - 15) * math.cos(angulo_rad)
            y1 = CENTRO[1] + (RAIO_EXTERNO - 15) * math.sin(angulo_rad)
            x2 = CENTRO[0] + (RAIO_EXTERNO + 5) * math.cos(angulo_rad)
            y2 = CENTRO[1] + (RAIO_EXTERNO + 5) * math.sin(angulo_rad)
            pygame.draw.line(self.tela, (100, 100, 120), (int(x1), int(y1)), (int(x2), int(y2)), 2)

        # Símbolos
        for pos, info in POSICOES_PLACA.items():
            x, y = self.calcular_posicao_simbolo(pos)
            cor = CORES_CATEGORIA.get(info["categoria"], COR_TEXTO)

            # Destaque se selecionado
            if pos == self.pos_ponteiro1 or pos == self.pos_ponteiro2:
                pygame.draw.circle(self.tela, COR_DESTAQUE, (x, y), 25, 3)

            texto = self.fonte.render(info["simbolo"], True, cor)
            rect = texto.get_rect(center=(x, y))
            self.tela.blit(texto, rect)

    def desenhar_ponteiro(self, angulo: float, raio: int, cor: tuple, label: str):
        """Desenha um ponteiro na placa."""
        angulo_rad = math.radians(angulo)
        x = CENTRO[0] + raio * math.cos(angulo_rad)
        y = CENTRO[1] + raio * math.sin(angulo_rad)

        # Linha do ponteiro
        pygame.draw.line(self.tela, cor, CENTRO, (int(x), int(y)), 4)

        # Ponta do ponteiro
        pygame.draw.circle(self.tela, cor, (int(x), int(y)), 8)

        # Label
        texto = self.fonte.render(label, True, cor)
        self.tela.blit(texto, (int(x) + 12, int(y) - 12))

    def desenhar_mensagem(self):
        """Desenha a mensagem resultante na parte inferior."""
        # Fundo da mensagem
        pygame.draw.rect(self.tela, (40, 40, 50), (50, ALTURA - 120, LARGURA - 100, 80), border_radius=10)

        # Borda
        cor_borda = COR_VALIDA if self.valida else COR_INVALIDA
        pygame.draw.rect(self.tela, cor_borda, (50, ALTURA - 120, LARGURA - 100, 80), 3, border_radius=10)

        # Texto da mensagem
        cor_msg = COR_VALIDA if self.valida else COR_INVALIDA
        texto = self.fonte_grande.render(self.mensagem, True, cor_msg)
        rect = texto.get_rect(center=(LARGURA // 2, ALTURA - 80))
        self.tela.blit(texto, rect)

        # Status
        status = "VÁLIDA" if self.valida else "Inválida"
        texto_status = self.fonte.render(f"Status: {status}", True, cor_msg)
        self.tela.blit(texto_status, (60, ALTURA - 110))

        # Dica do SPACE
        if self.valida:
            texto_dica = self.fonte.render("Espaço = falar", True, (150, 150, 150))
            self.tela.blit(texto_dica, (LARGURA - 180, ALTURA - 110))

    def desenhar_titulo(self):
        """Desenha o título do aplicativo."""
        texto = self.fonte_titulo.render("Relógio da Fala", True, COR_TEXTO)
        rect = texto.get_rect(center=(LARGURA // 2, 30))
        self.tela.blit(texto, rect)

        # Mostrar tipo de voz
        tipo_voz = self.sintese.tipo if hasattr(self.sintese, 'tipo') else "N/D"
        texto_voz = self.fonte.render(f"Voz: {tipo_voz}", True, (150, 150, 150))
        self.tela.blit(texto_voz, (LARGURA - 120, 45))

    def desenhar_legenda(self):
        """Desenha a legenda das cores."""
        y = 60
        legendas = [
            ("Sujeitos", CORES_CATEGORIA["SUJEITO"]),
            ("Verbos", CORES_CATEGORIA["VERBO"]),
            ("Objetos", CORES_CATEGORIA["OBJETO"]),
            ("Emoções", CORES_CATEGORIA["EMOCAO"]),
        ]
        for label, cor in legendas:
            pygame.draw.circle(self.tela, cor, (30, y), 6)
            texto = self.fonte.render(label, True, cor)
            self.tela.blit(texto, (45, y - 8))
            y += 25

    def processar_eventos(self):
        """Processa eventos de entrada (mouse, teclado)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Verificar se clicou em algum ponteiro
                dist_centro = math.sqrt((mx - CENTRO[0]) ** 2 + (my - CENTRO[1]) ** 2)
                
                # Calcular distância do clique à ponta de cada ponteiro
                # Ponteiro 1 (curto)
                angulo_rad1 = math.radians(self.angulo_ponteiro1)
                ponta1_x = CENTRO[0] + RAIO_PONTEIRO1 * math.cos(angulo_rad1)
                ponta1_y = CENTRO[1] + RAIO_PONTEIRO1 * math.sin(angulo_rad1)
                dist_ponta1 = math.sqrt((mx - ponta1_x) ** 2 + (my - ponta1_y) ** 2)
                
                # Ponteiro 2 (longo)
                angulo_rad2 = math.radians(self.angulo_ponteiro2)
                ponta2_x = CENTRO[0] + RAIO_PONTEIRO2 * math.cos(angulo_rad2)
                ponta2_y = CENTRO[1] + RAIO_PONTEIRO2 * math.sin(angulo_rad2)
                dist_ponta2 = math.sqrt((mx - ponta2_x) ** 2 + (my - ponta2_y) ** 2)
                
                # Verificar se clicou perto da ponta de algum ponteiro
                raio_clique = 25  # Raio de tolerância para clique
                
                if dist_ponta1 < raio_clique and dist_ponta1 < dist_ponta2:
                    self.arrastando = 1
                elif dist_ponta2 < raio_clique:
                    self.arrastando = 2
                elif dist_centro < RAIO_PONTEIRO2 + 30:
                    # Se não clicou na ponta, verificar qual ponteiro está mais próximo
                    # Calcular ângulo do clique
                    angulo_clique = math.degrees(math.atan2(my - CENTRO[1], mx - CENTRO[0]))
                    
                    # Diferença angular entre o clique e cada ponteiro
                    diff1 = abs((angulo_clique - self.angulo_ponteiro1 + 180) % 360 - 180)
                    diff2 = abs((angulo_clique - self.angulo_ponteiro2 + 180) % 360 - 180)
                    
                    if diff1 < diff2:
                        self.arrastando = 1
                    else:
                        self.arrastando = 2

            elif event.type == pygame.MOUSEBUTTONUP:
                self.arrastando = None

            elif event.type == pygame.MOUSEMOTION and self.arrastando:
                mx, my = event.pos
                angulo = math.degrees(math.atan2(my - CENTRO[1], mx - CENTRO[0]))
                pos = self.posicao_para_angulo(angulo)

                if self.arrastando == 1:
                    self.pos_ponteiro1 = pos
                    self.angulo_ponteiro1 = self.calcular_angulo_posicao(pos)
                elif self.arrastando == 2:
                    self.pos_ponteiro2 = pos
                    self.angulo_ponteiro2 = self.calcular_angulo_posicao(pos)

                self.atualizar_selecao()

            elif event.type == pygame.KEYDOWN:
                # Teclas 1-16 para selecionar posições
                if pygame.K_1 <= event.key <= pygame.K_9:
                    pos = event.key - pygame.K_0
                    self.pos_ponteiro1 = pos
                    self.angulo_ponteiro1 = self.calcular_angulo_posicao(pos)
                    self.atualizar_selecao()
                elif event.key == pygame.K_0:
                    self.pos_ponteiro1 = 10
                    self.angulo_ponteiro1 = self.calcular_angulo_posicao(10)
                    self.atualizar_selecao()

                # Q-W-E-R para posições 11-16
                elif event.key == pygame.K_q:
                    self.pos_ponteiro2 = 11
                    self.angulo_ponteiro2 = self.calcular_angulo_posicao(11)
                    self.atualizar_selecao()
                elif event.key == pygame.K_w:
                    self.pos_ponteiro2 = 12
                    self.angulo_ponteiro2 = self.calcular_angulo_posicao(12)
                    self.atualizar_selecao()
                elif event.key == pygame.K_e:
                    self.pos_ponteiro2 = 13
                    self.angulo_ponteiro2 = self.calcular_angulo_posicao(13)
                    self.atualizar_selecao()
                elif event.key == pygame.K_r:
                    self.pos_ponteiro2 = 14
                    self.angulo_ponteiro2 = self.calcular_angulo_posicao(14)
                    self.atualizar_selecao()
                elif event.key == pygame.K_t:
                    self.pos_ponteiro2 = 15
                    self.angulo_ponteiro2 = self.calcular_angulo_posicao(15)
                    self.atualizar_selecao()
                elif event.key == pygame.K_y:
                    self.pos_ponteiro2 = 16
                    self.angulo_ponteiro2 = self.calcular_angulo_posicao(16)
                    self.atualizar_selecao()

                # Espaço para falar a mensagem
                elif event.key == pygame.K_SPACE:
                    self.falar_mensagem()

        return True

    def executar(self):
        """Loop principal do aplicativo."""
        rodando = True
        relogio = pygame.time.Clock()

        while rodando:
            rodando = self.processar_eventos()

            # Desenhar
            self.desenhar_placa()
            self.desenhar_ponteiro(
                self.angulo_ponteiro1, RAIO_PONTEIRO1, COR_PONTEIRO1, "P1"
            )
            self.desenhar_ponteiro(
                self.angulo_ponteiro2, RAIO_PONTEIRO2, COR_PONTEIRO2, "P2"
            )
            self.desenhar_mensagem()
            self.desenhar_titulo()
            self.desenhar_legenda()

            pygame.display.flip()
            relogio.tick(30)

        pygame.quit()


# ============================================================
# PONTO DE ENTRADA
# ============================================================

if __name__ == "__main__":
    app = RelogioDaFala()
    app.executar()
