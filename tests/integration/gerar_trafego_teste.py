"""
Gerador de tráfego simulado para testar o modelo DDoS
Cria diferentes tipos de tráfego (normal e ataques) para validação
"""
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def gerar_trafego_normal(n_amostras=1000):
    """Gera tráfego normal (benigno)"""
    print(f"[INFO] Gerando {n_amostras} amostras de tráfego NORMAL...")
    
    dados = []
    base_time = datetime.now()
    
    for i in range(n_amostras):
        # Tráfego web normal
        if random.random() < 0.6:  # 60% tráfego web
            timestamp = base_time + timedelta(seconds=random.uniform(0, 3600))
            src_ip = f"192.168.1.{random.randint(10, 100)}"
            dst_ip = f"8.8.{random.randint(1, 10)}.{random.randint(1, 100)}"
            src_port = random.randint(40000, 65000)
            dst_port = random.choice([80, 443, 8080])
            protocol = "TCP"
            length = random.randint(60, 1500)
            tcp_flags = 24  # ACK + PSH (tráfego normal)
            
        # Tráfego DNS normal
        elif random.random() < 0.3:  # 30% DNS
            timestamp = base_time + timedelta(seconds=random.uniform(0, 3600))
            src_ip = f"192.168.1.{random.randint(10, 100)}"
            dst_ip = f"8.8.{random.randint(1, 10)}.{random.randint(1, 100)}"
            src_port = random.randint(40000, 65000)
            dst_port = 53
            protocol = "UDP"
            length = random.randint(50, 200)
            tcp_flags = 0
            
        # Outro tráfego normal
        else:
            timestamp = base_time + timedelta(seconds=random.uniform(0, 3600))
            src_ip = f"192.168.1.{random.randint(10, 100)}"
            dst_ip = f"10.0.{random.randint(1, 10)}.{random.randint(1, 100)}"
            src_port = random.randint(1024, 65000)
            dst_port = random.choice([22, 25, 110, 143, 993, 995])
            protocol = random.choice(["TCP", "UDP"])
            length = random.randint(40, 800)
            tcp_flags = random.choice([16, 24, 25]) if protocol == "TCP" else 0
        
        dados.append({
            'timestamp': timestamp,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': protocol,
            'length': length,
            'tcp_flags': tcp_flags
        })
    
    return dados

def gerar_ataque_syn_flood(n_amostras=50):
    """Gera ataque SYN Flood"""
    print(f"[INFO] Gerando {n_amostras} amostras de ataque SYN FLOOD...")
    
    dados = []
    base_time = datetime.now()
    target_ip = "192.168.1.100"  # Alvo do ataque
    
    for i in range(n_amostras):
        # IPs de origem falsificados (spoofing)
        src_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        timestamp = base_time + timedelta(milliseconds=random.randint(0, 1000))  # Muito rápido
        dst_ip = target_ip
        src_port = random.randint(1024, 65535)
        dst_port = random.choice([80, 443, 22, 25])  # Serviços comuns
        protocol = "TCP"
        length = random.randint(40, 80)  # Pacotes pequenos
        tcp_flags = 2  # SYN flag
        
        dados.append({
            'timestamp': timestamp,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': protocol,
            'length': length,
            'tcp_flags': tcp_flags
        })
    
    return dados

def gerar_ataque_udp_flood(n_amostras=30):
    """Gera ataque UDP Flood"""
    print(f"[INFO] Gerando {n_amostras} amostras de ataque UDP FLOOD...")
    
    dados = []
    base_time = datetime.now()
    target_ip = "192.168.1.200"
    
    for i in range(n_amostras):
        # IPs de origem distribuídos (botnet simulada)
        src_ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        timestamp = base_time + timedelta(milliseconds=random.randint(0, 500))  # Muito rápido
        dst_ip = target_ip
        src_port = random.randint(1024, 65535)
        dst_port = random.choice([53, 123, 161, 1900, 5353])  # Portas para amplificação
        protocol = "UDP"
        length = random.randint(1000, 3000)  # Pacotes grandes (amplificação)
        tcp_flags = 0
        
        dados.append({
            'timestamp': timestamp,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': protocol,
            'length': length,
            'tcp_flags': tcp_flags
        })
    
    return dados

