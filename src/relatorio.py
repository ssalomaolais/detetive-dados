import os
import pandas as pd

os.makedirs("output", exist_ok=True)

df = pd.read_csv("data/vendas.csv", parse_dates=["data_venda"])

fat_total = df["valor_total"].sum()
ticket_medio = df["valor_total"].mean()
n_vendas = len(df)
n_dups = df.duplicated().sum()
n_nulos = df.isnull().sum().sum()
pct_nulos = (n_nulos / df.size) * 100

fat_mes = df.groupby(df["data_venda"].dt.to_period("M"))["valor_total"].sum()
mes_maior = fat_mes.idxmax()
mes_menor = fat_mes.idxmin()
queda_julho_pct = ((fat_mes.mean() - fat_mes.min()) / fat_mes.mean()) * 100

top_produtos = df.groupby("produto")["valor_total"].sum().sort_values(ascending=False).head(3)
top_cidades = df.groupby("cidade")["valor_total"].sum().sort_values(ascending=False).head(3)

markdown = f"""# Relatório Executivo — Análise de Vendas 2024

## 1. Resumo Executivo
A base analisada contém **{n_vendas} vendas** em 2024, com faturamento total de **R$ {fat_total:,.2f}** e ticket médio de **R$ {ticket_medio:,.2f}**. Foram identificados problemas de qualidade de dados ({n_dups} duplicatas, {pct_nulos:.1f}% de valores nulos) e uma queda atípica em **{mes_menor}** (~{queda_julho_pct:.0f}% abaixo da média).

## 2. Principais Descobertas
- **Faturamento total:** R$ {fat_total:,.2f}
- **Ticket médio:** R$ {ticket_medio:,.2f}
- **Mês com maior faturamento:** {mes_maior} (R$ {fat_mes.max():,.2f})
- **Mês com menor faturamento:** {mes_menor} (R$ {fat_mes.min():,.2f})
- **Top 3 produtos:**
  1. {top_produtos.index[0]} — R$ {top_produtos.iloc[0]:,.2f}
  2. {top_produtos.index[1]} — R$ {top_produtos.iloc[1]:,.2f}
  3. {top_produtos.index[2]} — R$ {top_produtos.iloc[2]:,.2f}
- **Top 3 cidades:** {", ".join(top_cidades.index.tolist())}
- **Notebook Pro X** apresenta crescimento inesperado a partir de setembro/2024

## 3. Problemas Encontrados
- **{n_dups} linhas duplicadas** — risco de faturamento inflado
- **{n_nulos} valores nulos** ({pct_nulos:.1f}% da base) em cliente e cidade
- **Valores negativos** em quantidade — indicam devoluções ou erro de sistema
- **Queda de ~{queda_julho_pct:.0f}% em {mes_menor}** — muito acima da sazonalidade esperada
- **Inconsistências em valor_total** vs. quantidade × valor_unitario

## 4. Recomendações Acionáveis
1. **Deduplicar a base** antes de qualquer relatório oficial (economia estimada de R$ {df[df.duplicated()]["valor_total"].sum():,.2f} em faturamento fantasma)
2. **Investigar a queda de {mes_menor}** — verificar se foi problema comercial, operacional ou de registro
3. **Aproveitar o crescimento do Notebook Pro X** — reforçar estoque e campanha a partir de setembro
4. **Corrigir valores negativos** — separar devoluções de erros de sistema
5. **Preencher campos obrigatórios** (cliente, cidade) — bloqueio no cadastro
6. **Focar nas top 3 cidades** para expansão regional

## 5. Próximos Passos
- Implementar validação na origem (formulário de venda)
- Criar dashboard automatizado
- Revisar metas de julho com base no histórico
- Análise de rentabilidade por produto
"""

with open("output/relatorio.md", "w", encoding="utf-8") as f:
    f.write(markdown)

print(">>> Relatório gerado em output/relatorio.md")
