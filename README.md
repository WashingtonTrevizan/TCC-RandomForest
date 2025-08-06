# 🛡️ Sistema de Detecção DDoS com Random Forest

Sistema inteligente para detecção de ataques DDoS usando algoritmos de Machine Learning.

## 📁 Estrutura do Projeto (ORGANIZADA)

```
📦 SDN redes/
├── 🚀 main.py              # Script principal - COMECE AQUI
├── 🧪 run_tests.py         # Executa todos os testes
├── 🔧 deploy.py            # Deploy para produção
├── 📋 requirements.txt     # Dependências
│
├── 📂 src/                 # Código principal
│   ├── 🎯 app_inferencia.py       # Interface Streamlit
│   ├── 📂 core/                   # Módulos centrais
│   │   └── feature_engineering.py
│   ├── 📂 models/                 # Treinamento e inferência
│   │   ├── treinar_modelo_realista.py
│   │   └── inferencia_ddos.py
│   └── 📂 preprocessing/          # Processamento de dados
│       ├── preprocessamento_realista.py
│       └── pcap_to_csv.py
│
├── 📂 tests/               # Testes e validações
│   ├── 📂 unit/                   # Testes unitários
│   │   ├── validar_modelo.py
│   │   └── verificar_modelo.py
│   └── 📂 integration/            # Testes de integração
│       ├── testar_modelo_realista.py
│       ├── test_pipeline.py
│       └── gerar_trafego_teste.py
│
├── 📂 data/                # Dados organizados
│   ├── 📂 raw/                    # Dados brutos (PCAP)
│   ├── 📂 processed/              # Datasets processados
│   └── 📂 models/                 # Modelos e artefatos
│
├── 📂 experiments/         # Experimentos e versões antigas
├── 📂 docs/                # Documentação
├── 📂 live_capture/        # Captura ao vivo (legado)
└── 📂 logs/                # Logs do sistema
```

## 🚀 Como Usar

### Opção 1: Menu Interativo (RECOMENDADO)
```bash
python main.py
```

### Opção 2: Comandos Diretos

**1. Treinar modelo:**
```bash
python src/models/treinar_modelo_realista.py
```

**2. Fazer inferência:**
```bash
python src/app_inferencia.py
```

**3. Executar todos os testes:**
```bash
python run_tests.py
```

**4. Deploy para produção:**
```bash
python deploy.py
```

## 🎯 Funcionalidades

- ✅ **Detecção de 4 tipos de ataques:** UDP-Flood, SYN-Flood, HTTP-Flood, Tráfego Normal
- ✅ **Interface web:** Streamlit para uso fácil
- ✅ **Barras de progresso:** Feedback visual durante processamento
- ✅ **Pipeline completo:** PCAP → Processamento → Detecção
- ✅ **Testes automatizados:** Validação completa do sistema
- ✅ **Anti-overfitting:** Modelo realista com 99.4% acurácia

## 📊 Performance

- **Acurácia de Teste:** 99.4%
- **Validação Cruzada:** 92.6% F1-macro
- **Classes Detectadas:** 4 (Benign, UDP-Flood, SYN-Flood, HTTP-Flood)
- **Features Utilizadas:** 9 (flow_duration, packet_rate, byte_rate, etc.)

## 🛠️ Tecnologias

- **Python 3.12+**
- **scikit-learn** - Machine Learning
- **Streamlit** - Interface Web
- **pandas/numpy** - Processamento de dados
- **tqdm** - Barras de progresso
- **joblib** - Serialização de modelos

## 📚 Documentação

Consulte a pasta `docs/` para documentação detalhada:
- `docs/explicacao.txt` - Explicação técnica
- `docs/documentacao.txt` - Documentação completa
- `docs/README_CORRIGIDO.md` - Versão anterior

## 🧪 Testes

O sistema inclui uma suite completa de testes:

- **Testes Unitários:** Validação de componentes individuais
- **Testes de Integração:** Validação do pipeline completo
- **Testes de Performance:** Métricas e benchmarks

Execute: `python run_tests.py`

## 🚀 Status do Projeto

✅ **PRODUÇÃO** - Sistema funcional e testado
- Modelo treinado e validado
- Interface web operacional
- Testes automatizados passando
- Documentação completa

---

**Autor:** Seu Nome  
**Data:** 2025  
**Versão:** 2.0 (Organizada)
