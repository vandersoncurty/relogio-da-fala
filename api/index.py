"""
Interface Web — Relógio da Fala
Linguagem de Comunicação Alternativa e Aumentativa (CAA)

Aplicação Flask adaptada para Vercel Serverless Functions.
"""

import os
import sys
import tempfile
import requests

# Adicionar o diretório atual ao path para importar gramatica
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, jsonify, request, send_file
from gramatica import POSICOES_PLACA, COMBINACOES_VALIDAS, TRADUCAO, obter_frase

app = Flask(__name__)

# URL da API VLibras
VLBRAS_API_URL = "https://traducao2.vlibras.gov.br/translate"

# URL da API ARASAAC
ARASAAC_API_URL = "https://api.arasaac.org/v1"
ARASAAC_STATIC_URL = "https://static.arasaac.org/pictograms"

# Mapeamento dos símbolos para buscas ARASAAC (em espanhol)
ARASAAC_MAP = {
    "EU": {"busca": "yo", "id": 6632},
    "VOCÊ": {"busca": "tú", "id": 6625},
    "SIM": {"busca": "sí", "id": 5584},
    "NÃO": {"busca": "no", "id": 5526},
    "QUERO": {"busca": "querer", "id": 5441},
    "PRECISO": {"busca": "necesitar", "id": 37160},
    "COMER": {"busca": "comer", "id": 6456},
    "BEBER": {"busca": "beber", "id": 6061},
    "ÁGUA": {"busca": "agua", "id": 32464},
    "COMIDA": {"busca": "comida", "id": 4610},
    "BANHEIRO": {"busca": "baño", "id": 6929},
    "SAIR": {"busca": "salir", "id": 2806},
    "FELIZ": {"busca": "feliz", "id": 9907},
    "TRISTE": {"busca": "triste", "id": 35545},
    "DOR": {"busca": "dolor", "id": 2367},
    "AJUDA": {"busca": "ayuda", "id": 12252}
}


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
    """Valida uma combinação de ponteiros."""
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
    """Gera áudio da frase usando gTTS."""
    texto = request.args.get("texto", "")

    if not texto:
        return jsonify({"erro": "Parâmetro 'texto' é obrigatório"}), 400

    try:
        from gtts import gTTS
        tts = gTTS(text=texto, lang='pt-br')

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            arquivo = fp.name

        return send_file(arquivo, mimetype="audio/mpeg", as_attachment=True,
                         download_name="fala.mp3")
    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar áudio: {str(e)}"}), 500


@app.route("/api/traduzir-libras")
def api_traduzir_libras():
    """Traduz texto para Libras usando a API VLibras."""
    texto = request.args.get("texto", "")

    if not texto:
        return jsonify({"erro": "Parâmetro 'texto' é obrigatório"}), 400

    try:
        response = requests.post(
            VLBRAS_API_URL,
            json={"text": texto, "from": "pt-br"},
            timeout=10
        )

        if response.status_code == 200:
            glosa = response.text.strip()
            return jsonify({
                "texto_original": texto,
                "glosa_libras": glosa,
                "sucesso": True
            })
        else:
            return jsonify({
                "erro": f"Erro na API VLibras: {response.status_code}",
                "sucesso": False
            }), 500
    except requests.exceptions.RequestException as e:
        return jsonify({
            "erro": f"Erro de conexão com VLibras: {str(e)}",
            "sucesso": False
        }), 500


@app.route("/api/pictogramas")
def api_pictogramas():
    """Busca pictogramas na API ARASAAC para todos os símbolos da placa."""
    resultados = {}

    for simbolo, info in ARASAAC_MAP.items():
        busca = info["busca"]
        picto_id = info.get("id")

        if picto_id:
            resultados[simbolo] = {
                "id": picto_id,
                "url": f"{ARASAAC_STATIC_URL}/{picto_id}/{picto_id}_300.png",
                "busca": busca
            }
            continue

        try:
            response = requests.get(
                f"{ARASAAC_API_URL}/pictograms/es/search/{busca}",
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    pictogram = data[0]
                    picto_id = pictogram.get("_id")
                    if picto_id:
                        resultados[simbolo] = {
                            "id": picto_id,
                            "url": f"{ARASAAC_STATIC_URL}/{picto_id}/{picto_id}_300.png",
                            "busca": busca
                        }
                    else:
                        resultados[simbolo] = {"id": None, "url": None, "busca": busca}
                else:
                    resultados[simbolo] = {"id": None, "url": None, "busca": busca}
            else:
                resultados[simbolo] = {"id": None, "url": None, "busca": busca}
        except requests.exceptions.RequestException:
            resultados[simbolo] = {"id": None, "url": None, "busca": busca}

    return jsonify(resultados)
