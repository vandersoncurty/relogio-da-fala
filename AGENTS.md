# AGENTS.md

Python project "Relógio da Fala" — an AAC (CAA) communication board. Core is a small compiler pipeline (scanner → parser) over a fixed grammar of 16 symbols / 102 valid combinations, with three frontends (Flask web, pygame desktop, terminal). UI and docs are in Brazilian Portuguese.

## Commands

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt   # setup
.venv/bin/python webapp/app.py         # Flask local :5000 (só API; a página vem SEM css/js → use vercel dev p/ UI)
.venv/bin/python main.py texto         # terminal mode
.venv/bin/python main.py interface     # pygame GUI (needs a display; fails headless)
.venv/bin/pytest testes/testar_tudo.py -v                          # all tests
.venv/bin/pytest 'testes/testar_tudo.py::testar_parser' -v         # single test
.venv/bin/python main.py testes        # same tests, readable pt-BR summary

# Vercel local — a forma completa (CSS/JS/rotas funcionando, como em produção)
vercel link -p relogio-da-fala -y      # 1x por clone (autentique antes com `vercel login`)
vercel dev --listen tcp://0.0.0.0:3002 # --port está deprecado; o esquema precisa ser tcp:// (não http://)
```

- **Never trust exit codes for tests.** Test functions (`testar_*`) only print ✓/✗ and `return` a bool — no asserts. pytest collects them (names match `test*`) and reports "4 passed" even when internal checks printed ✗; it just emits `PytestReturnNotNoneWarning`. `main.py testes` also exits 0 on failure. The only pass/fail signal is the printed summary (`TODOS OS TESTES PASSARAM` vs `✗ FALHOU`).
- There is no lint, formatter, typecheck, codegen, or CI config. Only `requirements.txt` (no pyproject). Don't invent verification steps.
- Tests are pure/in-process (no network, no services).
- **`vercel dev` exige `uv` no PATH** — o `python3` do sistema não tem pip, então o builder falha com `uv is required ... No module named pip`. Instale uma vez: `curl -LsSf https://astral.sh/uv/install.sh | sh` (instala `~/.local/bin/uv`) e garanta `~/.local/bin` no PATH do shell que roda o `vercel dev`.

## Vercel — como funciona de verdade

`vercel.json` é **moderno/zero-config**: `outputDirectory: "public"` + rewrite `/(.*)` → `/api/index`. Verificado com `vercel build` (após `vercel pull --yes --environment preview`): `.vercel/output/static/` recebe o conteúdo de `public/` e o config compilado serve **filesystem primeiro**, depois a função. Não reverter para `version:2` + `builds`: esse pipeline legado gera saída **sem arquivos estáticos** — o CSS/JS quebraria no próximo deploy (o deploy de produção atual só funciona porque é antigo).

**Sync map — edições devem ser replicadas nas cópias** (estão em sincronia):

| Canonical (local) | Deploy copy (Vercel) |
|---|---|
| `gramatica.py` | `api/gramatica.py` (idêntico; `api/index.py` importa a cópia local) |
| `webapp/app.py` | `api/index.py` (equivalente; diferem em docstrings/`sys.path`/1 var) |
| `webapp/templates/*` | `public/templates/*` |
| `webapp/static/{css,js}/*` | `public/{css,js}/*` |

Quirks verificados (não são regressões suas):

- `api/index.py` cria o Flask com `template_folder=<raiz>/webapp/templates` — **o bundle da função exclui `public/`** (é o outputDirectory), então `render_template` lê de `webapp/templates`. Não "simplifique" de volta para `Flask(__name__)`: volta o `TemplateNotFound` (500 no `/`).
- Os templates usam caminhos absolutos `/css/` e `/js/` (sem `url_for`); `vercel dev` e o deploy resolvem via filesystem. Rodando `webapp/app.py` direto no Flask, esses paths dão **404 e a página vem sem estilo** — para a UI completa localmente, use `vercel dev`.

## Architecture notes

- `gramatica.py` is the single source of truth: `POSICOES_PLACA` (16 symbols), `COMBINACOES_VALIDAS` (102 pairs), `TRADUCAO`, `obter_frase(p1, p2)`. The web APIs (`/api/validar`, `/api/combinacoes`) read it directly — no DB.
- Flow: `scanner.escanear_frase` normalizes (lowercase, strips accents — `"Eu quero agua"` is accepted) → `parser.Parser.parse_frase` (recursive descent; raises `SyntaxError`, lexer raises `RuntimeError`).
- Root `parser.py` is project code, not stdlib.
- All scripts use `sys.path.insert(...)` hacks — run them from the repo root (commands above already do).
- External APIs: `/api/falar` (gTTS) and `/api/traduzir-libras` (VLibras) need internet; `/api/pictogramas` uses hardcoded ARASAAC IDs and is effectively offline.

## Conventions

- Keep all strings, comments, and docs in Brazilian Portuguese to match the codebase.
- Commit subjects use a bracketed prefix: `[feat]`, `[fix]`, `[refactor]` (not `feat:`).
- The README is partly stale: it says `cd projeto_de_linguagens` (directory doesn't exist — run from repo root) and its file tree predates the Vercel restructure (missing `api/`, `public/`, `vercel.json`). Trust the code over the README.
