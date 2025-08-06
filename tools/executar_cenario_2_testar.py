#!/usr/bin/env python
"""
🔴 CENÁRIO 2: TESTAR MODELO COM DATASET DIFERENTE
=================================================

Script para executar APENAS o teste do modelo:
1. Gerar dataset de teste (diferente do treinamento)
2. Carregar modelo previamente treinado
3. Executar teste e avaliar performance
4. Gerar relatório de resultados

Execução: python executar_cenario_2_testar.py

⚠️ PREREQUISITO: Cenário 1 deve ter sido executado primeiro
"""

import os
import subprocess
import sys
from pathlib import Path

def verificar_prerequisites():
    """Verifica se o modelo foi treinado"""
    arquivos_necessarios = [
        "data/models/ddos_model_realista.pkl",
        "data/models/scaler_realista.joblib", 
        "data/models/label_mapping_realista.json"
    ]
    
    for arquivo in arquivos_necessarios:
        if not os.path.exists(arquivo):
            return False, arquivo
    
    return True, None

def executar_cenario_testar():
    """Executa cenário completo de teste"""
    
    print("🔴 CENÁRIO 2: TESTE DE MODELO")
    print("=" * 60)
    print("🎯 Objetivo: Dataset Novo → Carregar Modelo → Testar → Relatório")
    print()
    
    # Verificar prerequisites
    print("🔍 Verificando prerequisites...")
    tem_modelo, arquivo_faltando = verificar_prerequisites()
    
    if not tem_modelo:
        print(f"❌ Modelo não encontrado: {arquivo_faltando}")
        print("⚠️ Execute primeiro o cenário 1:")
        print("   python executar_cenario_1_treinar.py")
        return False
    
    print("✅ Modelo treinado encontrado!")
    print()
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("experiments"):
        print("❌ Erro: Execute este script da raiz do projeto")
        return False
    
    try:
        print("📊 PASSO 1/2: Gerando dataset de teste (diferente do treino)...")
        print("-" * 50)
        result = subprocess.run([
            sys.executable, "experiments/gerar_trafego_teste.py"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode != 0:
            print(f"❌ Erro na geração de dados de teste: {result.stderr}")
            return False
        
        print("✅ Dataset de teste gerado com sucesso!")
        print(f"📁 Salvo em: data/raw/test_traffic_realistic.csv")
        print()
        
        print("🧪 PASSO 2/2: Testando modelo com dataset novo...")
        print("-" * 50)
        result = subprocess.run([
            sys.executable, "tools/teste_definitivo.py"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode != 0:
            print(f"❌ Erro no teste: {result.stderr}")
            return False
            
        print("✅ Teste executado com sucesso!")
        print()
        
        print("🎉 CENÁRIO 2 COMPLETO!")
        print("=" * 60)
        print("📦 ARQUIVOS GERADOS:")
        arquivos_teste = [
            "data/raw/test_traffic_realistic.csv - Dataset de teste",
            "data/processed/test_features_realistic.csv - Features de teste",
            "data/processed/teste_modelo_trafego_realista.csv - Resultados detalhados"
        ]
        
        for arquivo in arquivos_teste:
            caminho = arquivo.split(" - ")[0]
            if os.path.exists(caminho):
                print(f"  ✅ {arquivo}")
            else:
                print(f"  ❌ {arquivo}")
        
        print()
        print("📊 ANÁLISE DOS RESULTADOS:")
        
        # Tentar mostrar resumo se o arquivo existe
        resultado_path = "data/processed/teste_modelo_trafego_realista.csv"
        if os.path.exists(resultado_path):
            try:
                import pandas as pd
                df = pd.read_csv(resultado_path)
                accuracy = df['Correto'].mean()
                total_samples = len(df)
                
                print(f"   🎯 Amostras testadas: {total_samples:,}")
                print(f"   📈 Acurácia geral: {accuracy:.3f} ({accuracy*100:.1f}%)")
                
                # Distribuição por classe
                print(f"   📊 Distribuição dos dados de teste:")
                label_counts = df['Label'].value_counts()
                for label, count in label_counts.items():
                    correct = df[df['Label'] == label]['Correto'].sum()
                    class_acc = (correct / count) * 100
                    print(f"      {label}: {count:,} amostras ({class_acc:.1f}% acertos)")
                    
            except Exception as e:
                print(f"   ⚠️ Não foi possível analisar resultados: {e}")
        
        print()
        print("📋 RELATÓRIOS DISPONÍVEIS:")
        print("   📄 Resultados detalhados: data/processed/teste_modelo_trafego_realista.csv")
        print("   📄 Relatório completo: Execute tools/gerar_relatorio_final.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    print("🔴 INICIANDO CENÁRIO 2: TESTE")
    print("=" * 60)
    
    success = executar_cenario_testar()
    
    if success:
        print("\n🎉 CENÁRIO 2 EXECUTADO COM SUCESSO!")
        print("📊 Teste completo do modelo finalizado")
        print("📋 Verifique os relatórios gerados")
    else:
        print("\n❌ FALHA NO CENÁRIO 2!")
        print("🔧 Verifique os erros e prerequisites")
    
    print("=" * 60)
