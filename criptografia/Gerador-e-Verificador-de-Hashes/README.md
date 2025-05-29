# 🛡️ HashGuard — Monitoramento Forense de Integridade em Tempo Real

## 🔥 O que é

Script de monitoramento contínuo de arquivos com:

- Hashes com HMAC (proteção de integridade + origem)
- Timestamps assinados com chave privada (prova temporal)
- Log de eventos forenses automatizado em formato JSON

Ideal para manter a **cadeia de custódia digital** intacta durante análises forenses ou monitoramentos sensíveis.

## 🚀 Requisitos

- Python 3.7+
- Bibliotecas:
  - `watchdog`
  - `cryptography`

Instalar com:

```bash
pip install watchdog cryptography




🔑 Preparar chave privada RSA
bash
Copiar
Editar
openssl genpkey -algorithm RSA -out chave_privada.pem -pkeyopt rsa_keygen_bits:2048
