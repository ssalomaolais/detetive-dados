```markdown
# Uso de IA no Case — Detetive de Dados

## Ferramenta utilizada
Microsoft Copilot (interface web, https://copilot.microsoft.com)
**Motivo:** GitHub Copilot Chat do VS Code estava indisponível na rede corporativa (nenhum modelo aparecia).

## Prompts usados

### Prompt 1 — Geração do dataset sintético
- **Texto:** script Python com pandas/numpy para gerar 800 linhas de vendas em 2024, inserindo propositalmente ~30 duplicatas, ~40 nulos em cliente/cidade, valores negativos, queda de ~60% em julho e crescimento de "Notebook Pro X" a partir de setembro, com seed 42.
- **Por quê:** precisava de um CSV "sujo" controlado para treinar detecção de problemas.
- **Resultado:** lógica correta, mas retornou o código sem quebras de linha (tudo achatado) — precisei reformatar manualmente.

### Prompt 2 — Análise exploratória
- **Texto:** script analise.py com shape, dtypes, describe, nulos, duplicatas, quantidade < 0, valores inconsistentes, faturamento por mês/produto/categoria/cidade e ticket médio.
- **Por quê:** base para todas as decisões seguintes.
- **Resultado:** funcionou bem após ajuste de formatação.

### Prompt 3 — Insights
- **Texto:** análise sênior pedindo inconsistências, outliers, tendências, oportunidades e alertas com números exatos.
- **Por quê:** gerar interpretação qualificada dos dados.
- **Resultado:** identificou corretamente a queda de julho e o domínio do Notebook Pro X, mas generalizou em algumas recomendações.

### Prompt 4 — Gráficos
- **Texto:** 4 gráficos (linha mensal, top produtos, boxplot por categoria, heatmap de correlação) salvos em PNG 150dpi.
- **Resultado:** funcionou sem ajustes relevantes.

### Prompt 5 — Relatório executivo
- **Texto:** script que gera Markdown com Resumo, Descobertas, Problemas, Recomendações, Próximos Passos, com todos os números calculados do dataframe.
- **Resultado:** estrutura boa, mas algumas recomendações vieram genéricas ("melhorar vendas") — reescrevi para citar métricas específicas.

## O que a IA acertou
- Lógica do dataset sintético com seed fixo (reprodutibilidade)
- Estrutura organizada da análise exploratória
- Identificação correta da queda de julho e do crescimento do Notebook Pro X
- Estrutura profissional do relatório executivo

## O que a IA errou
- Retornou o código sem indentação/quebras de linha (precisei reconstruir)
- Recomendações iniciais genéricas, sem citar números
- Esqueceu em um dos prompts de tratar `data_venda` como datetime

## Ajustes manuais feitos
- Reformatação completa do código do gerador
- Adição de `parse_dates=['data_venda']` na leitura do CSV
- Reescrita das recomendações para incluir métricas exatas
- Garantia de que nenhum número no relatório fosse hardcoded
