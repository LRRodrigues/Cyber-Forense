#!/usr/bin/env python3
import os
import sys
import json
import exifread
import docx
import PyPDF2
from datetime import datetime

def extrair_exif(imagem):
    with open(imagem, 'rb') as f:
        tags = exifread.process_file(f, details=False)
    return {tag: str(value) for tag, value in tags.items()}

def extrair_pdf(pdf_path):
    metadados = {}
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        info = reader.metadata
        if info:
            for chave, valor in info.items():
                metadados[chave] = str(valor)
    return metadados

def extrair_docx(docx_path):
    doc = docx.Document(docx_path)
    props = doc.core_properties
    return {
        "autor": props.author,
        "título": props.title,
        "assunto": props.subject,
        "palavras-chave": props.keywords,
        "comentários": props.comments,
        "criado_em": str(props.created),
        "modificado_em": str(props.modified),
    }

def salvar_json(dados, saida_path):
    with open(saida_path, 'w') as f:
        json.dump(dados, f, indent=4)
    print(f"[+] Resultado salvo em: {saida_path}")

def processar_arquivo(path):
    if not os.path.exists(path):
        print(f"[-] Caminho inválido: {path}")
        return

    print(f"[+] Processando: {path}")
    ext = os.path.splitext(path)[-1].lower()
    resultado = {}

    try:
        if ext in ['.jpg', '.jpeg', '.tiff']:
            resultado = extrair_exif(path)
        elif ext == '.pdf':
            resultado = extrair_pdf(path)
        elif ext == '.docx':
            resultado = extrair_docx(path)
        else:
            print(f"[-] Tipo de arquivo não suportado: {ext}")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_saida = f"metadados_{os.path.basename(path)}_{timestamp}.json"
        salvar_json(resultado, nome_saida)

    except Exception as e:
        print(f"[-] Erro ao processar: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 meta_extractor.py <arquivo>")
        sys.exit(1)

    caminho = sys.argv[1]
    processar_arquivo(caminho)
