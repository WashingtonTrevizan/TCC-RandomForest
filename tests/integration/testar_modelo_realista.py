"""
Testa o modelo realista com novos dados
"""
import pandas as pd
import numpy as np
import joblib
import time
from tqdm import tqdm
from sklearn.metrics import classification_report, confusion_matrix

def gerar_dados_teste():
    """Gera alguns dados de teste para verificar o modelo"""
    print("🧪 GERANDO DADOS DE TESTE")
    print("="*40)
    
    # Simular diferentes tipos de tráfego
    dados_teste = []
    
    with tqdm(total=4, desc="🔬 Criando amostras", unit="tipo") as pbar:
        # 1. Tráfego normal
        pbar.set_description("🟢 Tráfego normal...")
        for i in range(50):
            dados_teste.append({
                'flow_duration': np.random.uniform(1.0, 300.0),
                'packet_rate': np.random.uniform(1, 100),
                'byte_rate': np.random.uniform(1000, 50000),
                'src_ip_count': np.random.randint(1, 20),
                'dst_ip_count': np.random.randint(1, 10),
                'tcp_syn': np.random.choice([0, 1], p=[0.8, 0.2]),
                'length': np.random.randint(64, 1500),
                'dst_port': np.random.choice([80, 443, 22, 25, 53]),
                'protocol': np.random.choice([1, 2]),
                'tipo_real': 'Normal'
            })
        pbar.update(1)
        
        # 2. Possível UDP Flood
        pbar.set_description("🔴 UDP Flood...")
        for i in range(20):
            dados_teste.append({
                'flow_duration': np.random.uniform(0.01, 1.0),
                'packet_rate': np.random.uniform(1000, 5000),
                'byte_rate': np.random.uniform(800000, 2000000),
                'src_ip_count': np.random.randint(100, 1000),
                'dst_ip_count': np.random.randint(1, 5),
                'tcp_syn': 0,
                'length': np.random.randint(100, 1000),
                'dst_port': np.random.choice([53, 123, 161]),
                'protocol': 2,
                'tipo_real': 'UDP-Flood'
            })
        pbar.update(1)
        
        # 3. Possível SYN Flood
        pbar.set_description("🟡 SYN Flood...")
        for i in range(20):
            dados_teste.append({
                'flow_duration': np.random.uniform(0.001, 0.5),
                'packet_rate': np.random.uniform(500, 3000),
                'byte_rate': np.random.uniform(20000, 200000),
                'src_ip_count': np.random.randint(50, 500),
                'dst_ip_count': np.random.randint(1, 3),
                'tcp_syn': 1,
                'length': np.random.randint(40, 80),
                'dst_port': np.random.choice([80, 443, 22]),
                'protocol': 1,
                'tipo_real': 'SYN-Flood'
            })
        pbar.update(1)
        
        # 4. Possível HTTP Flood
        pbar.set_description("🟠 HTTP Flood...")
        for i in range(20):
            dados_teste.append({
                'flow_duration': np.random.uniform(2.0, 30.0),
                'packet_rate': np.random.uniform(800, 2000),
                'byte_rate': np.random.uniform(200000, 800000),
                'src_ip_count': np.random.randint(20, 200),
                'dst_ip_count': np.random.randint(1, 5),
                'tcp_syn': 0,
                'length': np.random.randint(200, 800),
                'dst_port': np.random.choice([80, 443]),
                'protocol': 1,
                'tipo_real': 'HTTP-Flood'
            })
        pbar.update(1)
    
    return pd.DataFrame(dados_teste)

