# Relógio da Fala

## Linguagem de Comunicação Alternativa e Aumentativa (CAA) e Testador em Python para Comunicação Acessível e Validação Formal

---

### Descrição

Placa de CAA em formato de relógio com 16 símbolos e dois ponteiros independentes, permitindo que pessoas com necessidades comunicativas complexas expressem necessidades básicas e emocionais por meio de combinações visuais. O projeto inclui versão digital (desktop e web) e planejamento de placa física.

### Tipo de Projeto

**Extensionista** — O projeto foi desenvolvido com base em entrevista real com pais de criança autista não verbal, identificando necessidades comunicativas reais da comunidade.

### Público-Alvo

- Crianças com Transtorno do Espectro Autista (TEA)
- Idosos com dificuldades comunicacionais

### Funcionalidades

- **16 símbolos** organizados em 4 quadrantes (sujeitos, verbos, objetos, emoções)
- **102 combinações válidas** definidas por gramática BNF/EBNF
- **Interface desktop** com pygame-ce (ponteiros arrastáveis)
- **Interface web** com Flask, Canvas interativo e design responsivo
- **Síntese de voz** via gTTS (online) e pyttsx3 (offline)
- **VLibras** — avatar em Libras para pessoas surdas
- **ARASAAC** — 16 pictogramas visuais para comunicação por imagens
- **Validação automática** de combinações (scanner + parser)

### Estrutura do Projeto

```
projeto_de_linguagens/
├── gramatica.py              # Definição BNF/EBNF e 102 combinações
├── scanner.py                # Analisador léxico (regex)
├── parser.py                 # Analisador sintático descendente recursivo
├── interface.py              # Interface gráfica desktop (pygame-ce)
├── voz.py                    # Síntese de voz (gTTS + pyttsx3)
├── main.py                   # Ponto de entrada principal
├── requirements.txt          # Dependências Python
├── README.md                 # Este arquivo
├── arquivos_apoio/
│   ├── relatorio.md          # Relatório do projeto (markdown)
│   ├── relatorio.docx        # Relatório do projeto (Word)
│   ├── gerar_docx.py         # Script para gerar .docx
│   └── normas_abnt.md        # Normas ABNT de formatação
├── testes/
│   └── testar_tudo.py        # Testes automatizados (30 casos)
└── webapp/
    ├── app.py                # Aplicação Flask (rotas + API)
    ├── templates/
    │   ├── base.html         # Template base com VLibras Widget
    │   └── index.html        # Página principal com relógio
    └── static/
        ├── css/
        │   └── style.css     # Dark theme, glassmorphism, responsivo
        └── js/
            └── clock.js      # Canvas interativo + pictogramas
```

### Como Executar

#### Pré-requisitos

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

#### Interface Web (recomendado)

```bash
cd projeto_de_linguagens
.venv/bin/python3 webapp/app.py
# Acesse http://localhost:5000
```

#### Interface Desktop

```bash
cd projeto_de_linguagens
.venv/bin/python3 main.py interface
```

#### Modo Texto (Terminal)

```bash
cd projeto_de_linguagens
.venv/bin/python3 main.py texto
```

#### Executar Testes

```bash
cd projeto_de_linguagens
.venv/bin/pytest testes/testar_tudo.py -v
```

### Dependências

- Python 3.8+
- pygame-ce — interface gráfica desktop
- Flask — interface web
- gTTS — síntese de voz online (voz natural)
- pyttsx3 — síntese de voz offline (fallback)
- python-docx — geração do relatório em .docx

### Gramática BNF

```bnf
<frase> ::= <combinacao>
<combinacao> ::= <ponteiro1> <ponteiro2>
<ponteiro1> ::= <SUJEITO> | <EMOCAO>
<ponteiro2> ::= <VERBO> | <OBJETO> | <ESTADO>
<SUJEITO> ::= "Eu" | "Você"
<VERBO> ::= "quero" | "preciso" | "comer" | "beber"
<OBJETO> ::= "água" | "comida" | "banheiro" | "sair"
<EMOCAO> ::= "feliz" | "triste" | "dor" | "ajuda"
<ESTADO> ::= "sim" | "não"
```

### Integrações

| Tecnologia | Função |
|---|---|
| **Flask** | Backend web com API REST |
| **VLibras** | Avatar 3D traduzindo para Libras |
| **ARASAAC** | 16 pictogramas CAA (CC BY-NC-SA) |
| **gTTS** | Síntese de voz Google (online) |
| **Web Speech API** | Síntese de voz do navegador |

### Referências

- ARASAAC. **Pictogramas: Comunicação Aumentativa e Alternativa.** s.d. https://arasaac.org/
- BEUKELMAN, David R.; LIGHT, Janice C. **Augmentative & Alternative Communication.** 5. ed. Baltimore: Paul H. Brookes Publishing Co., 2020.
- BRASIL. **Lei nº 13.146, de 6 de julho de 2015.** Lei Brasileira de Inclusão da Pessoa com Deficiência.
- HOPCROFT, John E.; MOTWANI, Rajeev; ULLMAN, Jeffrey D. **Introduction to Automata Theory, Languages, and Computation.** 3. ed. Boston: Addison-Wesley, 2006.
- ISAAC BRASIL. **Comunicação Aumentativa e Alternativa.** s.d. https://www.isaacbrasil.org.br/
- ISO/IEC 14977:1996. **Information technology — Syntactic metalanguage — Extended BNF.**
- VLIBRAS. **VLibras: Tradução automática para tornar a Web mais acessível.** s.d. https://www.vlibras.gov.br/
- W3C. **Web Content Accessibility Guidelines (WCAG) 2.2.** W3C Recommendation, 5 out. 2023.

### Licença

Projeto acadêmico — Uso educacional.
