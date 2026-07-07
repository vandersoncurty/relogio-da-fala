# Relógio da Fala

## Linguagem de Comunicação Alternativa e Aumentativa (CAA) e Testador em Python para Comunicação Acessível e Validação Formal

---

### Descrição

Placa de CAA em formato de relógio com 16 símbolos e dois ponteiros independentes, permitindo que pessoas com necessidades comunicativas complexas expressem necessidades básicas e emocionais por meio de combinações visuais.

### Público-Alvo

- Crianças com Transtorno do Espectro Autista (TEA)
- Idosos com dificuldades comunicacionais

### Estrutura do Projeto

```
projeto/
├── gramatica.py          # Definição BNF/EBNF e tokens
├── scanner.py            # Analisador léxico
├── parser.py             # Analisador sintático
├── interface.py          # Interface gráfica (pygame)
├── voz.py                # Síntese de voz
├── main.py               # Ponto de entrada principal
├── relatorio.md          # Relatório do projeto
├── normas_abnt.md        # Normas ABNT de formatação
├── README.md             # Este arquivo
├── placa_fisica/         # Arquivos da placa física
│   └── (a definir)
└── testes/               # Testes automatizados
    └── testar_tudo.py
```

### Como Executar

#### Modo Texto (Terminal)

```bash
cd projeto
python main.py texto
```

#### Executar Testes

```bash
cd projeto
python main.py testes
```

#### Interface Gráfica

```bash
cd projeto
pip install pygame
python main.py interface
```

### Dependências

- Python 3.8+
- pygame-ce (para interface gráfica)
- gTTS (para síntese de voz - online, voz natural)
- pyttsx3 (alternativa offline - voz robótica)

### Instalação das Dependências

```bash
pip install pygame-ce gTTS pyttsx3
```

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

### Referências

- BEUKELMAN, David R.; LIGHT, Janice C. **Augmentative & Alternative Communication.** 5. ed. Baltimore: Paul H. Brookes Publishing Co., 2020.
- HOPCROFT, John E.; MOTWANI, Rajeev; ULLMAN, Jeffrey D. **Introduction to Automata Theory, Languages, and Computation.** 3. ed. Boston: Addison-Wesley, 2006.
- ISO/IEC 14977:1996. **Information technology — Syntactic metalanguage — Extended BNF.** Genebra: ISO/IEC, 1996.
- W3C. **Web Content Accessibility Guidelines (WCAG) 2.2.** W3C Recommendation, 5 out. 2023.
- BRASIL. **Lei nº 13.146, de 6 de julho de 2015.** Lei Brasileira de Inclusão da Pessoa com Deficiência.

### Licença

Projeto acadêmico — Uso educacional.
