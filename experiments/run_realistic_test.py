#!/usr/bin/env python3
"""
🎯 PIPELINE COMPLETO - TESTE REAL DO SISTEMA DDoS
================================================

Executa o teste completo e realista do sistema:

1. 📊 Gera tráfego de TREINAMENTO (distribuição balanceada)
2. 🧠 Treina modelo com dados realistas
3. 🧪 Gera tráfego de TESTE (distribuição aleatória)
4. 🎯 Testa modelo em cenário real
5. 📈 Analisa performance e gera relatório

Este é o teste definitivo para validar se o sistema
funciona em condições reais!

Autor: Sistema DDoS Detection
Data: 2025
"""

import os
import sys
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

# Adicionar src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def run_command(command, description):
    """Executa comando e mostra progresso"""
    print(f"\n🔄 {description}")
    print("=" * 60)
    
    # Usar o Python do ambiente virtual
    python_exe = ".venv/Scripts/python.exe"
    if command.startswith("python "):
        command = command.replace("python ", f"{python_exe} ")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print("✅ Sucesso!")
        if result.stdout:
            print("📋 Output:")
            print(result.stdout[-500:])  # Últimas 500 chars
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro: {e}")
        if e.stderr:
            print("📋 Erro detalhado:")
            print(e.stderr[-500:])
        return False

