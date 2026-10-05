import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("output/graficos", exist_ok=True)

df = pd.read_csv("data/vendas.csv", parse_dates=["data_venda"])

print("=" * 60)
print("SHAPE:", df.shape)
print("=" * 60)
print("\nDTYPES:\n", df.dtypes)
print("\nDESCRIBE:\n", df.describe())
print("\nNULOS:\n", df.isnull().sum())
print("\nDUPLICATAS EXATAS:", df.duplicated().sum())
print("\nQUANTIDADE < 0:", (df["quantidade"] < 0).sum())

df["valor_calc"] = (df["quantidade"] * df["valor_unitario"]).round(2)
incons = (df["valor_total"] - df["valor_calc"]).abs() > 0.01
print("VALOR_TOTAL INCONSISTENTE:", incons.sum())

print("\nFATURAMENTO POR MÊS:")
fat_mes = df.groupby(df["data_venda"].dt.to_period("M"))["valor_total"].sum()
print(fat_mes)

print("\nTOP 10 PRODUTOS:")
print(df.groupby("produto")["valor_total"].sum().sort_values(ascending=False).head(10))

print("\nFATURAMENTO POR CATEGORIA:")
print(df.groupby("categoria")["valor_total"].sum().sort_values(ascending=False))

print("\nFATURAMENTO POR CIDADE:")
print(df.groupby("cidade")["valor_total"].sum().sort_values(ascending=False))

print("\nTICKET MÉDIO:", round(df["valor_total"].mean(), 2))

# GRÁFICOS
plt.figure(figsize=(10, 5))
fat_mes.plot(kind="line", marker="o")
plt.title("Faturamento Mensal 2024")
plt.ylabel("R$")
plt.tight_layout()
plt.savefig("output/graficos/grafico_faturamento_mensal.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
top = df.groupby("produto")["valor_total"].sum().sort_values().tail(10)
top.plot(kind="barh")
plt.title("Top 10 Produtos por Faturamento")
plt.tight_layout()
plt.savefig("output/graficos/grafico_top_produtos.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
sns.boxplot(data=df, x="categoria", y="valor_total")
plt.xticks(rotation=45)
plt.title("Boxplot valor_total por Categoria")
plt.tight_layout()
plt.savefig("output/graficos/grafico_boxplot_categoria.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 6))
sns.heatmap(df[["quantidade", "valor_unitario", "valor_total"]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlação")
plt.tight_layout()
plt.savefig("output/graficos/grafico_heatmap_correlacao.png", dpi=150)
plt.close()

print("\n>>> Gráficos salvos em output/graficos/")
