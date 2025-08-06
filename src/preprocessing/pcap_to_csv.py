import pyshark
import csv
import os
import threading
import time
import sys
from collections import defaultdict

PCAP_PATH = "data/captura.pcap"
CSV_PATH = "data/pcap_convertido.csv"
running = True

# Animação de carregamento
def spinner():
    while running:
        for c in "|/-\\":
            sys.stdout.write(f"\r[INFO] Convertendo pacotes... {c}")
            sys.stdout.flush()
            time.sleep(0.1)

def convert_pcap_to_csv():
    global running
    print(f"[INFO] Convertendo {PCAP_PATH} para {CSV_PATH}...")

    # Iniciar spinner em paralelo
    t = threading.Thread(target=spinner)
    t.start()

    # Contadores para features adicionais
    flow_counts = defaultdict(int)
    cap = pyshark.FileCapture(
        PCAP_PATH,
        only_summaries=False,
        use_json=True,  # Melhora performance
        include_raw=False,
        disable_protocol="http"  # Ignora HTTP para velocidade
    )

    with open(CSV_PATH, 'w', newline='') as csvfile:
        # Fields básicos (sem features calculadas - isso será feito depois)
        fieldnames = [
            'timestamp', 'src_ip', 'dst_ip', 'src_port', 'dst_port',
            'protocol', 'length', 'tcp_flags'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for pkt in cap:
            try:
                # Flags TCP (SYN, ACK, RST, etc.)
                tcp_flags = 0
                if hasattr(pkt, 'tcp'):
                    tcp_flags = int(pkt.tcp.flags, 16)  # Converte flags hex para int

                # Escreve no CSV (apenas dados brutos)
                writer.writerow({
                    'timestamp': pkt.sniff_time,
                    'src_ip': pkt.ip.src,
                    'dst_ip': pkt.ip.dst,
                    'src_port': pkt[pkt.transport_layer].srcport if hasattr(pkt, 'transport_layer') else 0,
                    'dst_port': pkt[pkt.transport_layer].dstport if hasattr(pkt, 'transport_layer') else 0,
                    'protocol': pkt.transport_layer,
                    'length': int(pkt.length),
                    'tcp_flags': tcp_flags
                })

            except AttributeError:
                continue

    running = False
    t.join()
    print("\n[✅] Conversão concluída! CSV salvo em:", CSV_PATH)

if __name__ == "__main__":
    convert_pcap_to_csv()