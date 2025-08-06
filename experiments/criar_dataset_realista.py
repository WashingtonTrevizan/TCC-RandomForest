"""
Corrige o problema de data leakage e cria um dataset mais realista
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def criar_regras_rotulacao_realistas(df):
    """Cria labels baseado em múltiplos critérios mais complexos e realistas"""
    print("[INFO] Aplicando regras de rotulação REALISTAS...")
    
    labels = []  # Lista vazia para append
    
    for i, row in df.iterrows():
        # Score de suspeição baseado em múltiplos fatores
        score_suspeito = 0
        
        # 1. Taxa de pacotes anômala
        if row['packet_rate'] > 1000:
            score_suspeito += 2
        elif row['packet_rate'] > 500:
            score_suspeito += 1
            
        # 2. Taxa de bytes anômala  
        if row['byte_rate'] > 1000000:  # 1MB/s
            score_suspeito += 2
        elif row['byte_rate'] > 500000:
            score_suspeito += 1
            
        # 3. Duração de fluxo suspeita
        if row['flow_duration'] < 0.1:  # Muito rápido
            score_suspeito += 1
        elif row['flow_duration'] > 3600:  # Muito longo 
            score_suspeito += 1
            
        # 4. Flags TCP suspeitas
        if row['tcp_syn'] == 1 and row['flow_duration'] < 1.0:
            score_suspeito += 2
            
        # 5. Contagem de IPs anômala
        if row['src_ip_count'] > 10000:  # Muitos IPs origem
            score_suspeito += 1
        if row['dst_ip_count'] > 1000:   # Muitos IPs destino
            score_suspeito += 1
            
        # 6. Protocolos e portas específicas
        if row['protocol'] == 2 and row['dst_port'] in [53, 123, 161]:  # DNS/NTP/SNMP amplification
            score_suspeito += 1
            
        # 7. Adicionar ruído (realismo)
        ruido = random.uniform(-0.5, 0.5)
        score_suspeito += ruido
        
        # Classificar baseado no score (com sobreposição intencional)
        if score_suspeito >= 4.0:
            # Determinar tipo específico de ataque
            if row['protocol'] == 2 and row['byte_rate'] > 800000:
                labels.append('UDP-Flood')
            elif row['tcp_syn'] == 1 and row['packet_rate'] > 200:
                labels.append('SYN-Flood')  
            elif row['dst_port'] in [80, 443] and row['packet_rate'] > 800:
                labels.append('HTTP-Flood')
            else:
                labels.append('DDoS-Other')  # Novo tipo genérico
        elif score_suspeito >= 2.5:
            # Zona cinzenta - pode ser suspeito ou não
            if random.random() < 0.3:  # 30% chance de ser ataque
                labels.append(random.choice(['UDP-Flood', 'SYN-Flood', 'HTTP-Flood']))
            else:
                labels.append('Benign')
        else:
            labels.append('Benign')
    
    df['Label'] = labels
    return df

def adicionar_ataques_sinteticos_realistas(df, n_ataques=1000):
    """Adiciona ataques sintéticos mais realistas com ruído"""
    print(f"[INFO] Adicionando {n_ataques} ataques sintéticos realistas...")
    
    ataques_novos = []
    
    for i in range(n_ataques):
        if i < n_ataques // 4:  # 25% UDP Flood
            ataque = {
                'flow_duration': random.uniform(0.01, 2.0),
                'packet_rate': random.uniform(800, 5000),  # Menos extremo
                'byte_rate': random.uniform(500000, 2000000), # Com variação
                'src_ip_count': random.randint(100, 5000),
                'dst_ip_count': random.randint(1, 50), 
                'tcp_syn': 0,
                'length': random.randint(100, 1500),
                'dst_port': random.choice([53, 123, 161, 1900]),
                'protocol': 2,
                'Label': 'UDP-Flood'
            }
        elif i < n_ataques // 2:  # 25% SYN Flood
            ataque = {
                'flow_duration': random.uniform(0.001, 0.5),
                'packet_rate': random.uniform(200, 2000),
                'byte_rate': random.uniform(10000, 100000),
                'src_ip_count': random.randint(50, 1000),
                'dst_ip_count': random.randint(1, 10),
                'tcp_syn': 1,
                'length': random.randint(40, 100),
                'dst_port': random.choice([80, 443, 22, 25]),
                'protocol': 1,
                'Label': 'SYN-Flood'
            }
        elif i < 3 * n_ataques // 4:  # 25% HTTP Flood
            ataque = {
                'flow_duration': random.uniform(1.0, 30.0),
                'packet_rate': random.uniform(500, 2000),
                'byte_rate': random.uniform(100000, 800000),
                'src_ip_count': random.randint(10, 500),
                'dst_ip_count': random.randint(1, 20),
                'tcp_syn': 0,
                'length': random.randint(200, 1000),
                'dst_port': random.choice([80, 443]),
                'protocol': 1,
                'Label': 'HTTP-Flood'
            }
        else:  # 25% tráfego suspeito (falsos positivos intencionais)
            ataque = {
                'flow_duration': random.uniform(0.1, 10.0),
                'packet_rate': random.uniform(100, 1000),
                'byte_rate': random.uniform(50000, 500000),
                'src_ip_count': random.randint(10, 1000),
                'dst_ip_count': random.randint(1, 100),
                'tcp_syn': random.choice([0, 1]),
                'length': random.randint(60, 1500),
                'dst_port': random.randint(1, 65535),
                'protocol': random.choice([1, 2]),
                'Label': 'Benign'  # Suspeito mas normal
            }
        
        ataques_novos.append(ataque)
    
    # Adicionar ao dataset original
    df_ataques = pd.DataFrame(ataques_novos)
    df_combined = pd.concat([df, df_ataques], ignore_index=True)
    
    # Embaralhar
    df_combined = df_combined.sample(frac=1).reset_index(drop=True)
    
    return df_combined

def criar_dataset_realista():
    """Cria um dataset mais realista para treinamento"""
    print("🔧 CRIANDO DATASET MAIS REALISTA")
    print("="*60)
    
    # Carregar dados originais
    df_original = pd.read_csv('data/dataset_final.csv')
    print(f"Dataset original: {df_original.shape}")
    
    # Usar apenas subset para evitar overfitting
    df_subset = df_original.sample(n=50000, random_state=42).copy()
    print(f"Subset para retreino: {df_subset.shape}")
    
    # Remover labels originais
    df_subset = df_subset.drop(['Label', 'Label_encoded'], axis=1)
    
    # Aplicar rotulação mais realista
    df_subset = criar_regras_rotulacao_realistas(df_subset)
    
    # Adicionar ataques sintéticos
    df_final = adicionar_ataques_sinteticos_realistas(df_subset, n_ataques=2000)
    
    # Adicionar encoding
    label_mapping = {'Benign': 0, 'UDP-Flood': 1, 'SYN-Flood': 2, 'HTTP-Flood': 3, 'DDoS-Other': 4}
    df_final['Label_encoded'] = df_final['Label'].map(label_mapping)
    
    # Salvar dataset realista
    df_final.to_csv('data/dataset_realista.csv', index=False)
    
    print(f"\n📊 DISTRIBUIÇÃO DO DATASET REALISTA:")
    print(df_final['Label'].value_counts())
    print(f"\nTotal: {len(df_final)} amostras")
    print(f"Balanceamento: {(df_final['Label'] != 'Benign').sum() / len(df_final) * 100:.1f}% ataques")
    
    print(f"\n✅ Dataset realista salvo em: data/dataset_realista.csv")

if __name__ == "__main__":
    criar_dataset_realista()
