"""
Script para testar o pipeline completo corrigido
Execute este script para verificar se tudo está funcionando
"""
import os
import sys
import pandas as pd

def test_feature_engineering():
    """Testa o módulo de feature engineering"""
    print("="*60)
    print("TESTE 1: Feature Engineering")
    print("="*60)
    
    try:
        sys.path.append("tools")
        from feature_engineering import full_feature_pipeline, REQUIRED_FEATURES
        
        # Carregar dados de exemplo
        df = pd.read_csv("data/pcap_convertido.csv")
        print(f"✓ Dados carregados: {df.shape}")
        
        # Testar pipeline
        df_processed = full_feature_pipeline(df.head(1000), include_labels=True)  # Só uma amostra para teste
        print(f"✓ Pipeline executado: {df_processed.shape}")
        
        # Verificar features
        missing = [f for f in REQUIRED_FEATURES if f not in df_processed.columns]
        if missing:
            print(f"✗ Features faltantes: {missing}")
            return False
        else:
            print(f"✓ Todas as features presentes: {REQUIRED_FEATURES}")
        
        print("✅ Feature Engineering: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Feature Engineering: FALHOU - {e}")
        return False

def test_data_processing():
    """Testa o processamento completo dos dados"""
    print("\n" + "="*60)
    print("TESTE 2: Processamento de Dados")
    print("="*60)
    
    try:
        # Executar pipeline de tratamento
        print("Executando tratar_csv_para_ia.py...")
        os.system("python tools/tratar_csv_para_ia.py")
        
        # Verificar se arquivo foi criado
        if os.path.exists("data/dataset_final.csv"):
            df = pd.read_csv("data/dataset_final.csv")
            print(f"✓ Dataset final criado: {df.shape}")
            print(f"✓ Colunas: {list(df.columns)}")
            
            if 'Label' in df.columns:
                print(f"✓ Distribuição de labels:")
                print(df['Label'].value_counts())
        else:
            print("❌ Arquivo dataset_final.csv não foi criado")
            return False
        
        print("✅ Processamento de Dados: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Processamento de Dados: FALHOU - {e}")
        return False

def test_preprocessing():
    """Testa o pré-processamento"""
    print("\n" + "="*60)
    print("TESTE 3: Pré-processamento")
    print("="*60)
    
    try:
        # Executar pré-processamento
        print("Executando preprocessamento_ia.py...")
        os.system("python tools/preprocessamento_ia.py")
        
        # Verificar arquivos criados
        files_to_check = [
            "data/dataset_preprocessado.csv",
            "model/scaler.joblib",
            "model/encoder.joblib",
            "model/label_mapping.json"
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                print(f"✓ {file_path} criado")
            else:
                print(f"❌ {file_path} não encontrado")
                return False
        
        # Verificar dados preprocessados
        df = pd.read_csv("data/dataset_preprocessado.csv")
        print(f"✓ Dataset preprocessado: {df.shape}")
        
        print("✅ Pré-processamento: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Pré-processamento: FALHOU - {e}")
        return False

def test_model_training():
    """Testa o treinamento do modelo"""
    print("\n" + "="*60)
    print("TESTE 4: Treinamento do Modelo")
    print("="*60)
    
    try:
        # Executar treinamento
        print("Executando treinamento do modelo...")
        os.system("python model/main_train_model.py")
        
        # Verificar se modelo foi criado
        if os.path.exists("model/ddos_model.pkl"):
            print("✓ Modelo ddos_model.pkl criado")
        else:
            print("❌ Modelo não foi criado")
            return False
        
        if os.path.exists("model/model_metadata.json"):
            print("✓ Metadados do modelo criados")
        else:
            print("❌ Metadados do modelo não foram criados")
        
        print("✅ Treinamento do Modelo: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Treinamento do Modelo: FALHOU - {e}")
        return False

def test_inference():
    """Testa a inferência"""
    print("\n" + "="*60)
    print("TESTE 5: Inferência")
    print("="*60)
    
    try:
        # Usar um arquivo pequeno para teste
        test_file = "data/pcap_convertido.csv"
        
        # Executar inferência
        print("Executando inferência...")
        cmd = f"python tools/inferencia_ddos.py {test_file} data/teste_inferencia.csv"
        os.system(cmd)
        
        # Verificar resultado
        if os.path.exists("data/teste_inferencia.csv"):
            df = pd.read_csv("data/teste_inferencia.csv")
            print(f"✓ Inferência concluída: {df.shape}")
            
            if 'Predito' in df.columns:
                print(f"✓ Coluna 'Predito' encontrada")
                print(f"✓ Distribuição das predições:")
                print(df['Predito'].value_counts())
            else:
                print("❌ Coluna 'Predito' não encontrada")
                return False
        else:
            print("❌ Arquivo de resultado da inferência não foi criado")
            return False
        
        print("✅ Inferência: PASSOU")
        return True
        
    except Exception as e:
        print(f"❌ Inferência: FALHOU - {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DO PIPELINE CORRIGIDO")
    print("="*60)
    
    tests = [
        test_feature_engineering,
        test_data_processing, 
        test_preprocessing,
        test_model_training,
        test_inference
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    # Resumo final
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    test_names = [
        "Feature Engineering",
        "Processamento de Dados", 
        "Pré-processamento",
        "Treinamento do Modelo",
        "Inferência"
    ]
    
    passed = 0
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{i+1}. {name:25} | {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(tests)} testes passaram")
    
    if passed == len(tests):
        print("\n🎉 TODOS OS TESTES PASSARAM! Pipeline corrigido com sucesso!")
    else:
        print(f"\n⚠️  {len(tests)-passed} teste(s) falharam. Verifique os erros acima.")

if __name__ == "__main__":
    main()
