import streamlit as st
import pandas as pd
from datetime import date


# =========================
# CONFIGURAÇÃO GERAL
# =========================
st.set_page_config(
    page_title="Objetivos Diários 2026",
    layout="wide"
)

def gerar_relatorio_html(df_mes, mes_nome):
    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Resumo Mensal</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, Inter, Arial;
                padding: 40px;
                color: #1F2933;
            }}
            h1 {{
                font-size: 22px;
                margin-bottom: 10px;
            }}
            h2 {{
                font-size: 16px;
                margin-top: 30px;
            }}
            p {{
                font-size: 14px;
                color: #4B5563;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                padding: 10px;
                border-bottom: 1px solid #E5E7EB;
                text-align: left;
            }}
            th {{
                background-color: #F9FAFB;
                font-weight: 600;
            }}
        </style>
    </head>
    <body>

    <h1>Resumo Mensal — {mes_nome} 2026</h1>

    <p>Produtividade média: <b>{int(df_mes["Produtividade"].mean() * 100)}%</b></p>
    <p>Dias produtivos: <b>{int((df_mes["Produtividade"] >= 0.7).sum())}</b></p>

    <h2>Hábitos</h2>
    <table>
        <tr><th>Hábito</th><th>Dias cumpridos</th></tr>
    """

    for habito, total in df_mes.sum().items():
        if habito not in ["Produtividade", "Produtivo", "Mês"]:
            html += f"<tr><td>{habito}</td><td>{int(total)}</td></tr>"

    html += """
    </table>
    </body>
    </html>
    """

    return html



st.markdown("""
<style>
/* =========================
   BASE GLOBAL
========================= */
.stApp {
    background-color: #FAFAFA;
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", sans-serif;
    color: #2C2C2C;
}

/* =========================
   CONTAINER
========================= */
.block-container {
    max-width: 520px;
    padding-top: 3rem;
    padding-bottom: 3rem;
}

/* =========================
   TÍTULO PRINCIPAL
========================= */
h1 {
    font-size: 1.8rem;
    font-weight: 600;
    letter-spacing: -0.4px;
    color: #1F2933;
    margin-bottom: 0.3rem;
}

/* =========================
   SUBTÍTULO
========================= */
p {
    font-size: 14px;
    color: #6B7280;
}

/* =========================
   SEÇÕES
========================= */
h2, h3 {
    font-size: 1rem;
    font-weight: 600;
    color: #374151;
    margin-top: 2rem;
}

/* =========================
   INPUT DATA
========================= */
input {
    border-radius: 10px !important;
    border: 1px solid #E5E7EB !important;
    background-color: #FFFFFF !important;
}

/* =========================
   CHECKBOX
========================= */
label {
    font-size: 14px;
    color: #374151;
    line-height: 1.9;
}

/* =========================
   BOTÃO (NEUTRO)
========================= */
.stButton button {
    width: 100%;
    height: 44px;
    border-radius: 10px;
    background-color: #E5E7EB;
    color: #1F2933;
    font-weight: 500;
    border: none;
}

.stButton button:hover {
    background-color: #D1D5DB;
}

/* =========================
   MÉTRICAS (SEM CARA DE CARD)
========================= */
[data-testid="stMetric"] {
    background: transparent;
    padding: 0;
}

[data-testid="stMetric"] > div {
    box-shadow: none;
    border-radius: 0;
}