def gerar_ataque_http_flood(n_amostras=20):
    """Gera ataque HTTP Flood"""
    print(f"[INFO] Gerando {n_amostras} amostras de ataque HTTP FLOOD...")
    
    dados = []
    base_time = datetime.now()
    target_ip = "192.168.1.150"
    
    for i in range(n_amostras):
        # IPs de origem variados (botnet)
        src_ip = f"192.168.{random.randint(1, 10)}.{random.randint(1, 255)}"
        
        timestamp = base_time + timedelta(milliseconds=random.randint(0, 2000))
        dst_ip = target_ip
        src_port = random.randint(30000, 65535)
        dst_port = random.choice([80, 443])  # HTTP/HTTPS
        protocol = "TCP"
        length = random.randint(200, 800)  # Requisições HTTP
        tcp_flags = 24  # ACK + PSH
        
        dados.append({
            'timestamp': timestamp,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'src_port': src_port,
            'dst_port': dst_port,
            'protocol': protocol,
            'length': length,
            'tcp_flags': tcp_flags
        })
    
    return dados

def criar_dataset_teste():
    """Cria dataset completo de teste"""
    print("🔧 CRIANDO DATASET DE TESTE PARA VALIDAÇÃO")
    print("="*60)
    
    # Gerar diferentes tipos de tráfego
    trafego_normal = gerar_trafego_normal(800)
    ataque_syn = gerar_ataque_syn_flood(100) 
    ataque_udp = gerar_ataque_udp_flood(80)
    ataque_http = gerar_ataque_http_flood(20)
    
    # Combinar todos os dados
    todos_dados = trafego_normal + ataque_syn + ataque_udp + ataque_http
    
    # Criar DataFrame
    df = pd.DataFrame(todos_dados)
    
    # Embaralhar os dados
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Salvar dataset de teste
    os.makedirs("data", exist_ok=True)
    arquivo_teste = "data/trafego_simulado_teste.csv"
    df.to_csv(arquivo_teste, index=False)
    
    print(f"\n📊 ESTATÍSTICAS DO DATASET DE TESTE:")
    print(f"Total de amostras: {len(df)}")
    print(f"Período: {df['timestamp'].min()} até {df['timestamp'].max()}")
    print(f"Protocolos: {df['protocol'].value_counts().to_dict()}")
    print(f"Portas mais comuns: {df['dst_port'].value_counts().head().to_dict()}")
    
    print(f"\n✅ Dataset de teste salvo em: {arquivo_teste}")
    return arquivo_teste

def validar_dataset_teste(arquivo):
    """Valida o dataset de teste criado"""
    print("\n🔍 VALIDANDO DATASET DE TESTE:")
    print("="*50)
    
    df = pd.read_csv(arquivo)
    
    # Verificações básicas
    print(f"✓ Shape: {df.shape}")
    print(f"✓ Colunas: {list(df.columns)}")
    print(f"✓ Valores nulos: {df.isnull().sum().sum()}")
    
    # Verificar tipos esperados de tráfego
    tcp_count = (df['protocol'] == 'TCP').sum()
    udp_count = (df['protocol'] == 'UDP').sum()
    syn_flags = (df['tcp_flags'] == 2).sum()
    
    print(f"\n📈 ANÁLISE DO TRÁFEGO:")
    print(f"• TCP: {tcp_count} pacotes")
    print(f"• UDP: {udp_count} pacotes") 
    print(f"• SYN flags: {syn_flags} pacotes (possíveis ataques)")
    print(f"• Tamanho médio: {df['length'].mean():.1f} bytes")
    print(f"• Portas web (80/443): {df['dst_port'].isin([80, 443]).sum()} pacotes")
    
    return True

def main():
    """Função principal"""
    print("🚀 GERADOR DE TRÁFEGO SIMULADO PARA TESTE")
    print("="*60)
    
    # Criar dataset de teste
    arquivo_teste = criar_dataset_teste()
    
    # Validar dataset
    validar_dataset_teste(arquivo_teste)
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print(f"1. Use este arquivo para testar o modelo:")
    print(f"   python tools/inferencia_ddos.py {arquivo_teste} data/resultados_teste.csv")
    print(f"2. Analise os resultados para verificar se o modelo está detectando corretamente")
    print(f"3. Compare com os padrões esperados (SYN floods, UDP floods, etc.)")

if __name__ == "__main__":
    main()
