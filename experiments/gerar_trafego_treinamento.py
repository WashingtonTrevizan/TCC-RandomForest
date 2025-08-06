"""
🚀 GERADOR DE TRÁFEGO REALISTA PARA TREINAMENTO
==============================================

Gera tráfego de rede sintético com distribuição controlada:
- 40% Tráfego Normal (Benign)
- 20% UDP-Flood 
- 20% SYN-Flood
- 20% HTTP-Flood

Baseado em padrões reais de ataques DDoS observados na literatura.

Autor: Sistema DDoS Detection
Data: 2025
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from tqdm import tqdm
import os

# Configurações globais
np.random.seed(42)
random.seed(42)

class TrafficGenerator:
    """Gerador de tráfego de rede sintético"""
    
    def __init__(self):
        self.current_time = datetime.now()
        
        # Portas comuns por serviço
        self.web_ports = [80, 443, 8080, 8443]
        self.dns_ports = [53]
        self.mail_ports = [25, 587, 993, 995]
        self.ssh_ports = [22]
        self.ftp_ports = [21, 990]
        self.ntp_ports = [123]
        self.snmp_ports = [161, 162]
        
        # IPs comuns (simulados)
        self.normal_src_ips = self._generate_ip_pool(100)  # 100 IPs normais
        self.attack_src_ips = self._generate_ip_pool(5000)  # 5000 IPs para ataques
        self.target_ips = self._generate_ip_pool(20)  # 20 IPs alvo
        
    def _generate_ip_pool(self, count):
        """Gera pool de IPs simulados"""
        ips = []
        for _ in range(count):
            ip = f"{random.randint(1, 223)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            ips.append(ip)
        return ips
    
    def _get_timestamp(self):
        """Gera timestamp sequencial"""
        self.current_time += timedelta(milliseconds=random.randint(1, 100))
        return self.current_time.timestamp()
    
    def generate_benign_traffic(self, n_samples):
        """Gera tráfego normal (navegação web, emails, etc.)"""
        print("🟢 Gerando tráfego NORMAL...")
        
        traffic = []
        
        with tqdm(total=n_samples, desc="Tráfego Normal", unit="pkt") as pbar:
            for i in range(n_samples):
                # Simular diferentes tipos de tráfego normal
                traffic_type = random.choices(
                    ['web', 'email', 'dns', 'ssh', 'ftp', 'p2p'],
                    weights=[50, 15, 20, 5, 5, 5]
                )[0]
                
                if traffic_type == 'web':
                    # Navegação web normal
                    sample = {
                        'timestamp': self._get_timestamp(),
                        'src_ip': random.choice(self.normal_src_ips),
                        'dst_ip': random.choice(self.target_ips),
                        'src_port': random.randint(1024, 65535),
                        'dst_port': random.choice(self.web_ports),
                        'protocol': 1,  # TCP
                        'length': random.randint(64, 1500),
                        'tcp_flags': random.choice(['ACK', 'PSH,ACK', 'FIN,ACK']),
                        'flow_duration': random.uniform(0.5, 300.0),  # 0.5s a 5min
                        'packet_count': random.randint(5, 200),
                        'byte_count': random.randint(1000, 50000),
                        'Label': 'Benign'
                    }
                    
                elif traffic_type == 'dns':
                    # Consultas DNS normais
                    sample = {
                        'timestamp': self._get_timestamp(),
                        'src_ip': random.choice(self.normal_src_ips),
                        'dst_ip': random.choice(self.target_ips),
                        'src_port': random.randint(1024, 65535),
                        'dst_port': 53,
                        'protocol': 2,  # UDP
                        'length': random.randint(64, 512),
                        'tcp_flags': '',
                        'flow_duration': random.uniform(0.01, 2.0),
                        'packet_count': random.randint(1, 5),
                        'byte_count': random.randint(64, 1000),
                        'Label': 'Benign'
                    }
                    
                elif traffic_type == 'email':
                    # Tráfego de email
                    sample = {
                        'timestamp': self._get_timestamp(),
                        'src_ip': random.choice(self.normal_src_ips),
                        'dst_ip': random.choice(self.target_ips),
                        'src_port': random.randint(1024, 65535),
                        'dst_port': random.choice(self.mail_ports),
                        'protocol': 1,  # TCP
                        'length': random.randint(64, 1500),
                        'tcp_flags': 'ACK',
                        'flow_duration': random.uniform(10.0, 600.0),
                        'packet_count': random.randint(10, 500),
                        'byte_count': random.randint(5000, 100000),
                        'Label': 'Benign'
                    }
                    
                else:
                    # Outros tipos de tráfego
                    sample = {
                        'timestamp': self._get_timestamp(),
                        'src_ip': random.choice(self.normal_src_ips),
                        'dst_ip': random.choice(self.target_ips),
                        'src_port': random.randint(1024, 65535),
                        'dst_port': random.randint(1, 65535),
                        'protocol': random.choice([1, 2]),
                        'length': random.randint(64, 1500),
                        'tcp_flags': random.choice(['ACK', 'PSH,ACK', '']),
                        'flow_duration': random.uniform(1.0, 100.0),
                        'packet_count': random.randint(1, 100),
                        'byte_count': random.randint(100, 10000),
                        'Label': 'Benign'
                    }
                
                traffic.append(sample)
                pbar.update(1)
        
        return traffic
    
    def generate_udp_flood(self, n_samples):
        """Gera ataques UDP Flood"""
        print("🔴 Gerando ataques UDP-FLOOD...")
        
        traffic = []
        
        with tqdm(total=n_samples, desc="UDP Flood", unit="pkt") as pbar:
            for i in range(n_samples):
                # Simular amplificação DNS, NTP, SNMP
                amplification_type = random.choices(
                    ['dns', 'ntp', 'snmp', 'generic'],
                    weights=[40, 30, 20, 10]
                )[0]
                
                if amplification_type == 'dns':
                    dst_port = 53
                    length = random.randint(512, 4096)  # Amplificação DNS
                elif amplification_type == 'ntp':
                    dst_port = 123
                    length = random.randint(468, 1500)  # Amplificação NTP
                elif amplification_type == 'snmp':
                    dst_port = 161
                    length = random.randint(1000, 1500)  # Amplificação SNMP
                else:
                    dst_port = random.randint(1, 65535)
                    length = random.randint(64, 1500)
                
                sample = {
                    'timestamp': self._get_timestamp(),
                    'src_ip': random.choice(self.attack_src_ips),  # IPs spoofados
                    'dst_ip': random.choice(self.target_ips),
                    'src_port': random.randint(1024, 65535),
                    'dst_port': dst_port,
                    'protocol': 2,  # UDP
                    'length': length,
                    'tcp_flags': '',
                    'flow_duration': random.uniform(0.001, 0.1),  # Muito rápido
                    'packet_count': random.randint(1, 10),
                    'byte_count': random.randint(64, 15000),
                    'Label': 'UDP-Flood'
                }
                
                traffic.append(sample)
                pbar.update(1)
        
        return traffic
    
    def generate_syn_flood(self, n_samples):
        """Gera ataques SYN Flood"""
        print("🟡 Gerando ataques SYN-FLOOD...")
        
        traffic = []
        
        with tqdm(total=n_samples, desc="SYN Flood", unit="pkt") as pbar:
            for i in range(n_samples):
                # Alvos típicos: serviços TCP
                target_ports = self.web_ports + self.ssh_ports + self.mail_ports
                
                sample = {
                    'timestamp': self._get_timestamp(),
                    'src_ip': random.choice(self.attack_src_ips),  # IPs spoofados
                    'dst_ip': random.choice(self.target_ips),
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice(target_ports),
                    'protocol': 1,  # TCP
                    'length': random.randint(40, 80),  # Pacotes SYN pequenos
                    'tcp_flags': 'SYN',
                    'flow_duration': random.uniform(0.001, 0.5),  # Sem resposta
                    'packet_count': 1,  # Apenas SYN
                    'byte_count': random.randint(40, 80),
                    'Label': 'SYN-Flood'
                }
                
                traffic.append(sample)
                pbar.update(1)
        
        return traffic
    
    def generate_http_flood(self, n_samples):
        """Gera ataques HTTP Flood"""
        print("🟠 Gerando ataques HTTP-FLOOD...")
        
        traffic = []
        
        with tqdm(total=n_samples, desc="HTTP Flood", unit="pkt") as pbar:
            for i in range(n_samples):
                # Simular requisições HTTP massivas
                
                sample = {
                    'timestamp': self._get_timestamp(),
                    'src_ip': random.choice(self.attack_src_ips),
                    'dst_ip': random.choice(self.target_ips),
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([80, 443]),
                    'protocol': 1,  # TCP
                    'length': random.randint(200, 1000),  # Requisições HTTP
                    'tcp_flags': random.choice(['PSH,ACK', 'ACK']),
                    'flow_duration': random.uniform(1.0, 60.0),  # Conexões persistentes
                    'packet_count': random.randint(5, 100),
                    'byte_count': random.randint(1000, 50000),
                    'Label': 'HTTP-Flood'
                }
                
                traffic.append(sample)
                pbar.update(1)
        
        return traffic

def generate_training_dataset(total_samples=100000):
    """
    Gera dataset balanceado para treinamento
    40% Normal, 20% UDP-Flood, 20% SYN-Flood, 20% HTTP-Flood
    """
    print("🎯 GERANDO DATASET DE TREINAMENTO")
    print("=" * 60)
    print(f"Total de amostras: {total_samples:,}")
    
    # Calcular distribuição
    benign_count = int(total_samples * 0.4)      # 40%
    udp_flood_count = int(total_samples * 0.2)   # 20%
    syn_flood_count = int(total_samples * 0.2)   # 20%
    http_flood_count = int(total_samples * 0.2)  # 20%
    
    print(f"📊 Distribuição:")
    print(f"  🟢 Normal: {benign_count:,} ({40}%)")
    print(f"  🔴 UDP-Flood: {udp_flood_count:,} ({20}%)")
    print(f"  🟡 SYN-Flood: {syn_flood_count:,} ({20}%)")
    print(f"  🟠 HTTP-Flood: {http_flood_count:,} ({20}%)")
    print()
    
    generator = TrafficGenerator()
    all_traffic = []
    
    # Gerar cada tipo de tráfego
    all_traffic.extend(generator.generate_benign_traffic(benign_count))
    all_traffic.extend(generator.generate_udp_flood(udp_flood_count))
    all_traffic.extend(generator.generate_syn_flood(syn_flood_count))
    all_traffic.extend(generator.generate_http_flood(http_flood_count))
    
    # Converter para DataFrame
    print("\n📋 Criando DataFrame...")
    df = pd.DataFrame(all_traffic)
    
    # Embaralhar dados
    print("🔀 Embaralhando dados...")
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    # Salvar
    output_path = "data/raw/training_traffic_realistic.csv"
    os.makedirs("data/raw", exist_ok=True)
    
    print(f"💾 Salvando em: {output_path}")
    df.to_csv(output_path, index=False)
    
    # Estatísticas finais
    print(f"\n📊 ESTATÍSTICAS FINAIS:")
    print(f"Total de registros: {len(df):,}")
    print(f"Distribuição real:")
    label_counts = df['Label'].value_counts()
    for label, count in label_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {label}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n✅ Dataset de treinamento criado com sucesso!")
    return df

if __name__ == "__main__":
    # Gerar dataset de treinamento
    df_training = generate_training_dataset(100000)
    
    print("\n" + "=" * 60)
    print("🎉 DATASET DE TREINAMENTO PRONTO!")
    print("📁 Localização: data/raw/training_traffic_realistic.csv")
    print("🚀 Próximo passo: Executar preprocessamento")
