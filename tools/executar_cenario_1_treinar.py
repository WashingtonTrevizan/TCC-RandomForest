#!/usr/bin/env python
"""
🟢 CENÁRIO 1: TREINAR MODELO COM DATASET
========================================

Script para executar APENAS o treinamento do modelo:
1. Gerar dataset de treinamento
2. Pré-processar dados  
3. Treinar modelo Random Forest
4. Salvar modelo treinado

Execução: python executar_cenario_1_treinar.py
"""

import os
import subprocess
import sys
from pathlib import Path

def executar_cenario_treinar():
    """Executa cenário completo de treinamento"""
    
    print("🟢 CENÁRIO 1: TREINAMENTO DE MODELO")
    print("=" * 60)
    print("🎯 Objetivo: Dataset → Processamento → Treinamento → Modelo")
    print()
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("experiments"):
        print("❌ Erro: Execute este script da raiz do projeto")
        return False
    
    try:
        print("📊 PASSO 1/3: Gerando dataset de treinamento...")
        print("-" * 50)
        result = subprocess.run([
            sys.executable, "experiments/gerar_trafego_treinamento.py"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode != 0:
            print(f"❌ Erro na geração de dados: {result.stderr}")
            return False
        
        print("✅ Dataset de treinamento gerado com sucesso!")
        print(f"📁 Salvo em: data/raw/training_traffic_realistic.csv")
        print()
        
        print("⚙️ PASSO 2/3: Pré-processando dados...")
        print("-" * 50)
        result = subprocess.run([
            sys.executable, "src/preprocessing/preprocessamento_realista.py"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode != 0:
            print(f"❌ Erro no pré-processamento: {result.stderr}")
            return False
            
        print("✅ Dados pré-processados com sucesso!")
        print(f"📁 Salvo em: data/processed/dataset_preprocessado_realista.csv")
        print()
        
        print("🤖 PASSO 3/3: Treinando modelo...")
        print("-" * 50)
        result = subprocess.run([
            sys.executable, "src/models/treinar_modelo_realista.py"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode != 0:
            print(f"❌ Erro no treinamento: {result.stderr}")
            return False
        
        print("✅ Modelo treinado com sucesso!")
        print()
        
        print("🎉 CENÁRIO 1 COMPLETO!")
        print("=" * 60)
        print("📦 ARQUIVOS GERADOS:")
        arquivos = [
            "data/raw/training_traffic_realistic.csv - Dataset bruto",
            "data/processed/dataset_preprocessado_realista.csv - Dataset processado", 
            "data/models/ddos_model_realista.pkl - Modelo treinado",
            "data/models/scaler_realista.joblib - Normalizador",
            "data/models/label_mapping_realista.json - Mapeamento de labels"
        ]
        
        for arquivo in arquivos:
            if os.path.exists(arquivo.split(" - ")[0]):
                print(f"  ✅ {arquivo}")
            else:
                print(f"  ❌ {arquivo}")
        
        print()
        print("🚀 PRÓXIMO PASSO: Execute cenário 2 para testar o modelo")
        print("   python executar_cenario_2_testar.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🟢 INICIANDO CENÁRIO 1: TREINAMENTO")
    print("=" * 60)
    
    success = executar_cenario_treinar()
    
    if success:
        print("\n🎉 CENÁRIO 1 EXECUTADO COM SUCESSO!")
        print("📦 Modelo pronto para ser testado no cenário 2")
    else:
        print("\n❌ FALHA NO CENÁRIO 1!")
        print("🔧 Verifique os erros e tente novamente")
    
    print("=" * 60)
