"""
Script para validar o modelo treinado usando tráfego simulado
Testa se o modelo está detectando corretamente os diferentes tipos de ataque
"""
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

def carregar_resultados(arquivo_resultados):
    """Carrega os resultados da inferência"""
    if not os.path.exists(arquivo_resultados):
        raise FileNotFoundError(f"Arquivo de resultados não encontrado: {arquivo_resultados}")
    
    df = pd.read_csv(arquivo_resultados)
    print(f"[INFO] Resultados carregados: {df.shape}")
    return df

def analisar_deteccoes(df):
    """Analisa as detecções do modelo"""
    print("\n🔍 ANÁLISE DAS DETECÇÕES")
    print("="*50)
    
    # Distribuição geral das predições
    print("DISTRIBUIÇÃO DAS PREDIÇÕES:")
    predicoes = df['Predito'].value_counts()
    total = len(df)
    
    for classe, count in predicoes.items():
        porcentagem = (count / total) * 100
        print(f"  {classe:12} | {count:6} ({porcentagem:5.1f}%)")
    
    return predicoes

def validar_ataques_syn_flood(df):
    """Valida detecção de ataques SYN Flood"""
    print("\n🎯 VALIDAÇÃO: ATAQUES SYN FLOOD")
    print("-" * 40)
    
    # Identificar potenciais SYN floods baseado nas características
    syn_packets = df[df['tcp_flags'] == 2]  # Pacotes com flag SYN
    
    print(f"Total de pacotes SYN: {len(syn_packets)}")
    
    if len(syn_packets) > 0:
        syn_detections = syn_packets['Predito'].value_counts()
        print("Detecções em pacotes SYN:")
        for classe, count in syn_detections.items():
            porcentagem = (count / len(syn_packets)) * 100
            print(f"  {classe:12} | {count:4} ({porcentagem:5.1f}%)")
        
        # Verificar se SYN floods foram detectados corretamente
        syn_flood_detected = syn_packets[syn_packets['Predito'] == 'SYN-Flood']
        print(f"\n✓ SYN-Floods detectados: {len(syn_flood_detected)}")
        
        if len(syn_flood_detected) > 0:
            print("Características dos SYN-Floods detectados:")
            print(f"  Tamanho médio: {syn_flood_detected['length'].mean():.1f} bytes")
            print(f"  IPs únicos origem: {syn_flood_detected['src_ip'].nunique()}")
            print(f"  IPs únicos destino: {syn_flood_detected['dst_ip'].nunique()}")
    
    return len(syn_packets), len(syn_packets[syn_packets['Predito'] == 'SYN-Flood'])

def validar_ataques_udp_flood(df):
    """Valida detecção de ataques UDP Flood"""
    print("\n🎯 VALIDAÇÃO: ATAQUES UDP FLOOD")
    print("-" * 40)
    
    # Identificar potenciais UDP floods
    udp_packets = df[df['protocol'] == 'UDP']
    udp_grandes = udp_packets[udp_packets['length'] > 500]  # Pacotes UDP grandes
    
    print(f"Total de pacotes UDP: {len(udp_packets)}")
    print(f"Pacotes UDP grandes (>500 bytes): {len(udp_grandes)}")
    
    if len(udp_grandes) > 0:
        udp_detections = udp_grandes['Predito'].value_counts()
        print("Detecções em pacotes UDP grandes:")
        for classe, count in udp_detections.items():
            porcentagem = (count / len(udp_grandes)) * 100
            print(f"  {classe:12} | {count:4} ({porcentagem:5.1f}%)")
        
        udp_flood_detected = udp_grandes[udp_grandes['Predito'] == 'UDP-Flood']
        print(f"\n✓ UDP-Floods detectados: {len(udp_flood_detected)}")
        
        if len(udp_flood_detected) > 0:
            print("Características dos UDP-Floods detectados:")
            print(f"  Tamanho médio: {udp_flood_detected['length'].mean():.1f} bytes")
            print(f"  Portas de destino: {udp_flood_detected['dst_port'].value_counts().head(3).to_dict()}")
    
    return len(udp_grandes), len(udp_grandes[udp_grandes['Predito'] == 'UDP-Flood'])

def validar_ataques_http_flood(df):
    """Valida detecção de ataques HTTP Flood"""
    print("\n🎯 VALIDAÇÃO: ATAQUES HTTP FLOOD")
    print("-" * 40)
    
    # Identificar potenciais HTTP floods
    http_packets = df[df['dst_port'].isin([80, 443])]
    
    print(f"Total de pacotes HTTP/HTTPS: {len(http_packets)}")
    
    if len(http_packets) > 0:
        http_detections = http_packets['Predito'].value_counts()
        print("Detecções em pacotes HTTP/HTTPS:")
        for classe, count in http_detections.items():
            porcentagem = (count / len(http_packets)) * 100
            print(f"  {classe:12} | {count:4} ({porcentagem:5.1f}%)")
        
        http_flood_detected = http_packets[http_packets['Predito'] == 'HTTP-Flood']
        print(f"\n✓ HTTP-Floods detectados: {len(http_flood_detected)}")
        
        if len(http_flood_detected) > 0:
            print("Características dos HTTP-Floods detectados:")
            print(f"  Portas: {http_flood_detected['dst_port'].value_counts().to_dict()}")
            print(f"  IPs únicos origem: {http_flood_detected['src_ip'].nunique()}")
    
    return len(http_packets), len(http_packets[http_packets['Predito'] == 'HTTP-Flood'])

