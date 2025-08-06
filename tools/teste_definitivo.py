"""
🧪 TESTE DEFINITIVO COM TRÁFEGO REALISTA
=======================================

Testa o modelo treinado com os dados de teste que têm
distribuição aleatória e padrões realistas.

Este é o teste final que valida se o sistema consegue
detectar ataques DDoS em cenários reais!
"""

import pandas as pd
import numpy as np
import joblib
import os
from tqdm import tqdm
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import json

def convert_test_data_to_features():
    """Converte dados de teste para formato compatível com o modelo"""
    print("🔄 CONVERTENDO DADOS DE TESTE PARA FEATURES")
    print("=" * 60)
    
    # Carregar dados de teste brutos
    test_raw_path = "data/raw/test_traffic_realistic.csv"
    
    if not os.path.exists(test_raw_path):
        print(f"❌ Arquivo de teste não encontrado: {test_raw_path}")
        return None
    
    df = pd.read_csv(test_raw_path)
    print(f"📊 Dados de teste carregados: {df.shape}")
    
    # Converter para features compatíveis
    print("⚙️ Calculando features...")
    
    with tqdm(total=5, desc="Processando features", unit="etapa") as pbar:
        # Flow duration já existe
        df['flow_duration'] = df['flow_duration']
        pbar.update(1)
        
        # Calcular rates
        df['packet_rate'] = df['packet_count'] / (df['flow_duration'] + 0.001)
        df['byte_rate'] = df['byte_count'] / (df['flow_duration'] + 0.001)
        pbar.update(1)
        
        # IP counts (simplificado para dados sintéticos)
        df['src_ip_count'] = 1
        df['dst_ip_count'] = 1
        pbar.update(1)
        
        # TCP SYN
        df['tcp_syn'] = (df['tcp_flags'].str.contains('SYN', na=False)).astype(int)
        pbar.update(1)
        
        # Selecionar colunas necessárias
        required_cols = [
            'flow_duration', 'packet_rate', 'byte_rate',
            'src_ip_count', 'dst_ip_count', 'tcp_syn',
            'length', 'dst_port', 'protocol', 'Label'
        ]
        
        df_features = df[required_cols].copy()
        pbar.update(1)
    
    # Salvar dados convertidos
    output_path = "data/processed/test_features_realistic.csv"
    os.makedirs("data/processed", exist_ok=True)
    df_features.to_csv(output_path, index=False)
    
    print(f"✅ Features de teste salvas: {output_path}")
    print(f"📊 Shape final: {df_features.shape}")
    
    return df_features

