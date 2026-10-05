import os
import numpy as np
import pandas as pd

# Reprodutibilidade
np.random.seed(42)

# Criar pasta data/
os.makedirs("data", exist_ok=True)

# Configurações
n_base = 770  # 770 linhas originais + 30 duplicadas = 800 linhas finais
produtos = [
    "Notebook Pro X", "Mouse Gamer", "Teclado Mecânico", "Monitor 24",
    "Headset Pro", "Webcam HD", "Impressora Laser", "SSD 1TB",
    "Cadeira Office", "Dock Station",
]
categoria_map = {
    "Notebook Pro X": "Notebook",
    "Mouse Gamer": "Periférico",
    "Teclado Mecânico": "Periférico",
    "Monitor 24": "Monitor",
    "Headset Pro": "Áudio",
    "Webcam HD": "Vídeo",
    "Impressora Laser": "Impressão",
    "SSD 1TB": "Armazenamento",
    "Cadeira Office": "Móveis",
    "Dock Station": "Acessórios",
}
preco_map = {
    "Notebook Pro X": 8500,
    "Mouse Gamer": 180,
    "Teclado Mecânico": 350,
    "Monitor 24": 1100,
    "Headset Pro": 420,
    "Webcam HD": 280,
    "Impressora Laser": 1600,
    "SSD 1TB": 550,
    "Cadeira Office": 1200,
    "Dock Station": 450,
}
clientes = [f"Cliente_{i:03d}" for i in range(1, 201)]
cidades = [
    "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba",
    "Porto Alegre", "Campinas", "Salvador", "Recife", "Fortaleza", "Brasília",
]
meses = np.arange(1, 13)

# Julho com queda de ~60%
pesos_mes = np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.4, 1.0, 1.0, 1.0, 1.0, 1.0])
pesos_mes = pesos_mes / pesos_mes.sum()

rows = []
for _ in range(n_base):
    mes = np.random.choice(meses, p=pesos_mes)
    inicio_mes = pd.Timestamp(year=2024, month=int(mes), day=1)
    fim_mes = inicio_mes + pd.offsets.MonthEnd(1)

    data_venda = inicio_mes + pd.Timedelta(
        days=np.random.randint(0, (fim_mes - inicio_mes).days + 1)
    )

    # Crescimento inesperado do Notebook Pro X a partir de setembro
    if mes >= 9:
        produtos_ajustados = (
            ["Notebook Pro X"] * 8 +
            [p for p in produtos if p != "Notebook Pro X"]
        )
    else:
        produtos_ajustados = produtos

    produto = np.random.choice(produtos_ajustados)
    categoria = categoria_map[produto]

    cliente = np.random.choice(clientes)
    cidade = np.random.choice(cidades)

    quantidade = np.random.randint(1, 8)
    valor_unitario = preco_map[produto] * np.random.uniform(0.85, 1.15)
    valor_total = quantidade * valor_unitario

    rows.append([
        data_venda,
        produto,
        categoria,
        cliente,
        cidade,
        quantidade,
        round(valor_unitario, 2),
        round(valor_total, 2),
    ])

df = pd.DataFrame(
    rows,
    columns=[
        "data_venda", "produto", "categoria", "cliente", "cidade",
        "quantidade", "valor_unitario", "valor_total",
    ],
)

# 1. Inserir ~30 linhas duplicadas exatas
duplicadas = df.sample(n=30, random_state=42)
df = pd.concat([df, duplicadas], ignore_index=True)

# 2. Inserir ~40 valores nulos em cliente e cidade
idx_cliente_null = np.random.choice(df.index, size=40, replace=False)
idx_cidade_null = np.random.choice(df.index, size=40, replace=False)
df.loc[idx_cliente_null, "cliente"] = np.nan
df.loc[idx_cidade_null, "cidade"] = np.nan

# 3. Inserir alguns valores negativos em quantidade
idx_negativos = np.random.choice(df.index, size=15, replace=False)
df.loc[idx_negativos, "quantidade"] *= -1

# Recalcular valor_total após alterações de quantidade
df["valor_total"] = (df["quantidade"] * df["valor_unitario"]).round(2)

# Embaralhar linhas
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Salvar CSV
arquivo_saida = "data/vendas.csv"
df.to_csv(arquivo_saida, index=False, encoding="utf-8-sig")

# Exibir informações
print("Shape:", df.shape)
print("\nColunas:")
print(df.columns.tolist())
print("\nPrimeiras 5 linhas:")
print(df.head())
