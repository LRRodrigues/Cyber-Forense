import os
import shutil
import sqlite3
import json
from datetime import datetime
from pathlib import Path

def timestamp_webkit_para_datetime(ts):
    if not ts:
        return "N/A"
    try:
        return str(datetime(1601, 1, 1) + timedelta(microseconds=int(ts)))
    except:
        return "Erro"

def extrair_historico(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 50")
        dados = cursor.fetchall()
        conn.close()

        historico = []
        for url, title, ts in dados:
            historico.append({
                "URL": url,
                "Título": title,
                "Último Acesso": timestamp_webkit_para_datetime(ts)
            })
        return historico
    except Exception as e:
        return [{"Erro": str(e)}]

def extrair_downloads(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT current_path, tab_url, start_time FROM downloads ORDER BY start_time DESC LIMIT 50")
        dados = cursor.fetchall()
        conn.close()

        downloads = []
        for path, tab, ts in dados:
            downloads.append({
                "Arquivo": path,
                "Fonte": tab,
                "Data": timestamp_webkit_para_datetime(ts)
            })
        return downloads
    except Exception as e:
        return [{"Erro": str(e)}]

def extrair_cookies(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT host_key, name, value, expires_utc FROM cookies LIMIT 50")
        dados = cursor.fetchall()
        conn.close()

        cookies = []
        for host, nome, valor, exp in dados:
            cookies.append({
                "Host": host,
                "Nome": nome,
                "Valor": valor,
                "Expira em": timestamp_webkit_para_datetime(exp)
            })
        return cookies
    except Exception as e:
        return [{"Erro": str(e)}]

def copiar_banco(origem, destino):
    try:
        shutil.copy2(origem, destino)
        return True
    except Exception as e:
        print(f"[Erro] Falha ao copiar: {e}")
        return False

def main():
    user = os.getenv("USER") or os.getenv("USERNAME")
    caminho = Path(f"/home/{user}/.config/google-chrome/Default")  # Modifique conforme o navegador e SO

    if not caminho.exists():
        print("[!] Caminho não encontrado. Verifique se o navegador é baseado em Chromium.")
        return

    os.makedirs("artefatos_extraidos", exist_ok=True)

    arquivos = {
        "Historico": "History",
        "Downloads": "History",
        "Cookies": "Cookies"
    }

    for nome, arquivo in arquivos.items():
        origem = caminho / arquivo
        destino = Path(f"./artefatos_extraidos/{nome}_{user}.db")
        if copiar_banco(origem, destino):
            print(f"[+] {nome} copiado com sucesso!")

    print("\n[*] Iniciando análise...")

    print("\n=== HISTÓRICO DE NAVEGAÇÃO ===")
    print(json.dumps(extrair_historico("artefatos_extraidos/Historico_" + user + ".db"), indent=2, ensure_ascii=False))

    print("\n=== DOWNLOADS ===")
    print(json.dumps(extrair_downloads("artefatos_extraidos/Downloads_" + user + ".db"), indent=2, ensure_ascii=False))

    print("\n=== COOKIES ===")
    print(json.dumps(extrair_cookies("artefatos_extraidos/Cookies_" + user + ".db"), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    from datetime import timedelta
    main()
