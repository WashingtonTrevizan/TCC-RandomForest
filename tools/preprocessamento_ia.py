# preprocessamento_ia.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from joblib import dump
import os

# Carregar dataset tratado
df = pd.read_csv("data/dataset_final.csv")

# Definir features (garanta que todas existem no CSV)
required_features = [
    'flow_duration', 'packet_rate', 'byte_rate', 
    'src_ip_count', 'dst_ip_count', 'tcp_syn',
    'length', 'dst_port', 'protocol'
]
required_columns = ["Label"] + required_features

# Verificar colunas
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Coluna faltante: {col}")

# Codificar coluna 'protocol' (TCP -> 1, UDP -> 2, outros -> 0)
df['protocol'] = df['protocol'].map({'TCP': 1, 'UDP': 2}).fillna(0)

# Codificar labels (BENIGN/DDoS)
encoder = LabelEncoder()
df["Label_encoded"] = encoder.fit_transform(df["Label"])

# Tratar valores nulos/infinitos
df[required_features] = df[required_features].replace([np.inf, -np.inf], np.nan).fillna(0)

# Normalizar features
scaler = StandardScaler()
df[required_features] = scaler.fit_transform(df[required_features])

# Salvar artefatos
os.makedirs("data", exist_ok=True)
df.to_csv("data/dataset_preprocessado.csv", index=False)

os.makedirs("model", exist_ok=True)
dump(scaler, "model/scaler.joblib")
dump(encoder, "model/encoder.joblib")
print("[✅] Pré-processamento concluído!")