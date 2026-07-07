"""
Interface Web — Relógio da Fala
Linguagem de Comunicação Alternativa e Aumentativa (CAA)

Aplicação Flask com interface responsiva e design moderno.
"""

import sys
import os
import tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request, send_file
from gramatica import POSICOES_PLACA, COMBINACOES_VALIDAS, TRADUCAO, obter_frase

app = Flask(__name__)


@app.route("/")
def index():
    """Página principal com o relógio interativo."""
    return render_template("index.html")


@app.route("/api/simbolos")
def api_simbolos():
    """Retorna todos os símbolos da placa."""
    return jsonify(POSICOES_PLACA)


@app.route("/api/validar")
def api_validar():
    """
    Valida uma combinação de ponteiros.

    Query params:
        p1: posição do ponteiro 1 (1-16)
        p2: posição do ponteiro 2 (1-16)
    """
    p1 = request.args.get("p1", type=int)
    p2 = request.args.get("p2", type=int)

    if p1 is None or p2 is None:
        return jsonify({"erro": "Parâmetros p1 e p2 são obrigatórios"}), 400

    if p1 not in POSICOES_PLACA or p2 not in POSICOES_PLACA:
        return jsonify({"erro": "Posição inválida"}), 400

    frase = obter_frase(p1, p2)
    simbolo1 = POSICOES_PLACA[p1]["simbolo"]
    simbolo2 = POSICOES_PLACA[p2]["simbolo"]

    chave1 = (simbolo1, simbolo2)
    chave2 = (simbolo2, simbolo1)

    valida = chave1 in COMBINACOES_VALIDAS or chave2 in COMBINACOES_VALIDAS

    return jsonify({
        "p1": p1,
        "p2": p2,
        "simbolo1": simbolo1,
        "simbolo2": simbolo2,
        "frase": frase,
        "valida": valida
    })


@app.route("/api/combinacoes")
def api_combinacoes():
    """Retorna todas as combinações válidas."""
    combinacoes = []
    for (s1, s2), frase in COMBINACOES_VALIDAS.items():
        combinacoes.append({
            "simbolo1": s1,
            "simbolo2": s2,
            "frase": frase
        })
    return jsonify(combinacoes)


@app.route("/api/falar")
def api_falar():
    """
    Gera áudio da frase usando gTTS (fallback para Web Speech API).

    Query params:
        texto: texto para falar
    """
    texto = request.args.get("texto", "")

    if not texto:
        return jsonify({"erro": "Parâmetro 'texto' é obrigatório"}), 400

    try:
        from gtts import gTTS
        tts = gTTS(text=texto, lang='pt-br')

        # Salvar em arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            arquivo = fp.name

        return send_file(arquivo, mimetype="audio/mpeg", as_attachment=True,
                         download_name="fala.mp3")
    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar áudio: {str(e)}"}), 500


if __name__ == "__main__":
    print("=" * 50)
    print("RELÓGIO DA FALA — Interface Web")
    print("=" * 50)
    print("Acesse: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
