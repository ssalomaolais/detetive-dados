# Relatório Executivo — Análise de Vendas 2024

## 1. Resumo Executivo
A base analisada contém **800 vendas** em 2024, com faturamento total de **R$ 7,794,579.36** e ticket médio de **R$ 9,743.22**. Foram identificados problemas de qualidade de dados (23 duplicatas, 1.2% de valores nulos) e uma queda atípica em **2024-07** (~78% abaixo da média).

## 2. Principais Descobertas
- **Faturamento total:** R$ 7,794,579.36
- **Ticket médio:** R$ 9,743.22
- **Mês com maior faturamento:** 2024-10 (R$ 1,356,001.76)
- **Mês com menor faturamento:** 2024-07 (R$ 139,902.08)
- **Top 3 produtos:**
  1. Notebook Pro X — R$ 6,129,080.70
  2. Impressora Laser — R$ 473,036.68
  3. Cadeira Office — R$ 350,364.81
- **Top 3 cidades:** Curitiba, Salvador, Rio de Janeiro
- **Notebook Pro X** apresenta crescimento inesperado a partir de setembro/2024

## 3. Problemas Encontrados
- **23 linhas duplicadas** — risco de faturamento inflado
- **80 valores nulos** (1.2% da base) em cliente e cidade
- **Valores negativos** em quantidade — indicam devoluções ou erro de sistema
- **Queda de ~78% em 2024-07** — muito acima da sazonalidade esperada
- **Inconsistências em valor_total** vs. quantidade × valor_unitario

## 4. Recomendações Acionáveis
1. **Deduplicar a base** antes de qualquer relatório oficial (economia estimada de R$ 157,688.32 em faturamento fantasma)
2. **Investigar a queda de 2024-07** — verificar se foi problema comercial, operacional ou de registro
3. **Aproveitar o crescimento do Notebook Pro X** — reforçar estoque e campanha a partir de setembro
4. **Corrigir valores negativos** — separar devoluções de erros de sistema
5. **Preencher campos obrigatórios** (cliente, cidade) — bloqueio no cadastro
6. **Focar nas top 3 cidades** para expansão regional

## 5. Próximos Passos
- Implementar validação na origem (formulário de venda)
- Criar dashboard automatizado
- Revisar metas de julho com base no histórico
- Análise de rentabilidade por produto