def testar_modelo_realista():
    """Testa o modelo realista"""
    print("🎯 TESTE DO MODELO REALISTA")
    print("="*50)
    
    # Carregar modelo e preprocessadores
    print("[INFO] Carregando artefatos...")
    
    with tqdm(total=3, desc="📂 Carregando", unit="arquivo") as pbar:
        pbar.set_description("📂 Modelo...")
        modelo = joblib.load("data/models/ddos_model_realista.pkl")
        pbar.update(1)
        
        pbar.set_description("📂 Scaler...")
        scaler = joblib.load("data/models/scaler_realista.joblib")
        pbar.update(1)
        
        pbar.set_description("📂 Metadados...")
        import json
        with open("data/models/label_mapping_realista.json", "r") as f:
            label_mapping = json.load(f)
        pbar.update(1)
    
    # Mapeamento reverso
    reverse_mapping = {v: k for k, v in label_mapping.items()}
    
    # Gerar dados de teste
    df_teste = gerar_dados_teste()
    print(f"\n[INFO] Dados de teste gerados: {df_teste.shape}")
    
    # Preparar features
    REQUIRED_FEATURES = [
        'flow_duration', 'packet_rate', 'byte_rate', 
        'src_ip_count', 'dst_ip_count', 'tcp_syn',
        'length', 'dst_port', 'protocol'
    ]
    
    X_teste = df_teste[REQUIRED_FEATURES]
    
    print("\n[INFO] Fazendo predições...")
    
    with tqdm(total=3, desc="🔮 Predizendo", unit="etapa") as pbar:
        # Normalizar
        pbar.set_description("📏 Normalizando...")
        X_teste_scaled = scaler.transform(X_teste)
        pbar.update(1)
        
        # Predizer
        pbar.set_description("🎯 Classificando...")
        y_pred = modelo.predict(X_teste_scaled)
        pbar.update(1)
        
        # Obter probabilidades
        pbar.set_description("📊 Probabilidades...")
        y_proba = modelo.predict_proba(X_teste_scaled)
        pbar.update(1)
    
    # Converter predições para nomes
    pred_names = [reverse_mapping.get(pred, f"Classe_{pred}") for pred in y_pred]
    
    # Adicionar resultados ao DataFrame
    df_teste['Predição'] = pred_names
    df_teste['Confiança'] = y_proba.max(axis=1)
    
    # Análise dos resultados
    print(f"\n📊 RESULTADOS DO TESTE:")
    print("="*50)
    
    # Resumo por tipo real
    for tipo_real in df_teste['tipo_real'].unique():
        subset = df_teste[df_teste['tipo_real'] == tipo_real]
        pred_counts = subset['Predição'].value_counts()
        
        print(f"\n🔍 {tipo_real} ({len(subset)} amostras):")
        for pred, count in pred_counts.items():
            pct = (count / len(subset)) * 100
            print(f"  → {pred}: {count} ({pct:.1f}%)")
    
    # Matriz de confusão simplificada
    print(f"\n🎯 ACERTOS POR CATEGORIA:")
    print("-" * 30)
    
    mapping_esperado = {
        'Normal': 'Benign',
        'UDP-Flood': 'UDP-Flood', 
        'SYN-Flood': 'SYN-Flood',
        'HTTP-Flood': 'HTTP-Flood'
    }
    
    for tipo_real, esperado in mapping_esperado.items():
        subset = df_teste[df_teste['tipo_real'] == tipo_real]
        acertos = len(subset[subset['Predição'] == esperado])
        total = len(subset)
        pct = (acertos / total) * 100 if total > 0 else 0
        
        status = "✅" if pct >= 80 else "⚠️" if pct >= 60 else "❌"
        print(f"{status} {tipo_real:12} | {acertos:2}/{total:2} ({pct:5.1f}%)")
    
    # Salvar resultados detalhados
    print(f"\n[INFO] Salvando resultados...")
    df_teste.to_csv("data/processed/teste_modelo_realista.csv", index=False)
    
    # Amostras com baixa confiança
    baixa_confianca = df_teste[df_teste['Confiança'] < 0.8]
    if len(baixa_confianca) > 0:
        print(f"\n⚠️  PREDIÇÕES COM BAIXA CONFIANÇA ({len(baixa_confianca)} amostras):")
        print(baixa_confianca[['tipo_real', 'Predição', 'Confiança']].to_string())
    
    print(f"\n✅ Teste concluído! Resultados em: data/processed/teste_modelo_realista.csv")
    
    return df_teste

if __name__ == "__main__":
    resultados = testar_modelo_realista()