def test_model_with_realistic_data():
    """Testa modelo com dados realistas"""
    print("\n🎯 TESTE DO MODELO COM DADOS REALISTAS")
    print("=" * 60)
    
    # Converter dados de teste
    df_test = convert_test_data_to_features()
    if df_test is None:
        return False
    
    print(f"\n📊 DISTRIBUIÇÃO DOS DADOS DE TESTE:")
    label_counts = df_test['Label'].value_counts()
    for label, count in label_counts.items():
        percentage = (count / len(df_test)) * 100
        print(f"  {label}: {count:,} ({percentage:.1f}%)")
    
    # Carregar modelo e preprocessadores
    print(f"\n🔄 Carregando modelo treinado...")
    
    try:
        modelo = joblib.load("data/models/ddos_model_realista.pkl")
        scaler = joblib.load("data/models/scaler_realista.joblib")
        
        with open("data/models/label_mapping_realista.json", "r") as f:
            label_mapping = json.load(f)
        
        print("✅ Modelo e preprocessadores carregados")
        
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        return False
    
    # Preparar dados
    REQUIRED_FEATURES = [
        'flow_duration', 'packet_rate', 'byte_rate', 
        'src_ip_count', 'dst_ip_count', 'tcp_syn',
        'length', 'dst_port', 'protocol'
    ]
    
    X_test = df_test[REQUIRED_FEATURES]
    y_test_labels = df_test['Label']
    
    # Mapear labels para números
    y_test = y_test_labels.map(label_mapping)
    
    print(f"\n🔄 Fazendo predições...")
    
    with tqdm(total=3, desc="Testando modelo", unit="etapa") as pbar:
        # Normalizar
        X_test_scaled = scaler.transform(X_test)
        pbar.update(1)
        
        # Predizer
        y_pred = modelo.predict(X_test_scaled)
        pbar.update(1)
        
        # Probabilidades
        y_proba = modelo.predict_proba(X_test_scaled)
        pbar.update(1)
    
    # Calcular métricas
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n📈 RESULTADOS DO TESTE REALISTA:")
    print("=" * 60)
    print(f"🎯 Acurácia Geral: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Relatório detalhado
    reverse_mapping = {v: k for k, v in label_mapping.items()}
    target_names = [reverse_mapping[i] for i in sorted(reverse_mapping.keys()) if i in y_test.unique()]
    
    print(f"\n📋 RELATÓRIO DE CLASSIFICAÇÃO:")
    print(classification_report(y_test, y_pred, target_names=target_names))
    
    print(f"\n🎭 MATRIZ DE CONFUSÃO:")
    cm = confusion_matrix(y_test, y_pred)
    print(cm)
    
    # Análise por classe
    print(f"\n🔍 ANÁLISE POR CLASSE:")
    print("-" * 50)
    
    for i, label_name in enumerate(target_names):
        if i in y_test.values:
            # Calcular métricas para esta classe
            mask = (y_test == i)
            correct = (y_pred[mask] == i).sum()
            total = mask.sum()
            class_accuracy = (correct / total) if total > 0 else 0
            
            # Confiança média para esta classe
            if len(y_proba) > 0:
                class_confidence = y_proba[mask, i].mean() if total > 0 else 0
            else:
                class_confidence = 0
            
            status = "✅" if class_accuracy >= 0.9 else "⚠️" if class_accuracy >= 0.7 else "❌"
            print(f"{status} {label_name:12} | {correct:5}/{total:5} ({class_accuracy*100:5.1f}%) | Conf: {class_confidence:.3f}")
    
    # Análise de erros
    print(f"\n🚨 ANÁLISE DE ERROS:")
    errors = (y_test != y_pred)
    if errors.sum() > 0:
        print(f"Total de erros: {errors.sum():,} de {len(y_test):,} ({errors.sum()/len(y_test)*100:.2f}%)")
        
        # Mostrar alguns exemplos de erro
        error_examples = df_test[errors].head(10)
        if len(error_examples) > 0:
            print(f"\nExemplos de classificação incorreta:")
            for idx, row in error_examples.iterrows():
                real_label = row['Label']
                pred_label = reverse_mapping.get(y_pred[idx], f"Unknown_{y_pred[idx]}")
                print(f"  Real: {real_label:12} | Predito: {pred_label:12}")
    else:
        print("🎉 Nenhum erro de classificação!")
    
    # Análise de confiança
    print(f"\n📊 ANÁLISE DE CONFIANÇA:")
    max_proba = y_proba.max(axis=1)
    avg_confidence = max_proba.mean()
    low_confidence_count = (max_proba < 0.8).sum()
    
    print(f"Confiança média: {avg_confidence:.3f}")
    print(f"Predições com baixa confiança (<0.8): {low_confidence_count:,} ({low_confidence_count/len(max_proba)*100:.1f}%)")
    
    # Salvar resultados detalhados
    results_df = df_test.copy()
    results_df['Predição_Numérica'] = y_pred
    results_df['Predição'] = [reverse_mapping.get(pred, f"Unknown_{pred}") for pred in y_pred]
    results_df['Confiança'] = max_proba
    results_df['Correto'] = (y_test == y_pred)
    
    output_path = "data/processed/teste_modelo_trafego_realista.csv"
    results_df.to_csv(output_path, index=False)
    
    print(f"\n💾 Resultados detalhados salvos: {output_path}")
    
    # Resumo final
    print(f"\n" + "=" * 60)
    print(f"🎯 RESUMO DO TESTE REALISTA")
    print(f"=" * 60)
    print(f"📊 Amostras testadas: {len(df_test):,}")
    print(f"🎯 Acurácia: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"📈 Confiança média: {avg_confidence:.3f}")
    print(f"❌ Taxa de erro: {(1-accuracy)*100:.2f}%")
    
    if accuracy >= 0.95:
        print(f"🏆 EXCELENTE! Modelo detecta ataques com alta precisão")
    elif accuracy >= 0.85:
        print(f"✅ BOM! Modelo funciona bem para detecção")
    elif accuracy >= 0.70:
        print(f"⚠️ RAZOÁVEL! Modelo precisa de melhorias")
    else:
        print(f"❌ RUIM! Modelo não está funcionando adequadamente")
    
    return True

if __name__ == "__main__":
    print("🧪 INICIANDO TESTE DEFINITIVO DO SISTEMA DDoS")
    print("=" * 80)
    
    success = test_model_with_realistic_data()
    
    if success:
        print(f"\n🎉 TESTE COMPLETO REALIZADO COM SUCESSO!")
        print(f"📁 Verifique os resultados detalhados em data/processed/")
    else:
        print(f"\n❌ FALHA NO TESTE!")
        print(f"🔧 Verifique os erros e tente novamente")