def validar_trafego_normal(df):
    """Valida detecção de tráfego normal"""
    print("\n🎯 VALIDAÇÃO: TRÁFEGO NORMAL")
    print("-" * 40)
    
    # Tráfego que deveria ser classificado como normal
    trafego_normal = df[
        (df['tcp_flags'] != 2) &  # Não é SYN
        ~((df['protocol'] == 'UDP') & (df['length'] > 500)) &  # Não é UDP grande
        (df['dst_port'].isin([80, 443, 53, 22, 25, 110, 143]))  # Portas comuns
    ]
    
    print(f"Tráfego esperado como normal: {len(trafego_normal)}")
    
    if len(trafego_normal) > 0:
        normal_detections = trafego_normal['Predito'].value_counts()
        print("Detecções em tráfego normal:")
        for classe, count in normal_detections.items():
            porcentagem = (count / len(trafego_normal)) * 100
            print(f"  {classe:12} | {count:4} ({porcentagem:5.1f}%)")
        
        benign_detected = len(trafego_normal[trafego_normal['Predito'] == 'Benign'])
        accuracy_normal = (benign_detected / len(trafego_normal)) * 100
        print(f"\n✓ Precisão no tráfego normal: {accuracy_normal:.1f}%")
    
    return len(trafego_normal), len(trafego_normal[trafego_normal['Predito'] == 'Benign'])

def calcular_metricas_gerais(df):
    """Calcula métricas gerais do modelo"""
    print("\n📊 MÉTRICAS GERAIS DO MODELO")
    print("="*50)
    
    total_amostras = len(df)
    total_ataques_detectados = len(df[df['Predito'] != 'Benign'])
    total_trafego_normal = len(df[df['Predito'] == 'Benign'])
    
    print(f"Total de amostras testadas: {total_amostras}")
    print(f"Ataques detectados: {total_ataques_detectados} ({(total_ataques_detectados/total_amostras)*100:.1f}%)")
    print(f"Tráfego normal: {total_trafego_normal} ({(total_trafego_normal/total_amostras)*100:.1f}%)")
    
    # Análise temporal se houver timestamp
    if 'timestamp' in df.columns:
        try:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            periodo = df['timestamp'].max() - df['timestamp'].min()
            print(f"Período analisado: {periodo}")
            
            # Taxa de detecção por tempo
            if periodo.total_seconds() > 0:
                taxa_deteccao = total_ataques_detectados / periodo.total_seconds()
                print(f"Taxa de detecção: {taxa_deteccao:.2f} ataques/segundo")
        except:
            print("Não foi possível analisar dados temporais")

def gerar_relatorio_final(syn_stats, udp_stats, http_stats, normal_stats):
    """Gera relatório final da validação"""
    print("\n📋 RELATÓRIO FINAL DA VALIDAÇÃO")
    print("="*60)
    
    print("RESUMO DAS DETECÇÕES:")
    print(f"  SYN-Flood:  {syn_stats[1]}/{syn_stats[0]} pacotes SYN detectados como ataque")
    print(f"  UDP-Flood:  {udp_stats[1]}/{udp_stats[0]} pacotes UDP grandes detectados como ataque")
    print(f"  HTTP-Flood: {http_stats[1]}/{http_stats[0]} pacotes HTTP detectados como ataque")
    print(f"  Benign:     {normal_stats[1]}/{normal_stats[0]} tráfego normal detectado corretamente")
    
    # Calcular taxa de sucesso geral
    total_esperado = syn_stats[0] + udp_stats[0] + http_stats[0] + normal_stats[0]
    total_correto = syn_stats[1] + udp_stats[1] + http_stats[1] + normal_stats[1]
    
    if total_esperado > 0:
        taxa_sucesso = (total_correto / total_esperado) * 100
        print(f"\n🎯 TAXA DE SUCESSO GERAL: {taxa_sucesso:.1f}%")
        
        if taxa_sucesso >= 80:
            print("✅ MODELO FUNCIONANDO BEM!")
        elif taxa_sucesso >= 60:
            print("⚠️  MODELO PRECISA DE AJUSTES")
        else:
            print("❌ MODELO PRECISA SER RETREINADO")
    
    print("\n💡 RECOMENDAÇÕES:")
    if syn_stats[0] > 0 and syn_stats[1] == 0:
        print("- Ajustar regras de detecção de SYN-Flood")
    if udp_stats[0] > 0 and udp_stats[1] == 0:
        print("- Ajustar regras de detecção de UDP-Flood") 
    if http_stats[0] > 0 and http_stats[1] == 0:
        print("- Ajustar regras de detecção de HTTP-Flood")
    if normal_stats[0] > 0 and (normal_stats[1] / normal_stats[0]) < 0.8:
        print("- Reduzir falsos positivos no tráfego normal")

def main():
    """Função principal de validação"""
    if len(sys.argv) < 2:
        print("Uso: python validar_modelo.py <arquivo_resultados_inferencia>")
        print("Exemplo: python validar_modelo.py data/resultados_teste.csv")
        sys.exit(1)
    
    arquivo_resultados = sys.argv[1]
    
    print("🧪 VALIDAÇÃO DO MODELO DDOS")
    print("="*60)
    print(f"Arquivo de resultados: {arquivo_resultados}")
    print(f"Data/Hora: {datetime.now()}")
    
    try:
        # Carregar resultados
        df = carregar_resultados(arquivo_resultados)
        
        # Análise geral
        analisar_deteccoes(df)
        
        # Validações específicas
        syn_stats = validar_ataques_syn_flood(df)
        udp_stats = validar_ataques_udp_flood(df)
        http_stats = validar_ataques_http_flood(df)
        normal_stats = validar_trafego_normal(df)
        
        # Métricas gerais
        calcular_metricas_gerais(df)
        
        # Relatório final
        gerar_relatorio_final(syn_stats, udp_stats, http_stats, normal_stats)
        
    except Exception as e:
        print(f"❌ Erro durante a validação: {e}")
        raise

if __name__ == "__main__":
    main()
