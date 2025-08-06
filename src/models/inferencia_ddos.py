import pandas as pd
import numpy as np
from joblib import load
import sys
import os
import json

# Importar módulo de feature engineering
sys.path.append(os.path.dirname(__file__))
from feature_engineering import REQUIRED_FEATURES, REVERSE_LABEL_MAPPING, preprocess_basic_fields, calculate_flow_features, prepare_features_for_model

def carregar_modelo_e_preprocessadores():
    """Carrega modelo e preprocessadores salvos"""
    print("[INFO] Carregando modelo e preprocessadores...")
    
    try:
        scaler = load("model/scaler.joblib")
        encoder = load("model/encoder.joblib") 
        model = load("model/ddos_model.pkl")
        
        # Carregar mapeamento se existir
        if os.path.exists("model/label_mapping.json"):
            with open("model/label_mapping.json", "r") as f:
                label_mapping = json.load(f)
            print(f"[INFO] Label mapping carregado: {label_mapping}")
        
        print("[✓] Modelo e preprocessadores carregados com sucesso!")
        return scaler, encoder, model
        
    except Exception as e:
        print(f"[ERROR] Erro ao carregar modelo: {e}")
        raise

def preprocessar_para_inferencia(df, scaler):
    """Preprocessa dados para inferência usando pipeline padronizado"""
    print("[INFO] Preprocessando dados para inferência...")
    
    # 1. Preprocessar campos básicos
    df = preprocess_basic_fields(df.copy())
    
    # 2. Calcular features de fluxo
    df = calculate_flow_features(df)
    
    # 3. Preparar features finais (sem labels)
    df_features = prepare_features_for_model(df, include_labels=False)
    
    # 4. Aplicar normalização
    df_normalized = df_features.copy()
    df_normalized[REQUIRED_FEATURES] = scaler.transform(df_features[REQUIRED_FEATURES])
    
    print(f"[✓] Preprocessamento concluído. Shape: {df_normalized.shape}")
    return df_normalized, df_features

def realizar_inferencia():
    """Função principal de inferência"""
    if len(sys.argv) < 2:
        print("Uso: python inferencia_ddos.py <csv_entrada> [csv_saida]")
        sys.exit(1)
    
    csv_entrada = sys.argv[1]
    csv_saida = sys.argv[2] if len(sys.argv) > 2 else "data/resultados_inferencia.csv"
    
    print(f"[INFO] Arquivo de entrada: {csv_entrada}")
    print(f"[INFO] Arquivo de saída: {csv_saida}")
    
    # Carregar dados
    print("[INFO] Carregando dados...")
    df_original = pd.read_csv(csv_entrada)
    print(f"[INFO] Dados carregados. Shape: {df_original.shape}")
    
    # Carregar modelo
    scaler, encoder, model = carregar_modelo_e_preprocessadores()
    
    # Preprocessar dados
    df_normalized, df_features = preprocessar_para_inferencia(df_original, scaler)
    
    # Realizar predições
    print("[INFO] Realizando predições...")
    try:
        predictions = model.predict(df_normalized[REQUIRED_FEATURES])
        print(f"[✓] Predições realizadas. Total: {len(predictions)}")
        
        # Mapear predições para labels
        df_resultado = df_original.copy()
        df_resultado['Predito'] = [REVERSE_LABEL_MAPPING.get(pred, f"Desconhecido_{pred}") for pred in predictions]
        
        # Adicionar features calculadas para análise
        for feature in REQUIRED_FEATURES:
            if feature in df_features.columns:
                df_resultado[f'{feature}_calculated'] = df_features[feature].values
        
        # Salvar resultados
        print("[INFO] Salvando resultados...")
        df_resultado.to_csv(csv_saida, index=False)
        
        # Mostrar estatísticas
        print("\n" + "="*50)
        print("RESULTADOS DA INFERÊNCIA")
        print("="*50)
        print("Distribuição das predições:")
        print(df_resultado['Predito'].value_counts())
        print(f"\nTotal de registros processados: {len(df_resultado)}")
        print(f"Resultados salvos em: {csv_saida}")
        print("="*50)
        
        return df_resultado
        
    except Exception as e:
        print(f"[ERROR] Erro durante a inferência: {e}")
        raise

if __name__ == "__main__":
    realizar_inferencia()

