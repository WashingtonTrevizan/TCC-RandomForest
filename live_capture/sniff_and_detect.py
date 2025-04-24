import pyshark
import joblib
import pandas as pd
import os
from datetime import datetime
from colorama import init, Fore
import sys

init(autoreset=True)

MODEL_PATH = os.path.join("..", "model", "model.pkl")
LOG_FILE = os.path.join("..", "logs", "detections.log")

# Carrega modelo treinado
def load_model():
    print("[INFO] Carregando modelo IA...")
    return joblib.load(MODEL_PATH)

# Extrai features simples do pacote
def extract_features(packet):
    try:
        return {
            'length': int(packet.length),
            'protocol': 2 if 'UDP' in packet else 1  # protocolo simulado
        }
    except Exception:
        return None

# Escreve alerta no log
def log_detection(data, prediction):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {prediction} | {data}\n")

# Monitoramento de pacotes a partir de um arquivo
def monitor_from_file(file_path):
    model = load_model()
    print(f"[INFO] Processando pacotes do arquivo: {file_path}\n")

    try:
        capture = pyshark.FileCapture(file_path)
        for packet in capture:
            features = extract_features(packet)
            if features:
                df = pd.DataFrame([features])
                prediction = model.predict(df)[0]

                if prediction != "BENIGN":
                    print(Fore.RED + f"[ALERTA] ATAQUE DETECTADO: {prediction} - Dados: {features}")
                    log_detection(features, prediction)
                else:
                    print(Fore.GREEN + f"[OK] Tráfego normal - Len: {features['length']}")
    except Exception as e:
        print(Fore.RED + f"[ERRO] Falha ao processar arquivo: {e}")

# Entrada principal
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(Fore.YELLOW + "Uso: python sniff_and_detect.py <caminho_para_arquivo_pcap>")
    else:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            monitor_from_file(file_path)
        else:
            print(Fore.RED + f"[ERRO] Arquivo não encontrado: {file_path}")