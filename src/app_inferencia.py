import streamlit as st
import pandas as pd
import os
import uuid
import subprocess
import plotly.express as px

st.set_page_config(page_title="Detector de Ataques DDoS", layout="wide")
st.title("🛡️ DDoS Detection via IA")

uploaded_file = st.file_uploader("Faça upload de um CSV de tráfego de rede", type=["csv"])

if uploaded_file:
    # Gerar caminhos únicos
    file_id = str(uuid.uuid4())
    csv_path = f"data/pcap_convertido_{file_id}.csv"
    resultado_path = f"data/resultados_inferencia_{file_id}.csv"

    with open(csv_path, "wb") as f:
        f.write(uploaded_file.read())

    st.info("Executando inferência... Isso pode levar alguns segundos...")

    try:
        # Rodar inferência (ajuste o inferencia_ddos.py para aceitar argumentos)
        subprocess.run(
            ["python", "tools/inferencia_ddos.py", csv_path, resultado_path],
            check=True
        )

        if os.path.exists(resultado_path):
            df = pd.read_csv(resultado_path)

            st.success("✅ Inferência concluída!")
            st.subheader("📄 Resultados em Tabela")
            st.dataframe(df)

            # GRÁFICO 📊
            st.subheader("📊 Distribuição dos tipos de tráfego detectados")
            contagem = df["Predito"].value_counts().reset_index()
            contagem.columns = ["Tipo de Tráfego", "Quantidade"]

            fig = px.bar(contagem, x="Tipo de Tráfego", y="Quantidade",
                         color="Tipo de Tráfego",
                         title="Distribuição dos Rótulos Preditos",
                         text="Quantidade")
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("❌ Arquivo de resultados não encontrado.")
    except subprocess.CalledProcessError:
        st.error("❌ Erro ao executar a inferência.")
