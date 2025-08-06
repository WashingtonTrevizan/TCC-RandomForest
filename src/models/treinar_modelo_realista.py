"""
Treinamento de modelo com dataset realista - evita overfitting
"""
import pandas as pd
import numpy as np
import joblib
import os
import sys
import time
from tqdm import tqdm
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

def treinar_modelo_realista():
    """Treina modelo com dataset realista"""
    print("🧠 TREINAMENTO DE MODELO REALISTA (ANTI-OVERFITTING)")
    print("="*70)
    
    # Carregar dataset realista preprocessado
    DATA_PATH = "data/processed/dataset_preprocessado_realista.csv"
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Dataset não encontrado: {DATA_PATH}")
        print("Execute primeiro: python criar_dataset_realista.py")
        print("Em seguida: python preprocessamento_realista.py")
        return False
    
    df = pd.read_csv(DATA_PATH)
    print(f"[INFO] Dataset carregado: {df.shape}")
    
    print(f"[INFO] Distribuição das classes:")
    print(df["Label"].value_counts())
    
    # Tratar classes com poucas amostras
    print(f"[INFO] Verificando classes com poucas amostras...")
    class_counts = df["Label_encoded"].value_counts()
    small_classes = class_counts[class_counts < 2]
    
    if len(small_classes) > 0:
        print(f"[WARN] Classes com < 2 amostras encontradas: {small_classes.to_dict()}")
        print(f"[INFO] Removendo amostras de classes pequenas...")
        # Remover classes com menos de 2 amostras
        df = df[~df["Label_encoded"].isin(small_classes.index)]
        print(f"[INFO] Dataset após limpeza: {df.shape}")
    
    # Features e labels
    REQUIRED_FEATURES = [
        'flow_duration', 'packet_rate', 'byte_rate', 
        'src_ip_count', 'dst_ip_count', 'tcp_syn',
        'length', 'dst_port', 'protocol'
    ]
    
    X = df[REQUIRED_FEATURES]
    y = df["Label_encoded"]
    
    # Divisão estratificada
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    print(f"[INFO] Treino: {X_train.shape[0]} | Teste: {X_test.shape[0]}")
    
    # Modelo com parâmetros conservadores para evitar overfitting
    print("[INFO] Configurando Random Forest com parâmetros anti-overfitting...")
    
    rf = RandomForestClassifier(
        n_estimators=50,           # Menos árvores
        max_depth=8,               # Profundidade limitada
        min_samples_split=20,      # Mais amostras para split
        min_samples_leaf=10,       # Mais amostras por folha
        max_features='sqrt',       # Menos features por árvore
        class_weight='balanced',   # Balanceamento
        random_state=42,
        n_jobs=-1
    )
    
    # Validação cruzada antes do treino final
    print("[INFO] Executando validação cruzada (5-fold)...")
    
    # Barra de progresso para validação cruzada
    cv_scores = []
    with tqdm(total=5, desc="🔄 Validação Cruzada", unit="fold") as pbar:
        for i in range(5):
            # Simular cada fold da validação cruzada
            scores = cross_val_score(rf, X_train, y_train, cv=5, scoring='f1_macro')
            if i == 0:  # Só calcular uma vez
                cv_scores = scores
            time.sleep(0.5)  # Pequena pausa para visualizar o progresso
            pbar.update(1)
    
    print(f"[INFO] CV F1-macro: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    if cv_scores.mean() > 0.98:
        print("⚠️  ATENÇÃO: Score muito alto na validação cruzada - possível overfitting!")
    
    # Treino final com barra de progresso
    print("[INFO] Treinando modelo final...")
    
    # Configurar barra de progresso para o treinamento
    with tqdm(total=100, desc="🌳 Treinando Random Forest", unit="%") as pbar:
        # Simular progresso do treinamento
        for i in range(0, 101, 20):
            if i == 0:
                pbar.set_description("🌱 Inicializando...")
                time.sleep(0.3)
            elif i == 20:
                pbar.set_description("🌿 Construindo árvores...")
                rf.fit(X_train, y_train)  # Treino real aqui
                time.sleep(0.5)
            elif i == 40:
                pbar.set_description("🌳 Otimizando splits...")
                time.sleep(0.3)
            elif i == 60:
                pbar.set_description("🍃 Refinando folhas...")
                time.sleep(0.3)
            elif i == 80:
                pbar.set_description("🎯 Finalizando modelo...")
                time.sleep(0.3)
            elif i == 100:
                pbar.set_description("✅ Treinamento concluído!")
                time.sleep(0.2)
            
            pbar.update(20)
    
    # Avaliação com barra de progresso
    print("\n[INFO] Avaliando modelo...")
    
    with tqdm(total=4, desc="🧮 Calculando métricas", unit="etapa") as pbar:
        pbar.set_description("📊 Predições treino...")
        y_pred_train = rf.predict(X_train)
        pbar.update(1)
        
        pbar.set_description("📊 Predições teste...")
        y_pred_test = rf.predict(X_test)
        pbar.update(1)
        
        pbar.set_description("📈 Acurácia treino...")
        train_acc = accuracy_score(y_train, y_pred_train)
        pbar.update(1)
        
        pbar.set_description("📈 Acurácia teste...")
        test_acc = accuracy_score(y_test, y_pred_test)
        pbar.update(1)
    
    print(f"[INFO] Acurácia TREINO: {train_acc:.4f}")
    print(f"[INFO] Acurácia TESTE:  {test_acc:.4f}")
    print(f"[INFO] Diferença: {abs(train_acc - test_acc):.4f}")
    
    if abs(train_acc - test_acc) > 0.05:
        print("⚠️  ATENÇÃO: Grande diferença entre treino e teste - possível overfitting!")
    elif test_acc > 0.98:
        print("⚠️  ATENÇÃO: Acurácia muito alta - dados podem estar muito simples!")
    else:
        print("✅ Diferença aceitável entre treino e teste")
    
    # Relatório detalhado
    print("\n" + "="*60)
    print("RELATÓRIO DE CLASSIFICAÇÃO (TESTE)")
    print("="*60)
    
    # Mapear labels únicos no teste
    unique_labels = sorted(y_test.unique())
    label_names = {0: 'Benign', 1: 'UDP-Flood', 2: 'SYN-Flood', 3: 'HTTP-Flood', 4: 'DDoS-Other'}
    labels = [label_names[i] for i in unique_labels if i in label_names]
    
    print(classification_report(y_test, y_pred_test, target_names=labels))
    
    print("\nMATRIZ DE CONFUSÃO:")
    cm = confusion_matrix(y_test, y_pred_test)
    print(cm)
    
    # Feature importance
    print(f"\nIMPORTÂNCIA DAS FEATURES:")
    feature_importance = pd.DataFrame({
        'feature': REQUIRED_FEATURES,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    for _, row in feature_importance.iterrows():
        print(f"{row['feature']:20} | {row['importance']:.4f}")
    
    # Salvar modelo com progresso
    print(f"\n[INFO] Salvando modelo realista...")
    os.makedirs("model", exist_ok=True)
    
    with tqdm(total=3, desc="💾 Salvando arquivos", unit="arquivo") as pbar:
        pbar.set_description("💾 Salvando modelo...")
        joblib.dump(rf, "data/models/ddos_model_realista.pkl")
        pbar.update(1)
        
    # Metadados
        metadata = {
            "model_type": "RandomForestClassifier_Realista",
            "features": REQUIRED_FEATURES,
            "train_accuracy": float(train_acc),
            "test_accuracy": float(test_acc),
            "cv_score_mean": float(cv_scores.mean()),
            "cv_score_std": float(cv_scores.std()),
            "classes": labels,  # Usar labels atualizados
            "model_params": rf.get_params()
        }
        
        pbar.set_description("💾 Salvando metadados...")
        import json
        with open("data/models/model_realista_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        pbar.update(1)
        
        pbar.set_description("✅ Arquivos salvos!")
        time.sleep(0.5)
        pbar.update(1)
    
    print(f"[✅] Modelo realista salvo em: data/models/ddos_model_realista.pkl")
    
    # Diagnóstico final
    print(f"\n🎯 DIAGNÓSTICO FINAL:")
    if test_acc > 0.95 and abs(train_acc - test_acc) < 0.02:
        print("⚠️  MODELO AINDA PODE ESTAR OVERFITTING - dados muito simples")
        print("💡 Sugestão: Adicionar mais ruído ou usar dados reais")
    elif test_acc > 0.85:
        print("✅ MODELO COM PERFORMANCE BOA E REALISTA")
    else:
        print("⚠️  MODELO COM PERFORMANCE BAIXA - pode precisar de ajustes")
    
    return rf

if __name__ == "__main__":
    modelo = treinar_modelo_realista()
