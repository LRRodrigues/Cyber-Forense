# 🧠 MetaExtractor - Extrator Forense de Metadados

Ferramenta forense para extrair EXIF (imagens), metadados de PDF e DOCX, salvando em JSON legível e com marca temporal.

## 🔧 Suporta:
- `.jpg`, `.jpeg`, `.tiff` → EXIF
- `.pdf` → autor, criação, modificação, etc.
- `.docx` → autor, título, comentários, criação

## 📦 Instalação

```bash
pip install exifread python-docx PyPDF2
