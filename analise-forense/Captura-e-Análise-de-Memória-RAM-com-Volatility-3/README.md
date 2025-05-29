# 🧠 Captura e Análise de Memória com Volatility 3

## 🎯 Objetivo

Automatizar a **captura da memória RAM** (Linux) com **LiME** e análise forense com **Volatility 3**. Útil para identificar:
- Processos suspeitos
- Malwares em execução
- Conexões de rede
- Arquivos abertos
- Atividades persistentes na RAM

## ⚙️ Requisitos

- Linux (Ubuntu/Debian preferencialmente)
- `LiME` compilado (`lime.ko`)
- Python 3.8+
- Volatility 3 instalado
  - Instalação:  
    ```bash
    git clone https://github.com/volatilityfoundation/volatility3
    cd volatility3
    pip3 install -r requirements.txt
    ```

## 📦 Uso

```bash
chmod +x analisa_memoria.sh
sudo ./analisa_memoria.sh
