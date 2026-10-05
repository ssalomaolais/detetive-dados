# Detetive de Dados — Análise de Vendas 2024

Projeto Python que analisa uma base de vendas, identifica inconsistências, outliers e oportunidades de negócio, e gera relatório executivo automatizado.

## Estrutura
- `data/vendas.csv` — dataset gerado com problemas propositais
- `src/gerar_dataset.py` — gera o CSV
- `src/analise.py` — EDA + 4 gráficos
- `src/relatorio.py` — gera relatório executivo em Markdown
- `output/graficos/` — PNGs dos gráficos
- `output/relatorio.md` — relatório final
- `IA.md` — documentação do uso de IA

## Como rodar
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/gerar_dataset.py
python src/analise.py
python src/relatorio.py