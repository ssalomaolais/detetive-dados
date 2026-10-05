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
top_produtos = df.groupby("produto")["valor_total"].sum().sort_values(ascending=False).head(10)
print(top_produtos)

print("\nFATURAMENTO POR CATEGORIA:")
fat_cat = df.groupby("categoria")["valor_total"].sum().sort_values(ascending=False)
print(fat_cat)

print("\nFATURAMENTO POR CIDADE:")
print(df.groupby("cidade")["valor_total"].sum().sort_values(ascending=False))

print("\nTICKET MÉDIO:", round(df["valor_total"].mean(), 2))

# =============================================================
# GRÁFICO 1 — FATURAMENTO MENSAL COM VALORES
# =============================================================
plt.figure(figsize=(13, 6))
x = np.arange(len(fat_mes))
y = fat_mes.values

plt.plot(x, y, marker="o", color="steelblue", linewidth=2, markersize=8)
plt.fill_between(x, y, alpha=0.15, color="steelblue")

for i, valor in enumerate(y):
    plt.annotate(
        f"R$ {valor/1000:,.0f}k",
        xy=(i, valor),
        xytext=(0, 12),
        textcoords="offset points",
        ha="center",
        fontsize=9,
        fontweight="bold",
        color="darkblue",
    )

plt.xticks(x, [str(p) for p in fat_mes.index], rotation=45)
plt.title("Faturamento Mensal 2024", fontsize=15, fontweight="bold")
plt.ylabel("Faturamento (R$)", fontsize=11)
plt.xlabel("Mês", fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("output/graficos/grafico_faturamento_mensal.png", dpi=150)
plt.close()

# =============================================================
# GRÁFICO 2 — TOP 10 PRODUTOS COM VALORES
# =============================================================
plt.figure(figsize=(12, 7))
top_ordenado = top_produtos.sort_values(ascending=True)
bars = plt.barh(top_ordenado.index, top_ordenado.values, color="coral")

for barra, valor in zip(bars, top_ordenado.values):
    plt.text(
        barra.get_width() + (top_ordenado.max() * 0.01),
        barra.get_y() + barra.get_height() / 2,
        f"R$ {valor/1000:,.0f}k",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="darkred",
    )

plt.title("Top 10 Produtos por Faturamento", fontsize=15, fontweight="bold")
plt.xlabel("Faturamento (R$)", fontsize=11)
plt.xlim(0, top_ordenado.max() * 1.18)
plt.grid(True, axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("output/graficos/grafico_top_produtos.png", dpi=150)
plt.close()

# =============================================================
# GRÁFICO 3 — BOXPLOT COM MÉDIAS
# =============================================================
plt.figure(figsize=(12, 6))
ordem = df.groupby("categoria")["valor_total"].median().sort_values(ascending=False).index
sns.boxplot(data=df, x="categoria", y="valor_total", order=ordem, palette="Set2")

medias = df.groupby("categoria")["valor_total"].mean()
for i, cat in enumerate(ordem):
    media = medias[cat]
    plt.text(
        i, media,
        f"média\nR$ {media:,.0f}",
        ha="center",
        va="bottom",
        fontsize=8,
        fontweight="bold",
        color="darkgreen",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="darkgreen", alpha=0.85),
    )

plt.title("Distribuição de valor_total por Categoria", fontsize=15, fontweight="bold")
plt.ylabel("Valor Total (R$)", fontsize=11)
plt.xlabel("Categoria", fontsize=11)
plt.xticks(rotation=45, ha="right")
plt.grid(True, axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("output/graficos/grafico_boxplot_categoria.png", dpi=150)
plt.close()

# =============================================================
# GRÁFICO 4 — HEATMAP DE CORRELAÇÃO COM VALORES
# =============================================================
plt.figure(figsize=(9, 7))
corr = df[["quantidade", "valor_unitario", "valor_total"]].corr()

sns.heatmap(
    corr,
    annot=True,
    fmt=".3f",
    cmap="coolwarm",
    cbar=True,
    square=True,
    linewidths=2,
    linecolor="white",
    annot_kws={"fontsize": 13, "fontweight": "bold"},
)

plt.title("Correlação entre Variáveis Numéricas", fontsize=15, fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig("output/graficos/grafico_heatmap_correlacao.png", dpi=150)
plt.close()

print("\n>>> Gráficos salvos em output/graficos/")
print(">>> Todos com valores visíveis nos rótulos")