def check_file_exists(filepath, description):
    """Verifica se arquivo foi criado"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}: {filepath} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description} não encontrado: {filepath}")
        return False

def analyze_results():
    """Analisa os resultados do teste completo"""
    print("\n📊 ANÁLISE DOS RESULTADOS")
    print("=" * 60)
    
    try:
        # Carregar dados de treinamento
        train_path = "data/raw/training_traffic_realistic.csv"
        if os.path.exists(train_path):
            df_train = pd.read_csv(train_path)
            print(f"📈 DADOS DE TREINAMENTO:")
            print(f"   Total: {len(df_train):,} amostras")
            train_dist = df_train['Label'].value_counts(normalize=True) * 100
            for label, pct in train_dist.items():
                print(f"   {label}: {pct:.1f}%")
        
        # Carregar dados de teste
        test_path = "data/raw/test_traffic_realistic.csv"
        if os.path.exists(test_path):
            df_test = pd.read_csv(test_path)
            print(f"\n🧪 DADOS DE TESTE:")
            print(f"   Total: {len(df_test):,} amostras")
            test_dist = df_test['Label'].value_counts(normalize=True) * 100
            for label, pct in test_dist.items():
                print(f"   {label}: {pct:.1f}%")
        
        # Carregar resultados de teste do modelo
        results_path = "data/processed/teste_modelo_realista.csv"
        if os.path.exists(results_path):
            df_results = pd.read_csv(results_path)
            print(f"\n🎯 RESULTADOS DO MODELO:")
            
            # Calcular matriz de confusão simplificada
            mapping = {
                'Normal': 'Benign',
                'UDP-Flood': 'UDP-Flood',
                'SYN-Flood': 'SYN-Flood', 
                'HTTP-Flood': 'HTTP-Flood'
            }
            
            print(f"   Total predições: {len(df_results):,}")
            
            for real_type, expected in mapping.items():
                if real_type in df_results['tipo_real'].values:
                    subset = df_results[df_results['tipo_real'] == real_type]
                    correct = len(subset[subset['Predição'] == expected])
                    total = len(subset)
                    accuracy = (correct / total * 100) if total > 0 else 0
                    
                    status = "✅" if accuracy >= 90 else "⚠️" if accuracy >= 70 else "❌"
                    print(f"   {status} {real_type:12}: {correct:4}/{total:4} ({accuracy:5.1f}%)")
            
            # Análise de confiança
            if 'Confiança' in df_results.columns:
                avg_confidence = df_results['Confiança'].mean()
                low_confidence = len(df_results[df_results['Confiança'] < 0.8])
                print(f"\n📊 CONFIANÇA DAS PREDIÇÕES:")
                print(f"   Confiança média: {avg_confidence:.3f}")
                print(f"   Predições com baixa confiança: {low_confidence}")
        
        # Verificar modelo treinado
        model_path = "data/models/ddos_model_realista.pkl"
        if os.path.exists(model_path):
            print(f"\n🧠 MODELO TREINADO:")
            print(f"   Localização: {model_path}")
            
            # Carregar metadados se existir
            metadata_path = "data/models/model_realista_metadata.json"
            if os.path.exists(metadata_path):
                import json
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                print(f"   Acurácia de treino: {metadata.get('train_accuracy', 'N/A'):.3f}")
                print(f"   Acurácia de teste: {metadata.get('test_accuracy', 'N/A'):.3f}")
                print(f"   CV Score: {metadata.get('cv_score_mean', 'N/A'):.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na análise: {e}")
        return False

def main():
    """Executa pipeline completo de teste"""
    print("🎯 PIPELINE COMPLETO - TESTE REAL DO SISTEMA DDoS")
    print("=" * 80)
    print(f"🕐 Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    steps_completed = 0
    total_steps = 6
    
    # PASSO 1: Gerar dados de treinamento
    print(f"📊 PASSO 1/{total_steps}: Gerando dados de treinamento...")
    if run_command("python experiments/gerar_trafego_treinamento.py", 
                   "Criando dataset de treinamento balanceado"):
        if check_file_exists("data/raw/training_traffic_realistic.csv", "Dataset de treinamento"):
            steps_completed += 1
    
    # PASSO 2: Processar dados de treinamento  
    print(f"\n⚙️ PASSO 2/{total_steps}: Convertendo dados para features...")
    
    # Converter CSV sintético para formato compatível com o pipeline
    train_path = "data/raw/training_traffic_realistic.csv"
    processed_path = "data/processed/dataset_realista.csv"
    
    if os.path.exists(train_path):
        print("🔄 Convertendo formato dos dados...")
        try:
            df = pd.read_csv(train_path)
            
            # Calcular features necessárias a partir dos dados sintéticos
            df['flow_duration'] = df['flow_duration']
            df['packet_rate'] = df['packet_count'] / (df['flow_duration'] + 0.001)
            df['byte_rate'] = df['byte_count'] / (df['flow_duration'] + 0.001)
            
            # Simular contagens de IP (dados sintéticos)
            df['src_ip_count'] = 1  # Simplificado
            df['dst_ip_count'] = 1  # Simplificado
            
            # TCP SYN flag
            df['tcp_syn'] = (df['tcp_flags'].str.contains('SYN', na=False)).astype(int)
            
            # Manter apenas colunas necessárias
            required_cols = ['flow_duration', 'packet_rate', 'byte_rate', 
                           'src_ip_count', 'dst_ip_count', 'tcp_syn', 
                           'length', 'dst_port', 'protocol', 'Label']
            
            df_final = df[required_cols].copy()
            
            # Salvar
            os.makedirs("data/processed", exist_ok=True)
            df_final.to_csv(processed_path, index=False)
            print(f"✅ Dados convertidos: {processed_path}")
            steps_completed += 1
            
        except Exception as e:
            print(f"❌ Erro na conversão: {e}")
    
    # PASSO 3: Preprocessar dados
    print(f"\n🔧 PASSO 3/{total_steps}: Preprocessando dados...")
    if run_command("python src/preprocessing/preprocessamento_realista.py",
                   "Normalizando e preparando dados"):
        if check_file_exists("data/processed/dataset_preprocessado_realista.csv", "Dados preprocessados"):
            steps_completed += 1
    
    # PASSO 4: Treinar modelo
    print(f"\n🧠 PASSO 4/{total_steps}: Treinando modelo...")
    if run_command("python src/models/treinar_modelo_realista.py",
                   "Treinando Random Forest com dados realistas"):
        if check_file_exists("data/models/ddos_model_realista.pkl", "Modelo treinado"):
            steps_completed += 1
    
    # PASSO 5: Gerar dados de teste
    print(f"\n🧪 PASSO 5/{total_steps}: Gerando dados de teste...")
    if run_command("python experiments/gerar_trafego_teste.py",
                   "Criando dataset de teste com distribuição aleatória"):
        if check_file_exists("data/raw/test_traffic_realistic.csv", "Dataset de teste"):
            steps_completed += 1
    
    # PASSO 6: Testar modelo
    print(f"\n🎯 PASSO 6/{total_steps}: Testando modelo...")
    if run_command("python tests/integration/testar_modelo_realista.py",
                   "Validando detecção em cenário real"):
        if check_file_exists("data/processed/teste_modelo_realista.csv", "Resultados do teste"):
            steps_completed += 1
    
    # ANÁLISE FINAL
    print(f"\n📈 ANÁLISE FINAL DOS RESULTADOS")
    analyze_results()
    
    # RELATÓRIO FINAL
    print(f"\n" + "=" * 80)
    print(f"🏁 PIPELINE COMPLETO FINALIZADO!")
    print(f"✅ Passos concluídos: {steps_completed}/{total_steps}")
    print(f"📊 Taxa de sucesso: {(steps_completed/total_steps)*100:.1f}%")
    print(f"🕐 Término: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if steps_completed == total_steps:
        print(f"\n🎉 TESTE COMPLETO REALIZADO COM SUCESSO!")
        print(f"📁 Verifique os resultados em:")
        print(f"   • data/processed/teste_modelo_realista.csv")
        print(f"   • data/models/model_realista_metadata.json")
        print(f"🚀 Sistema pronto para produção!")
    else:
        print(f"\n⚠️  ALGUNS PASSOS FALHARAM")
        print(f"🔧 Verifique os erros acima e execute novamente")
    
    return steps_completed == total_steps

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
