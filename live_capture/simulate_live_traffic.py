import time
import random
import pandas as pd
import joblib
import os
from datetime import datetime
from colorama import init, Fore
import matplotlib.pyplot as plt
import socket
import struct


init(autoreset=True)

MODEL_PATH = os.path.join("model", "model.pkl")
LOG_PATH = os.path.join("logs", "detections.log")

# Contadores
attack_count = 0
benign_count = 0


def ip_to_int(ip):
    return struct.unpack("!I", socket.inet_aton(ip))[0]


# Setup matplotlib interativo
plt.ion()
fig, ax = plt.subplots()
bars = ax.bar(["BENIGN", "ATAQUE"], [0, 0], color=["green", "red"])
ax.set_ylim(0, 20)
ax.set_ylabel("Quantidade de Pacotes")
ax.set_title("Detecção em Tempo Real")

def update_chart():
    bars[0].set_height(benign_count)
    bars[1].set_height(attack_count)
    ax.set_ylim(0, max(20, benign_count + attack_count + 5))
    plt.draw()
    plt.pause(0.01)

# Simular pacotes
def generate_packet():
    length = random.choice([60, 64, 500, 1024, 1500, 2000])
    protocol = random.choice([1, 2])
    src_ip = f"192.168.1.{random.randint(2, 254)}"
    dst_ip = f"192.168.1.{random.randint(1, 5)}"

    return {
        "length": length,
        "protocol": protocol,
        "src_ip_num": ip_to_int(src_ip),
        "dst_ip_num": ip_to_int(dst_ip),
        "src_ip": src_ip,
        "dst_ip": dst_ip,
    }

# Carregar modelo
def load_model():
    print("[INFO] Carregando modelo IA simulado...")
    return joblib.load(MODEL_PATH)

# Gravar log
def log_detection(data, prediction):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {prediction} | {data}\n")

# Simulador de tráfego com gráfico
def simulate_monitor():
    global attack_count, benign_count
    model = load_model()
    print("[INFO] Iniciando simulação com gráfico...\n")

    try:
        while True:
            packet = generate_packet()  # <- estava com nome incorreto antes
            df = pd.DataFrame([{
                "length": packet["length"],
                "protocol": packet["protocol"],
                "src_ip_num": packet["src_ip_num"],
                "dst_ip_num": packet["dst_ip_num"]
            }])

            prediction = model.predict(df)[0]

            if prediction != "BENIGN":
                attack_count += 1
                print(Fore.RED + f"[ALERTA] Ataque Detectado: {prediction} - {packet}")
                log_detection(packet, prediction)
            else:
                benign_count += 1
                print(Fore.GREEN + f"[OK] Tráfego normal - {packet}")

            update_chart()
            time.sleep(1)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[INFO] Simulação encerrada pelo usuário.")

# Atualização do log:
def log_detection(data, prediction):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as f:
        f.write(f"[{timestamp}] {prediction} | SRC: {data['src_ip']} DST: {data['dst_ip']} LEN: {data['length']} PROTO: {data['protocol']}\n")
