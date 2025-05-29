#!/bin/bash

# Script para capturar memória (Linux) e analisar com Volatility 3
# Requer Volatility 3 instalado e LiME compilado

echo "======================================"
echo "🧠 Captura & Análise de RAM com Volatility 3"
echo "======================================"

read -p "Digite o nome do arquivo de dump (ex: memoria.lime): " NOME_DUMP
read -p "Deseja capturar RAM agora com LiME? (s/n): " CAPTURAR

if [[ "$CAPTURAR" == "s" ]]; then
    if [[ ! -f lime.ko ]]; then
        echo "[!] Módulo LiME não encontrado. Compile-o antes de continuar."
        echo "    Dica: https://github.com/504ensicsLabs/LiME"
        exit 1
    fi

    echo "[+] Carregando módulo LiME para captura..."
    sudo insmod lime.ko "path=/mnt/$NOME_DUMP format=lime"
    echo "[✓] Captura iniciada. Aguarde alguns segundos..."
    sleep 15
    sudo rmmod lime
    echo "[✓] Captura finalizada e salva em /mnt/$NOME_DUMP"
else
    read -p "Informe o caminho completo do dump existente: " NOME_DUMP
fi

echo "[+] Analisando memória com Volatility 3..."
mkdir -p analise_resultados

vol3() {
    python3 vol.py -f "$1" --output-file "analise_resultados/$2.txt" $3
    echo "[✓] $2.txt gerado"
}

# Ajuste abaixo: coloque o perfil se necessário
vol3 "$NOME_DUMP" "processos" linux.pslist
vol3 "$NOME_DUMP" "conexoes" linux.netstat
vol3 "$NOME_DUMP" "malware_check" linux.malfind
vol3 "$NOME_DUMP" "sockets" linux.lsof
vol3 "$NOME_DUMP" "memmap" linux.memmap

echo "======================================"
echo "✅ Análises completas! Veja a pasta 'analise_resultados/'"
echo "======================================"
