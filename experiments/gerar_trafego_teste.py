"""
🧪 GERADOR DE TRÁFEGO REALISTA PARA TESTE
========================================

Gera tráfego de teste com distribuição ALEATÓRIA para validar
se o modelo consegue identificar corretamente os ataques em
cenários reais não controlados.

Características:
- Distribuição aleatória (não balanceada)
- Padrões mais sutis e misturados
- Casos edge e ataques mascarados
- Cenários do mundo real

Autor: Sistema DDoS Detection
Data: 2025
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
from tqdm import tqdm
import os

# Seed diferente para gerar padrões diferentes
np.random.seed(123)
random.seed(123)

class TestTrafficGenerator:
    """Gerador de tráfego de teste com padrões realistas"""
    
    def __init__(self):
        self.current_time = datetime.now()
        
        # Simular cenários mais realistas
        self.office_ips = self._generate_ip_pool(50, "192.168.1")  # Rede interna
        self.home_ips = self._generate_ip_pool(200, "10.0.0")      # Usuários domésticos
        self.mobile_ips = self._generate_ip_pool(300, "172.16.0")  # Dispositivos móveis
        self.botnet_ips = self._generate_ip_pool(1000)             # IPs comprometidos
        self.legitimate_servers = self._generate_ip_pool(10)       # Servidores legítimos
        
        # Cenários temporais (hora do dia afeta padrões)
        self.current_hour = random.randint(0, 23)
        
    def _generate_ip_pool(self, count, prefix=None):
        """Gera pool de IPs com prefixo específico ou aleatório"""
        ips = []
        for _ in range(count):
            if prefix:
                ip = f"{prefix}.{random.randint(1, 254)}"
            else:
                ip = f"{random.randint(1, 223)}.{random.randint(1, 254)}.{random.randint(1, 254)}.{random.randint(1, 254)}"
            ips.append(ip)
        return ips
    
    def _get_timestamp(self):
        """Gera timestamp com padrões temporais realistas"""
        # Simular rajadas de tráfego
        if random.random() < 0.1:  # 10% chance de rajada
            self.current_time += timedelta(milliseconds=random.randint(1, 5))
        else:
            self.current_time += timedelta(milliseconds=random.randint(10, 1000))
        return self.current_time.timestamp()
    
    def _is_business_hours(self):
        """Verifica se é horário comercial"""
        return 8 <= self.current_hour <= 18
    
    def generate_mixed_normal_traffic(self, n_samples):
        """Gera tráfego normal com padrões diversos e realistas"""
        traffic = []
        
        with tqdm(total=n_samples, desc="🟢 Tráfego Misto Normal", unit="pkt") as pbar:
            for i in range(n_samples):
                # Padrões variam conforme horário
                if self._is_business_hours():
                    # Horário comercial: mais web, email, videoconferência
                    activity_type = random.choices(
                        ['web_browsing', 'video_streaming', 'email', 'file_transfer', 'video_call', 'cloud_sync'],
                        weights=[30, 25, 15, 10, 15, 5]
                    )[0]
                    src_pool = self.office_ips + self.home_ips
                else:
                    # Fora do horário: mais streaming, jogos, downloads
                    activity_type = random.choices(
                        ['streaming', 'gaming', 'downloads', 'social_media', 'messaging'],
                        weights=[40, 20, 20, 15, 5]
                    )[0]
                    src_pool = self.home_ips + self.mobile_ips
                
                src_ip = random.choice(src_pool)
                dst_ip = random.choice(self.legitimate_servers)
                
                if activity_type in ['web_browsing', 'social_media']:
                    sample = {
                        'timestamp': self._get_timestamp(),
                        'src_ip': src_ip,
                        'dst_ip': dst_ip,
                        'src_port': random.randint(1024, 65535),
                        'dst_port': random.choice([80, 443]),
                        'protocol': 1,
                        'length': random.randint(64, 1500),
                        'tcp_flags': random.choice(['ACK', 'PSH,ACK']),
                        'flow_duration': random.uniform(0.1, 120.0),
                        'packet_count': random.randint(3, 150),
                        'byte_count': random.randint(500, 75000),
                        'Label': 'Benign'
                    }
                    
                elif activity_type in ['video_streaming', 'streaming']:
                    sample = {
                        'timestamp': self._get_timestamp(),
                        'src_ip': src_ip,
                        'dst_ip': dst_ip,
                        'src_port': random.randint(1024, 65535),
                        'dst_port': random.choice([80, 443, 1935, 8080]),
                        'protocol': 1,
                        'length': random.randint(500, 1500),
                        'tcp_flags': 'ACK',
                        'flow_duration': random.uniform(30.0, 7200.0),  # Até 2h
                        'packet_count': random.randint(100, 10000),
                        'byte_count': random.randint(50000, 5000000),
                        'Label': 'Benign'
                    }
                    
                elif activity_type == 'gaming':
                    sample = {
                        'timestamp': self._get_timestamp(),
                        'src_ip': src_ip,
                        'dst_ip': dst_ip,
                        'src_port': random.randint(1024, 65535),
                        'dst_port': random.randint(27000, 28000),
                        'protocol': random.choice([1, 2]),
                        'length': random.randint(64, 200),
                        'tcp_flags': 'ACK' if random.choice([1, 2]) == 1 else '',
                        'flow_duration': random.uniform(0.01, 10.0),
                        'packet_count': random.randint(1, 50),
                        'byte_count': random.randint(64, 10000),
                        'Label': 'Benign'
                    }
                    
                else:  # Outros tipos
                    sample = {
                        'timestamp': self._get_timestamp(),
                        'src_ip': src_ip,
                        'dst_ip': dst_ip,
                        'src_port': random.randint(1024, 65535),
                        'dst_port': random.randint(1, 65535),
                        'protocol': random.choice([1, 2]),
                        'length': random.randint(64, 1500),
                        'tcp_flags': random.choice(['ACK', 'PSH,ACK', '']),
                        'flow_duration': random.uniform(0.1, 300.0),
                        'packet_count': random.randint(1, 200),
                        'byte_count': random.randint(64, 100000),
                        'Label': 'Benign'
                    }
                
                traffic.append(sample)
                pbar.update(1)
        
        return traffic
    
    def generate_subtle_udp_flood(self, n_samples):
        """Gera ataques UDP mais sutis e variados"""
        traffic = []
        
        with tqdm(total=n_samples, desc="🔴 UDP Flood Sutil", unit="pkt") as pbar:
            for i in range(n_samples):
                # Misturar ataques óbvios com sutis
                attack_intensity = random.choices(
                    ['subtle', 'moderate', 'aggressive'],
                    weights=[40, 35, 25]
                )[0]
                
                if attack_intensity == 'subtle':
                    # Ataque disfarçado de tráfego normal
                    src_ip = random.choice(self.home_ips + self.mobile_ips)
                    flow_duration = random.uniform(0.01, 2.0)
                    packet_count = random.randint(1, 20)
                    byte_count = random.randint(64, 5000)
                    
                elif attack_intensity == 'moderate':
                    src_ip = random.choice(self.botnet_ips)
                    flow_duration = random.uniform(0.001, 1.0)
                    packet_count = random.randint(5, 50)
                    byte_count = random.randint(500, 20000)
                    
                else:  # aggressive
                    src_ip = random.choice(self.botnet_ips)
                    flow_duration = random.uniform(0.001, 0.1)
                    packet_count = random.randint(10, 100)
                    byte_count = random.randint(1000, 50000)
                
                # Variar alvos
                target_service = random.choices(
                    ['dns', 'ntp', 'snmp', 'voip', 'gaming'],
                    weights=[35, 25, 15, 15, 10]
                )[0]
                
                if target_service == 'dns':
                    dst_port = 53
                elif target_service == 'ntp':
                    dst_port = 123
                elif target_service == 'snmp':
                    dst_port = 161
                elif target_service == 'voip':
                    dst_port = random.choice([5060, 5061])
                else:
                    dst_port = random.randint(27000, 28000)
                
                sample = {
                    'timestamp': self._get_timestamp(),
                    'src_ip': src_ip,
                    'dst_ip': random.choice(self.legitimate_servers),
                    'src_port': random.randint(1024, 65535),
                    'dst_port': dst_port,
                    'protocol': 2,
                    'length': random.randint(64, 4096),
                    'tcp_flags': '',
                    'flow_duration': flow_duration,
                    'packet_count': packet_count,
                    'byte_count': byte_count,
                    'Label': 'UDP-Flood'
                }
                
                traffic.append(sample)
                pbar.update(1)
        
        return traffic
    
    def generate_syn_flood_variants(self, n_samples):
        """Gera variações de SYN flood, incluindo ataques lentos"""
        traffic = []
        
        with tqdm(total=n_samples, desc="🟡 SYN Flood Variado", unit="pkt") as pbar:
            for i in range(n_samples):
                # Diferentes tipos de SYN flood
                attack_variant = random.choices(
                    ['classic', 'slowloris', 'slow_http', 'distributed'],
                    weights=[30, 25, 25, 20]
                )[0]
                
                if attack_variant == 'slowloris':
                    # Slowloris: conexões lentas para esgotar recursos
                    flow_duration = random.uniform(60.0, 3600.0)  # Muito longo
                    packet_count = random.randint(1, 10)
                    length = random.randint(40, 100)
                    
                elif attack_variant == 'slow_http':
                    flow_duration = random.uniform(30.0, 600.0)
                    packet_count = random.randint(3, 20)
                    length = random.randint(100, 500)
                    
                elif attack_variant == 'distributed':
                    # DDoS distribuído - mais IPs
                    flow_duration = random.uniform(0.001, 1.0)
                    packet_count = random.randint(1, 5)
                    length = random.randint(40, 80)
                    
                else:  # classic
                    flow_duration = random.uniform(0.001, 0.5)
                    packet_count = 1
                    length = random.randint(40, 80)
                
                sample = {
                    'timestamp': self._get_timestamp(),
                    'src_ip': random.choice(self.botnet_ips),
                    'dst_ip': random.choice(self.legitimate_servers),
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([80, 443, 22, 25, 8080]),
                    'protocol': 1,
                    'length': length,
                    'tcp_flags': 'SYN',
                    'flow_duration': flow_duration,
                    'packet_count': packet_count,
                    'byte_count': length * packet_count,
                    'Label': 'SYN-Flood'
                }
                
                traffic.append(sample)
                pbar.update(1)
        
        return traffic
    
    def generate_http_flood_realistic(self, n_samples):
        """Gera ataques HTTP flood mais realistas"""
        traffic = []
        
        with tqdm(total=n_samples, desc="🟠 HTTP Flood Realista", unit="pkt") as pbar:
            for i in range(n_samples):
                # Variar estratégias de ataque HTTP
                attack_type = random.choices(
                    ['get_flood', 'post_flood', 'slow_post', 'browser_based'],
                    weights=[40, 25, 20, 15]
                )[0]
                
                if attack_type == 'get_flood':
                    # Flood de requisições GET
                    flow_duration = random.uniform(0.1, 30.0)
                    packet_count = random.randint(5, 200)
                    byte_count = random.randint(1000, 100000)
                    
                elif attack_type == 'post_flood':
                    # Flood de requisições POST
                    flow_duration = random.uniform(1.0, 60.0)
                    packet_count = random.randint(10, 300)
                    byte_count = random.randint(5000, 200000)
                    
                elif attack_type == 'slow_post':
                    # Slow POST attack
                    flow_duration = random.uniform(60.0, 1800.0)
                    packet_count = random.randint(5, 50)
                    byte_count = random.randint(1000, 50000)
                    
                else:  # browser_based
                    # Ataque baseado em browser (mais sutil)
                    flow_duration = random.uniform(5.0, 120.0)
                    packet_count = random.randint(20, 150)
                    byte_count = random.randint(10000, 150000)
                
                sample = {
                    'timestamp': self._get_timestamp(),
                    'src_ip': random.choice(self.botnet_ips + self.home_ips),
                    'dst_ip': random.choice(self.legitimate_servers),
                    'src_port': random.randint(1024, 65535),
                    'dst_port': random.choice([80, 443, 8080, 8443]),
                    'protocol': 1,
                    'length': random.randint(200, 1500),
                    'tcp_flags': random.choice(['PSH,ACK', 'ACK']),
                    'flow_duration': flow_duration,
                    'packet_count': packet_count,
                    'byte_count': byte_count,
                    'Label': 'HTTP-Flood'
                }
                
                traffic.append(sample)
                pbar.update(1)
        
        return traffic

def generate_test_dataset(total_samples=50000):
    """
    Gera dataset de teste com distribuição ALEATÓRIA e realista
    """
    print("🧪 GERANDO DATASET DE TESTE REALISTA")
    print("=" * 60)
    print(f"Total de amostras: {total_samples:,}")
    
    # Distribuição aleatória mais realista
    # Em cenários reais, ataques são minoria
    benign_weight = random.uniform(60, 85)  # 60-85% normal
    remaining = 100 - benign_weight
    
    udp_weight = random.uniform(5, remaining * 0.5)
    remaining -= udp_weight
    
    syn_weight = random.uniform(5, remaining * 0.7)
    remaining -= syn_weight
    
    http_weight = remaining
    
    # Converter para contagem
    benign_count = int(total_samples * benign_weight / 100)
    udp_flood_count = int(total_samples * udp_weight / 100)
    syn_flood_count = int(total_samples * syn_weight / 100)
    http_flood_count = total_samples - benign_count - udp_flood_count - syn_flood_count
    
    print(f"📊 Distribuição ALEATÓRIA:")
    print(f"  🟢 Normal: {benign_count:,} ({benign_weight:.1f}%)")
    print(f"  🔴 UDP-Flood: {udp_flood_count:,} ({udp_weight:.1f}%)")
    print(f"  🟡 SYN-Flood: {syn_flood_count:,} ({syn_weight:.1f}%)")
    print(f"  🟠 HTTP-Flood: {http_flood_count:,} ({http_weight:.1f}%)")
    print()
    
    generator = TestTrafficGenerator()
    all_traffic = []
    
    # Gerar tráfego com padrões realistas
    all_traffic.extend(generator.generate_mixed_normal_traffic(benign_count))
    all_traffic.extend(generator.generate_subtle_udp_flood(udp_flood_count))
    all_traffic.extend(generator.generate_syn_flood_variants(syn_flood_count))
    all_traffic.extend(generator.generate_http_flood_realistic(http_flood_count))
    
    # Converter para DataFrame
    print("\n📋 Criando DataFrame de teste...")
    df = pd.DataFrame(all_traffic)
    
    # Embaralhar com padrões temporais mais realistas
    print("🔀 Embaralhando com padrões temporais...")
    df = df.sample(frac=1, random_state=456).reset_index(drop=True)
    
    # Salvar
    output_path = "data/raw/test_traffic_realistic.csv"
    os.makedirs("data/raw", exist_ok=True)
    
    print(f"💾 Salvando em: {output_path}")
    df.to_csv(output_path, index=False)
    
    # Estatísticas finais
    print(f"\n📊 ESTATÍSTICAS FINAIS DO TESTE:")
    print(f"Total de registros: {len(df):,}")
    print(f"Distribuição real:")
    label_counts = df['Label'].value_counts()
    for label, count in label_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  {label}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n✅ Dataset de teste criado com sucesso!")
    return df

if __name__ == "__main__":
    # Gerar dataset de teste
    df_test = generate_test_dataset(50000)
    
    print("\n" + "=" * 60)
    print("🎉 DATASET DE TESTE PRONTO!")
    print("📁 Localização: data/raw/test_traffic_realistic.csv")
    print("🚀 Próximo passo: Treinar modelo com dados de treino e testar com estes dados")
