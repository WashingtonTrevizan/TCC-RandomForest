# preprocessamento_realista.py
import pandas as pd
import numpy as np
import time
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder, StandardScaler
from joblib import dump
import os
import sys

# Importar configurações padronizadas
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core.feature_engineering import REQUIRED_FEATURES, validate_dataframe

def preprocessar_dataset_realista():
    print("🔧 PREPROCESSAMENTO DO DATASET REALISTA")
    print("="*50)
    
    # Carregar dataset realista
    with tqdm(total=1, desc="📂 Carregando dataset", unit="arquivo") as pbar:
        df = pd.read_csv("data/processed/dataset_realista.csv")
        pbar.update(1)
    
    print(f"[INFO] Dataset shape: {df.shape}")
    print(f"[INFO] Colunas disponíveis: {list(df.columns)}")
    
    # Verificar se todas as colunas necessárias existem
    required_columns = REQUIRED_FEATURES + ["Label"]
    validate_dataframe(df, required_columns)
    
    # Verificar distribuição de labels
    print(f"[INFO] Distribuição de labels:")
    print(df["Label"].value_counts())
    
    # Mapeamento de labels atualizado
    LABEL_MAPPING_REALISTA = {
        'Benign': 0,
        'UDP-Flood': 1, 
        'SYN-Flood': 2,
        'HTTP-Flood': 3,
        'DDoS-Other': 4
    }
    
    # Processamento com barra de progresso
    with tqdm(total=6, desc="⚙️ Processando dados", unit="etapa") as pbar:
        # Codificar labels
        pbar.set_description("🏷️ Mapeando labels...")
        df["Label_encoded"] = df["Label"].map(LABEL_MAPPING_REALISTA)
        pbar.update(1)
        
        # Verificar se houve problemas no mapeamento
        if df["Label_encoded"].isna().any():
            print("[WARN] Alguns labels não foram mapeados corretamente!")
            print("Labels únicos encontrados:", df["Label"].unique())
            print("Labels esperados:", list(LABEL_MAPPING_REALISTA.keys()))
            # Preencher NaN com 0 (Benign)
            df["Label_encoded"] = df["Label_encoded"].fillna(0)
        
        # Separar features e labels
        pbar.set_description("📊 Separando features...")
        X = df[REQUIRED_FEATURES].copy()
        y = df["Label_encoded"].copy()
        pbar.update(1)
        
        # Tratar valores nulos/infinitos
        pbar.set_description("🧹 Limpando dados...")
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(0)
        time.sleep(0.3)
        pbar.update(1)
        
        # Verificar se há dados inválidos
        if X.isna().any().any():
            print("[WARN] Ainda há valores NaN após tratamento!")
            X = X.fillna(0)
        
        # Normalizar features
        pbar.set_description("📏 Normalizando features...")
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        time.sleep(0.5)
        pbar.update(1)
        
        # Criar DataFrame final
        pbar.set_description("📋 Criando dataset final...")
        df_final = pd.DataFrame(X_scaled, columns=REQUIRED_FEATURES)
        df_final["Label"] = df["Label"].values
        df_final["Label_encoded"] = y.values
        pbar.update(1)
        
        # Criar encoder para labels
        pbar.set_description("🔧 Configurando encoder...")
        encoder = LabelEncoder()
        encoder.fit(list(LABEL_MAPPING_REALISTA.keys()))
        pbar.update(1)
    
    # Salvar artefatos com progresso
    print("\n[INFO] Salvando artefatos...")
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/models", exist_ok=True)
    
    with tqdm(total=4, desc="💾 Salvando arquivos", unit="arquivo") as pbar:
        pbar.set_description("💾 Dataset preprocessado...")
        df_final.to_csv("data/processed/dataset_preprocessado_realista.csv", index=False)
        pbar.update(1)
        
        pbar.set_description("💾 Scaler...")
        dump(scaler, "data/models/scaler_realista.joblib")
        pbar.update(1)
        
        pbar.set_description("💾 Encoder...")
        dump(encoder, "data/models/encoder_realista.joblib")
        pbar.update(1)
        
        # Salvar mapeamento para referência
        pbar.set_description("💾 Mapeamento labels...")
        import json
        with open("data/models/label_mapping_realista.json", "w") as f:
            json.dump(LABEL_MAPPING_REALISTA, f, indent=2)
        pbar.update(1)
    
    print(f"\n[✅] Pré-processamento realista concluído!")
    print(f"[INFO] Features shape: {X_scaled.shape}")
    print(f"[INFO] Labels distribution:")
    print(pd.Series(y).value_counts().sort_index())
    
    return df_final

if __name__ == "__main__":
    preprocessar_dataset_realista()
