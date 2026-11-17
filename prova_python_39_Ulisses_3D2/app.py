import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Veículos de Montes Claros", layout="wide")

CIDADE = "Montes Claros"
st.title(f"Frota de Veículos - {CIDADE}")

# Lê o arquivo CSV
df = pd.read_csv("numero_veiculos.csv", sep=None, engine="python")
df.columns = df.columns.str.strip()

# Pega o nome exato da coluna de cidade/município
cols_cidade = [c for c in df.columns if "munic" in c.lower() or "cidade" in c.lower() or "local" in c.lower()]
col_cidade = cols_cidade[0] if cols_cidade else df.columns[0]

# Filtra apenas a cidade de Montes Claros
df_filtrado = df[df[col_cidade].astype(str).str.strip().str.lower() == CIDADE.lower()].copy()

# Verifica como a tabela está organizada (formato longo ou formato largo)
cols_tipo = [c for c in df.columns if "tipo" in c.lower() or "veic" in c.lower() or "veíc" in c.lower() or "categ" in c.lower()]
cols_qtd = [c for c in df.columns if "quant" in c.lower() or "total" in c.lower() or "valor" in c.lower() or "qtd" in c.lower()]

if cols_tipo and cols_qtd:
    # Formato 1: Uma coluna para Tipo e outra para Quantidade
    col_tipo = cols_tipo[0]
    col_qtd = cols_qtd[0]
    df_filtrado[col_qtd] = pd.to_numeric(df_filtrado[col_qtd], errors="coerce").fillna(0)
    tabela_final = df_filtrado[[col_tipo, col_qtd]].rename(
        columns={col_tipo: "Tipo de Veículo", col_qtd: "Quantidade"}
    )
else:
    # Formato 2: Cada tipo de veículo é uma coluna (ex: Automóvel, Motocicleta, etc.)
    outras_cols = [c for c in df.columns if c != col_cidade and "cod" not in c.lower() and "cód" not in c.lower() and "uf" != c.lower() and "estado" not in c.lower() and "total" not in c.lower()]
    tabela_final = df_filtrado[outras_cols].melt(var_name="Tipo de Veículo", value_name="Quantidade")
    tabela_final["Quantidade"] = pd.to_numeric(tabela_final["Quantidade"], errors="coerce").fillna(0)

# Cria a barra lateral na esquerda
st.sidebar.title("Menu")
tela = st.sidebar.radio("Escolha a tela:", ["Tabela", "Gráfico"])

# Mostra a tela escolhida
if tela == "Tabela":
    st.subheader(f"Tabela de Veículos em {CIDADE}")
    st.dataframe(tabela_final, use_container_width=True, hide_index=True)

elif tela == "Gráfico":
    st.subheader(f"Gráfico de Pizza - Veículos em {CIDADE}")
    fig = px.pie(
        tabela_final,
        names="Tipo de Veículo",
        values="Quantidade",
        title=f"Distribuição de Veículos em {CIDADE}"
    )
    st.plotly_chart(fig, use_container_width=True)
