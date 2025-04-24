import pandas as pd
import numpy as np
from joblib import load
import sys

# Carregar scaler, encoder e modelo
scaler = load("model/scaler.joblib")
encoder = load("model/encoder.joblib")
from joblib import load
model = load("model/ddos_model.pkl")


csv_entrada = sys.argv[1]
csv_saida = sys.argv[2] if len(sys.argv) > 2 else "data/resultados_inferencia.csv"
df = pd.read_csv(csv_entrada)

def calcular_features(df):
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['flow_duration'] = df.groupby(['src_ip', 'dst_ip'])['timestamp'].transform(
            lambda x: (x.max() - x.min()).total_seconds()
        )
    else:
        df['flow_duration'] = 0

    df['packet_rate'] = df.groupby(['src_ip', 'dst_ip'])['length'].transform('count') / (df['flow_duration'] + 1e-6)
    df['byte_rate'] = df.groupby(['src_ip', 'dst_ip'])['length'].transform('sum') / (df['flow_duration'] + 1e-6)
    df['src_ip_count'] = df.groupby('src_ip')['src_ip'].transform('count')
    df['dst_ip_count'] = df.groupby('dst_ip')['dst_ip'].transform('count')

    if 'tcp_flags' in df.columns:
        df['tcp_syn'] = df['tcp_flags'].apply(lambda x: 1 if x & 0x02 else 0)
    else:
        df['tcp_syn'] = 0

    return df

def preprocessar(df):
    required_features = [
        'flow_duration', 'packet_rate', 'byte_rate', 
        'src_ip_count', 'dst_ip_count', 'tcp_syn',
        'length', 'dst_port', 'protocol'
    ]

    df['protocol'] = df['protocol'].map({'TCP': 1, 'UDP': 2}).fillna(0)
    df[required_features] = df[required_features].replace([np.inf, -np.inf], np.nan).fillna(0)
    df[required_features] = scaler.transform(df[required_features])

    return df, required_features

# Execução
print("[INFO] Calculando features...")
df = calcular_features(df)

print("[INFO] Pré-processando dados...")
df, features = preprocessar(df)

print("[INFO] Realizando previsões...")
predicoes = model.predict(df[features])

label_map = {
    0: 'Benign',
    1: 'HTTP-Flood',
    2: 'SYN-Flood',
    3: 'UDP-Flood'
}

df['Predito'] = [label_map.get(i, "Desconhecido") for i in predicoes]

print(df[['src_ip', 'dst_ip', 'protocol', 'Predito']].head())

df.to_csv("data/resultados_inferencia.csv", index=False)
df.to_csv(csv_saida, index=False)
print("[✅] Resultados salvos em: data/resultados_inferencia.csv")

