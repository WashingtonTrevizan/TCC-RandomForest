"""
Módulo centralizado para engenharia de features
Garante consistência entre treinamento e inferência
"""
import pandas as pd
import numpy as np
from datetime import datetime

# Mapeamento padronizado de labels
LABEL_MAPPING = {
    'Benign': 0,
    'UDP-Flood': 1,
    'SYN-Flood': 2, 
    'HTTP-Flood': 3
}

REVERSE_LABEL_MAPPING = {v: k for k, v in LABEL_MAPPING.items()}

# Features obrigatórias para o modelo
REQUIRED_FEATURES = [
    'flow_duration', 'packet_rate', 'byte_rate', 
    'src_ip_count', 'dst_ip_count', 'tcp_syn',
    'length', 'dst_port', 'protocol'
]

def validate_dataframe(df, required_columns):
    """Valida se o DataFrame tem as colunas necessárias"""
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Colunas faltantes: {missing_cols}")
    
    print(f"[✓] DataFrame validado. Shape: {df.shape}")
    return True

def preprocess_basic_fields(df):
    """Pré-processa campos básicos"""
    print("[INFO] Preprocessando campos básicos...")
    
    # Converter timestamp para datetime se for string
    if 'timestamp' in df.columns:
        if df['timestamp'].dtype == 'object':
            df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Mapear protocolo para numérico de forma consistente
    if df['protocol'].dtype == 'object':
        df['protocol'] = df['protocol'].map({'TCP': 1, 'UDP': 2, 'ICMP': 3}).fillna(0)
    
    # Garantir que dst_port é numérico
    df['dst_port'] = pd.to_numeric(df['dst_port'], errors='coerce').fillna(0)
    
    # Garantir que tcp_flags existe
    if 'tcp_flags' not in df.columns:
        df['tcp_flags'] = 0
    
    return df

def calculate_flow_features(df):
    """Calcula features de fluxo de rede"""
    print("[INFO] Calculando features de fluxo...")
    
    # 1. Flow Duration (por fluxo src_ip -> dst_ip)
    if 'timestamp' in df.columns:
        df['flow_duration'] = df.groupby(['src_ip', 'dst_ip'])['timestamp'].transform(
            lambda x: (x.max() - x.min()).total_seconds() if len(x) > 1 else 0.0
        )
    else:
        df['flow_duration'] = 0.0
    
    # 2. Packet Rate (pacotes por segundo por fluxo)
    df['flow_packet_count'] = df.groupby(['src_ip', 'dst_ip'])['length'].transform('count')
    df['packet_rate'] = df['flow_packet_count'] / (df['flow_duration'] + 1e-6)
    
    # 3. Byte Rate (bytes por segundo por fluxo)
    df['flow_byte_sum'] = df.groupby(['src_ip', 'dst_ip'])['length'].transform('sum')
    df['byte_rate'] = df['flow_byte_sum'] / (df['flow_duration'] + 1e-6)
    
    # 4. Contagem de IPs únicos (para detectar spoofing/distribuído)
    df['src_ip_count'] = df.groupby('src_ip')['src_ip'].transform('count')
    df['dst_ip_count'] = df.groupby('dst_ip')['dst_ip'].transform('count')
    
    # 5. TCP SYN flag detection
    if 'tcp_flags' in df.columns:
        df['tcp_syn'] = df['tcp_flags'].apply(lambda x: 1 if (int(x) & 0x02) else 0)
    else:
        df['tcp_syn'] = 0
    
    # Remover colunas auxiliares
    df = df.drop(['flow_packet_count', 'flow_byte_sum'], axis=1, errors='ignore')
    
    return df

def create_labels_based_on_rules(df):
    """Cria labels baseado em regras heurísticas"""
    print("[INFO] Aplicando regras de rotulação...")
    
    # Condições para diferentes tipos de ataque
    conditions = [
        # UDP Flood: protocolo UDP + alta taxa de bytes
        (df['protocol'] == 2) & (df['byte_rate'] > 1e6),
        
        # SYN Flood: TCP + muitos SYNs + baixa duração de fluxo
        (df['protocol'] == 1) & (df['tcp_syn'] == 1) & (df['flow_duration'] < 1.0) & (df['packet_rate'] > 100),
        
        # HTTP Flood: porta 80/443 + alta taxa de pacotes
        (df['dst_port'].isin([80, 443])) & (df['packet_rate'] > 1000),
    ]
    
    choices = ['UDP-Flood', 'SYN-Flood', 'HTTP-Flood']
    df['Label'] = np.select(conditions, choices, default='Benign')
    
    return df

def prepare_features_for_model(df, include_labels=True):
    """Prepara features finais para o modelo"""
    print("[INFO] Preparando features para o modelo...")
    
    # Verificar se todas as features obrigatórias existem
    validate_dataframe(df, REQUIRED_FEATURES)
    
    # Tratar valores infinitos e NaN
    df[REQUIRED_FEATURES] = df[REQUIRED_FEATURES].replace([np.inf, -np.inf], np.nan)
    df[REQUIRED_FEATURES] = df[REQUIRED_FEATURES].fillna(0)
    
    # Preparar DataFrame final
    result_df = df[REQUIRED_FEATURES].copy()
    
    if include_labels and 'Label' in df.columns:
        result_df['Label'] = df['Label']
        # Adicionar label encoding
        result_df['Label_encoded'] = result_df['Label'].map(LABEL_MAPPING)
    
    return result_df

def full_feature_pipeline(df, include_labels=True):
    """Pipeline completo de features"""
    print("[INFO] Iniciando pipeline completo de features...")
    
    # 1. Preprocessar campos básicos
    df = preprocess_basic_fields(df.copy())
    
    # 2. Calcular features de fluxo
    df = calculate_flow_features(df)
    
    # 3. Criar labels (se solicitado)
    if include_labels:
        df = create_labels_based_on_rules(df)
    
    # 4. Preparar features finais
    final_df = prepare_features_for_model(df, include_labels)
    
    print(f"[✓] Pipeline concluído. Shape final: {final_df.shape}")
    return final_df

def print_feature_summary(df):
    """Imprime resumo das features calculadas"""
    print("\n" + "="*50)
    print("RESUMO DAS FEATURES CALCULADAS")
    print("="*50)
    
    for feature in REQUIRED_FEATURES:
        if feature in df.columns:
            print(f"{feature:15} | Min: {df[feature].min():.2f} | Max: {df[feature].max():.2f} | Mean: {df[feature].mean():.2f}")
    
    if 'Label' in df.columns:
        print(f"\nDistribuição de Labels:")
        print(df['Label'].value_counts())
    
    print("="*50)
