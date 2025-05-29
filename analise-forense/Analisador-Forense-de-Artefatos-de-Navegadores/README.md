# 🔎 Analisador Forense de Artefatos de Navegador (Chromium)

## 💡 Objetivo

Extrair automaticamente **histórico de navegação**, **downloads** e **cookies** dos navegadores baseados em Chromium (Chrome, Edge, Brave etc.) para fins de **investigação forense digital**.

## 📁 Artefatos Coletados

- Histórico de Navegação (`History`)
- Arquivos Baixados (`History`)
- Cookies (`Cookies`)

## ⚙️ Requisitos

- Python 3.8+
- Acesso ao diretório de perfil do navegador (Linux/WSL)

## 🛠️ Como usar

```bash
python3 analisa_navegador.py
