#!/usr/bin/env python3
"""
🎯 SCRIPT PRINCIPAL DO SISTEMA DDoS DETECTION
============================================

Este é o ponto de entrada principal do sistema.
Escolha uma das opções para executar:

1. Treinar modelo - Treina um novo modelo com dados realistas
2. Fazer inferência - Analisa novos dados para detectar DDoS
3. Executar testes - Valida o sistema completo
4. Preprocessar dados - Converte PCAP para formato de treino

Autor: Seu Nome
Data: 2025
"""

import os
import sys
from pathlib import Path

# Adicionar src ao path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def show_menu():
    """Mostra o menu principal"""
    print("🛡️  SISTEMA DE DETECÇÃO DDoS - Random Forest")
    print("=" * 60)
    print("Escolha uma opção:")
    print()
    print("1. 🧠 Treinar novo modelo")
    print("2. 🔍 Fazer inferência em dados")
    print("3. 🧪 Executar testes do sistema")
    print("4. ⚙️  Preprocessar dados PCAP")
    print("5. 📊 Ver status do projeto")
    print("0. ❌ Sair")
    print()

def train_model():
    """Treina um novo modelo"""
    print("🧠 INICIANDO TREINAMENTO DO MODELO...")
    os.system("python src/models/treinar_modelo_realista.py")

def run_inference():
    """Executa inferência"""
    print("🔍 INICIANDO SISTEMA DE INFERÊNCIA...")
    os.system("python src/app_inferencia.py")

def run_tests():
    """Executa todos os testes"""
    print("🧪 EXECUTANDO TESTES DO SISTEMA...")
    print("\n1. Teste de integração do modelo:")
    os.system("python tests/integration/testar_modelo_realista.py")
    
    print("\n2. Teste do pipeline completo:")
    os.system("python tests/integration/test_pipeline.py")

def preprocess_data():
    """Preprocessa dados PCAP"""
    print("⚙️  INICIANDO PREPROCESSAMENTO...")
    os.system("python src/preprocessing/preprocessamento_realista.py")

def show_status():
    """Mostra status do projeto"""
    print("📊 STATUS DO PROJETO")
    print("=" * 40)
    
    # Verificar se modelo existe
    model_path = Path("data/models/ddos_model_realista.pkl")
    if model_path.exists():
        print("✅ Modelo treinado: SIM")
        print(f"   📁 Localização: {model_path}")
    else:
        print("❌ Modelo treinado: NÃO")
        print("   💡 Execute opção 1 para treinar")
    
    # Verificar dados
    data_path = Path("data/processed")
    if data_path.exists() and list(data_path.glob("*.csv")):
        print("✅ Dados processados: SIM")
        datasets = list(data_path.glob("*.csv"))
        for ds in datasets[:3]:  # Mostrar só os 3 primeiros
            print(f"   📄 {ds.name}")
    else:
        print("❌ Dados processados: NÃO")
        print("   💡 Execute opção 4 para processar")
    
    # Verificar testes
    test_results = Path("data/processed/teste_modelo_realista.csv")
    if test_results.exists():
        print("✅ Última execução de teste: SIM")
        print(f"   📄 Resultados: {test_results}")
    else:
        print("❌ Testes executados: NÃO")
        print("   💡 Execute opção 3 para testar")

def main():
    """Função principal"""
    while True:
        show_menu()
        
        try:
            choice = input("Digite sua escolha: ").strip()
            
            if choice == "0":
                print("👋 Até logo!")
                break
            elif choice == "1":
                train_model()
            elif choice == "2":
                run_inference()
            elif choice == "3":
                run_tests()
            elif choice == "4":
                preprocess_data()
            elif choice == "5":
                show_status()
            else:
                print("❌ Opção inválida! Tente novamente.")
            
            input("\nPressione ENTER para continuar...")
            
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()
