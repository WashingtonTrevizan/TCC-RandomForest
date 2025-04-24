import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

CSV_PATH = "data/pcap_convertido.csv"
SAIDA_TRATADA = "data/dataset_final.csv"

def calcular_features(df):
    # Calcula a duração do fluxo baseada no timestamp (se existir)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['flow_duration'] = df.groupby(['src_ip', 'dst_ip'])['timestamp'].transform(
            lambda x: (x.max() - x.min()).total_seconds()
        )
    else:
        df['flow_duration'] = 0  # Valor padrão se não houver timestamp

    # Taxa de pacotes e bytes (simplificado)
    df['packet_rate'] = df.groupby(['src_ip', 'dst_ip'])['length'].transform('count') / (df['flow_duration'] + 1e-6)
    df['byte_rate'] = df.groupby(['src_ip', 'dst_ip'])['length'].transform('sum') / (df['flow_duration'] + 1e-6)

    # Contagem de IPs de origem/destino (para detectar spoofing)
    df['src_ip_count'] = df.groupby('src_ip')['src_ip'].transform('count')
    df['dst_ip_count'] = df.groupby('dst_ip')['dst_ip'].transform('count')

    # Flags TCP (se disponíveis)
    if 'tcp_flags' in df.columns:
        df['tcp_syn'] = df['tcp_flags'].apply(lambda x: 1 if x & 0x02 else 0)  # Verifica flag SYN
    else:
        df['tcp_syn'] = 0

    return df

def rotular_ddos(df):
    # Regras baseadas nas features calculadas
    conditions = [
        (df['protocol'] == 'UDP') & (df['byte_rate'] > 1e6),
        (df['protocol'] == 'TCP') & (df['tcp_syn'] > 100),
        (df['dst_ip_count'] > 1000),
    ]
    choices = [
        'UDP-Flood',
        'SYN-Flood',
        'HTTP-Flood',
    ]
    df['Label'] = np.select(conditions, choices, default='Benign')
    return df

def tratar_csv():
    print("[INFO] Carregando CSV...")
    df = pd.read_csv(CSV_PATH)

    print("[INFO] Calculando features...")
    df = calcular_features(df)

    print("[INFO] Rotulando ataques DDoS...")
    df = rotular_ddos(df)

    print("[INFO] Salvando dataset tratado...")
    df.to_csv(SAIDA_TRATADA, index=False)
    print(f"[✅] Dataset salvo em: {SAIDA_TRATADA}")

if __name__ == "__main__":
    tratar_csv()