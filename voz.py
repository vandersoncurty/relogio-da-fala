"""
Módulo de Síntese de Voz — Relógio da Fala
Linguagem de Comunicação Alternativa e Aumentativa (CAA)

Converte a mensagem validada em áudio usando síntese de voz.

Prioridade: gTTS (online, mais natural) → pyttsx3 (offline, robótico)
"""

import sys
import os
import tempfile

# ============================================================
# SÍNTESE DE VOZ COM GTTS (online - prioritário)
# ============================================================

gtts_disponivel = False
try:
    from gtts import gTTS
    gtts_disponivel = True
except ImportError:
    pass

if gtts_disponivel:
    class SinteseVoz:
        """Síntese de voz online usando gTTS (voz natural)."""

        def __init__(self):
            self.idioma = "pt-br"
            self.tipo = "gTTS"

        def falar(self, mensagem: str):
            """Fala a mensagem em voz alta."""
            print(f"[VOZ gTTS] Falando: '{mensagem}'")
            try:
                tts = gTTS(text=mensagem, lang=self.idioma)

                # Salvar em arquivo temporário
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    arquivo = fp.name

                # Reproduzir
                if sys.platform == "win32":
                    os.system(f'start {arquivo}')
                elif sys.platform == "darwin":
                    os.system(f'afplay {arquivo}')
                else:
                    os.system(f'mpg123 {arquivo} 2>/dev/null || ffplay -nodisp -autoexit {arquivo} 2>/dev/null || aplay {arquivo} 2>/dev/null')

                # Limpar
                os.unlink(arquivo)
            except Exception as e:
                print(f"[ERRO] gTTS falhou: {e}")

        def falar_mensagem(self, valida: bool, mensagem: str):
            """Fala a mensagem com contexto."""
            if valida:
                self.falar(mensagem)
            else:
                self.falar(f"Atenção. {mensagem} não é uma combinação válida.")

# ============================================================
# FALLBACK: PYTTSX3 (offline)
# ============================================================

elif True:
    try:
        import pyttsx3

        class SinteseVoz:
            """Síntese de voz offline usando pyttsx3 (fallback)."""

            def __init__(self):
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", 150)
                self.engine.setProperty("volume", 1.0)
                self.tipo = "pyttsx3"

                # Tentar configurar voz em português
                voices = self.engine.getProperty("voices")
                for voice in voices:
                    if "portuguese" in voice.name.lower() or "pt" in voice.id.lower():
                        self.engine.setProperty("voice", voice.id)
                        break

            def falar(self, mensagem: str):
                """Fala a mensagem em voz alta."""
                print(f"[VOZ pyttsx3] Falando: '{mensagem}'")
                self.engine.say(mensagem)
                self.engine.runAndWait()

            def falar_mensagem(self, valida: bool, mensagem: str):
                """Fala a mensagem com contexto."""
                if valida:
                    self.falar(mensagem)
                else:
                    self.falar(f"Atenção. {mensagem} não é uma combinação válida.")

    except ImportError:
        class SinteseVoz:
            """Fallback: apenas imprime a mensagem."""
            def __init__(self):
                self.tipo = "simulada"
            def falar(self, mensagem: str):
                print(f"[VOZ SIMULADA] {mensagem}")
            def falar_mensagem(self, valida: bool, mensagem: str):
                if valida:
                    self.falar(mensagem)
                else:
                    print(f"[VOZ SIMULADA] Atenção. {mensagem} não é válida.")


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def criar_sintese():
    """Cria uma instância do módulo de síntese de voz."""
    return SinteseVoz()


# ============================================================
# TESTE
# ============================================================

if __name__ == "__main__":
    sintese = criar_sintese()

    print("Teste de síntese de voz:")
    print("-" * 40)

    sintese.falar_mensagem(True, "Eu quero água")
    sintese.falar_mensagem(True, "Estou com dor, preciso de ajuda")
    sintese.falar_mensagem(False, "Feliz banheiro")
