import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE

# Configurações de caminhos
DATA_PATH = os.path.join("data", "dataset_preprocessado.csv")
MODEL_PATH = os.path.join("model", "ddos_model.pkl")
SCALER_PATH = os.path.join("model", "scaler.joblib")

def load_dataset():
    """Carrega o dataset já pré-processado."""
    print("[INFO] Carregando dataset pré-processado...")
    df = pd.read_csv(DATA_PATH)
    return df

def train_model(df):
    """Treina o modelo com validação e otimização."""
    # Selecionar features (agora incluindo as novas)
    features = [
        'flow_duration', 'packet_rate', 'byte_rate', 
        'src_ip_count', 'dst_ip_count', 'tcp_syn',
        'length', 'dst_port', 'protocol'
    ]
    
    # Verificar se as features existem no DataFrame
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        raise ValueError(f"Features faltantes: {missing_features}")
    
    X = df[features]
    y = df["Label_encoded"]

    # Dividir treino/teste (estratificado)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    # Pipeline com normalização e modelo
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestClassifier(random_state=42, class_weight='balanced'))
    ])

    # Hiperparâmetros para otimização
    params = {
        'model__n_estimators': [100, 200],
        'model__max_depth': [10, 20, None],
        'model__min_samples_split': [2, 5],
        'model__min_samples_leaf': [1, 2]
    }

    # Busca de melhores parâmetros
    print("[INFO] Otimizando hiperparâmetros...")
    grid_search = GridSearchCV(
        pipeline, 
        params, 
        cv=5, 
        scoring='f1_weighted',
        verbose=2,
        n_jobs=-1
    )
    grid_search.fit(X_train, y_train)

    # Melhor modelo
    best_model = grid_search.best_estimator_
    print(f"Melhores parâmetros: {grid_search.best_params_}")

    # Avaliação
    y_pred = best_model.predict(X_test)
    print("\n[RELATÓRIO DE CLASSIFICAÇÃO]")
    print(classification_report(y_test, y_pred, target_names=df["Label"].unique()))
    print("\n[MATRIZ DE CONFUSÃO]")
    print(confusion_matrix(y_test, y_pred))

    # Salvar modelo
    os.makedirs("model", exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    print(f"[✅] Modelo salvo em {MODEL_PATH}")

if __name__ == "__main__":
    df = load_dataset()
    train_model(df)