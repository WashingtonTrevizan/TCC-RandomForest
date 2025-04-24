# Projeto DDoS Detector com IA

Este projeto simula o tráfego de rede e utiliza um modelo de Inteligência Artificial treinado para detectar ataques DDoS em tempo real. Você pode visualizar os resultados no terminal ou em uma interface gráfica com botão de iniciar/parar e gráfico em tempo real.

---

## 📁 Estrutura do Projeto

```
ddos-detector/
├── model/
│   ├── train_model.py         # Script de treino do modelo
│   └── model.pkl              # Modelo IA treinado
├── live_capture/
│   ├── simulate_live_traffic.py  # Simulação + gráfico (terminal)
├── logs/
│   └── detections.log         # Arquivo de log de detecção
├── ddos_gui.py                # Interface com botão iniciar/parar
├── requirements.txt           # Dependências do projeto
├── explicacao_projeto.txt     # Explicação técnica do sistema
```

---

## 🧠 Como Funciona

1. **Modelo de IA (Random Forest)**
   - Treinado com pacotes simulados (tamanho, protocolo e IPs convertidos)
   - Classifica tráfego como "BENIGN" ou tipo de ataque DDoS

2. **Simulador de Tráfego**
   - Gera pacotes falsos com:
     - `length` (tamanho)
     - `protocol` (1 = TCP, 2 = UDP)
     - `src_ip`, `dst_ip` (simulados e convertidos em números)

3. **Log de Detecção**
   - Quando um ataque é detectado, os dados são gravados em `logs/detections.log`

4. **Interface Gráfica (GUI)**
   - Exibe botão "Iniciar/Parar"
   - Mostra gráfico de barras em tempo real (BENIGN vs ATAQUE)

---

## 🚀 Como Rodar o Projeto

### 1. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 2. (Opcional) Treinar o modelo
```bash
python model/train_model.py
```

### 3. Rodar a simulação no terminal com gráfico
```bash
python live_capture/simulate_live_traffic.py
```

### 4. Rodar a interface gráfica com botão e gráfico
```bash
python ddos_gui.py
```

---

## 📄 Logs

- Os resultados são salvos em:
  ```
  logs/detections.log
  ```

Exemplo:
```
[2025-04-08 22:04:05] DDoS-UDP | SRC: 192.168.1.14 DST: 192.168.1.2 LEN: 1500 PROTO: 2
```

---

## ✅ Requisitos (requirements.txt)
```txt
scikit-learn
pandas
pyshark
joblib
numpy
matplotlib
pyqt5
colorama
```

---
