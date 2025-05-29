#!/bin/bash

# Script para coleta forense de disco com hash MD5/SHA1
# Uso: sudo ./coleta_forense.sh /dev/sdX nome_do_caso

if [[ $EUID -ne 0 ]]; then
  echo "Execute como root!"
  exit 1
fi

DISPOSITIVO=$1
CASO=$2
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARQUIVO_IMAGEM="${CASO}_${TIMESTAMP}.dd"
ARQUIVO_LOG="${CASO}_${TIMESTAMP}.log"

if [[ -z "$DISPOSITIVO" || -z "$CASO" ]]; then
  echo "Uso: sudo $0 /dev/sdX nome_do_caso"
  exit 1
fi

echo "[*] Criando imagem forense de $DISPOSITIVO..."
dd if="$DISPOSITIVO" of="$ARQUIVO_IMAGEM" bs=4M status=progress conv=noerror,sync

echo "[*] Calculando hashes..."
HASH_MD5=$(md5sum "$ARQUIVO_IMAGEM" | awk '{print $1}')
HASH_SHA1=$(sha1sum "$ARQUIVO_IMAGEM" | awk '{print $1}')

echo "[*] Registrando log da coleta..."
cat <<EOF > "$ARQUIVO_LOG"
Caso: $CASO
Dispositivo: $DISPOSITIVO
Arquivo da Imagem: $ARQUIVO_IMAGEM
Data e Hora: $TIMESTAMP
Hash MD5: $HASH_MD5
Hash SHA1: $HASH_SHA1
EOF

echo "[+] Imagem criada: $ARQUIVO_IMAGEM"
echo "[+] Log gerado: $ARQUIVO_LOG"