/* =========================
   DIVISÃO
========================= */
hr {
    margin: 3rem 0;
    border-color: #E5E7EB;
}
</style>
""", unsafe_allow_html=True)


ANO = 2026

OBJETIVOS = [
    "Acordei Cedo",
    "Alimentação Correta",
    "Trabalhei",
    "Academia",
    "Lutei",
    "Creatina",
    "Whey",
    "Estudei",
    "Orei",
    "Fui à Igreja"
]

ARQUIVO = "dados_2026.csv"

# =========================
# INICIALIZAR DADOS
# =========================
if not pd.io.common.file_exists(ARQUIVO):
    datas = pd.date_range(f"{ANO}-01-01", f"{ANO}-12-31")
    df = pd.DataFrame({"Data": datas})
    for obj in OBJETIVOS:
        df[obj] = False
    df.to_csv(ARQUIVO, index=False)

df = pd.read_csv(ARQUIVO, parse_dates=["Data"])

# =========================
# INTERFACE
# =========================
st.title("Acompanhamento de Hábitos — 2026")
st.caption("Registro contínuo de rotina, saúde e disciplina pessoal.")


data_escolhida = st.date_input(
    "Selecione o dia",
    value=date(ANO, 1, 1),
    min_value=date(ANO, 1, 1),
    max_value=date(ANO, 12, 31)
)

if "dia_atual" not in st.session_state:
    st.session_state.dia_atual = data_escolhida

if data_escolhida != st.session_state.dia_atual:
    st.session_state.clear()
    st.session_state.dia_atual = data_escolhida


linha = df[df["Data"] == pd.to_datetime(data_escolhida)].index[0]

st.subheader("✅ Objetivos do Dia")

cols = st.columns(2)  # mais estilo iPhone
novos_valores = {}

for i, obj in enumerate(OBJETIVOS):
    with cols[i % 2]:
        novos_valores[obj] = st.checkbox(
            obj,
            value=bool(df.loc[linha, obj]),
            key=f"{obj}_{data_escolhida}"
        )


# =========================
# SALVAR
# =========================
if st.button("💾 Salvar Dia"):
    for obj, val in novos_valores.items():
        df.loc[linha, obj] = val

    df.to_csv(ARQUIVO, index=False)
    st.info("Registro do dia atualizado.")
    
    # =========================
# INDICADOR DIÁRIO
# =========================
produtividade_dia = sum(novos_valores.values()) / len(OBJETIVOS)

st.metric(
    "Produtividade diária",
    f"{int(produtividade_dia * 100)}%"
)

if produtividade_dia >= 0.7:
    st.write("Status do dia: adequado.")
else:
    st.write("Status do dia: abaixo do esperado.")

# =========================
# VISÃO GERAL
# =========================
st.divider()
st.subheader("📊 Acompanhamento Anual")

df["Produtividade"] = df[OBJETIVOS].sum(axis=1) / len(OBJETIVOS)
df["Produtivo"] = df["Produtividade"] >= 0.7
df["Mês"] = df["Data"].dt.month

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Dias Produtivos", int(df["Produtivo"].sum()))

with col2:
    st.metric("Produtividade Média", f"{int(df['Produtividade'].mean() * 100)}%")

with col3:
    st.metric("Dias Registrados", int((df[OBJETIVOS].sum(axis=1) > 0).sum()))
    
    st.divider()
st.subheader("Resumo Mensal")




mes_escolhido = st.selectbox(
    "Selecione o mês",
    options=range(1, 13),
    format_func=lambda x: [
        "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
        "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
    ][x-1]
)

df_mes = df[df["Data"].dt.month == mes_escolhido]

if not df_mes.empty:
    dias_produtivos = int((df_mes["Produtividade"] >= 0.7).sum())
    produtividade_media = int(df_mes["Produtividade"].mean() * 100)

    habitos_soma = df_mes[OBJETIVOS].sum()
    habito_top = habitos_soma.idxmax()

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Dias Produtivos", dias_produtivos)
        st.metric("Produtividade Média", f"{produtividade_media}%")

    with col2:
        st.metric("Dias Registrados", int((df_mes[OBJETIVOS].sum(axis=1) > 0).sum()))
        st.metric("Hábito Mais Consistente", habito_top)
else:
    st.info("Nenhum dado registrado para este mês.")
    

nomes_meses = [
    "Janeiro","Fevereiro","Março","Abril","Maio","Junho",
    "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"
]

if not df_mes.empty:
    if st.button("Exportar resumo mensal"):
        html = gerar_relatorio_html(df_mes[OBJETIVOS + ["Produtividade"]], nomes_meses[mes_escolhido-1])
        st.download_button(
            label="Baixar relatório",
            data=html,
            file_name=f"Resumo_{nomes_meses[mes_escolhido-1]}_2026.html",
            mime="text/html"
        )


