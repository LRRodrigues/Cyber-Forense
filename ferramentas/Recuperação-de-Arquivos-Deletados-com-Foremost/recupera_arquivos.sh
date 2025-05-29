#!/bin/bash

# Verifica se o foremost está instalado
if ! command -v foremost &> /dev/null; then
    echo "[!] Foremost não encontrado. Instalando..."
    sudo apt update && sudo apt install foremost -y
fi

echo "=========================================="
echo " 🔍 Recuperação de Arquivos com Foremost "
echo "=========================================="

read -p "Informe o caminho da imagem ou disco (/dev/sdX ou arquivo .dd/.img): " DISCO
read -p "Informe o diretório de saída para os arquivos recuperados: " SAIDA

if [ ! -f "$DISCO" ] && [ ! -b "$DISCO" ]; then
    echo "[!] Caminho inválido: $DISCO"
    exit 1
fi

mkdir -p "$SAIDA"

echo "[+] Iniciando análise com foremost..."
foremost -i "$DISCO" -o "$SAIDA" -v

echo "=========================================="
echo "✅ Recuperação finalizada!"
echo "📁 Arquivos salvos em: $SAIDA"
echo "=========================================="
