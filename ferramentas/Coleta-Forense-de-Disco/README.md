# Coleta Forense de Disco - Script Bash

## 🔎 Objetivo

Realizar uma **imagem forense bit-a-bit** de um dispositivo de armazenamento (como HDs, SSDs, pen drives), preservando a integridade com geração de **hashes MD5 e SHA1** e criação de um log formal da coleta.

## ⚙️ Requisitos

- Sistema Linux
- Acesso ROOT
- Ferramentas `dd`, `md5sum`, `sha1sum`

## 💻 Uso

```bash
sudo ./coleta_forense.sh /dev/sdX nome_do_caso
