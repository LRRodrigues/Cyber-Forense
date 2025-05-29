import sqlite3
import os
import json
from datetime import datetime

def converter_timestamp(ts):
    try:
        return datetime.fromtimestamp(ts / 1000).strftime('%d/%m/%Y %H:%M:%S')
    except:
        return "Timestamp inválido"

def conectar_db(caminho):
    try:
        conn = sqlite3.connect(caminho)
        print(f"[+] Conectado ao banco: {caminho}")
        return conn
    except Exception as e:
        print(f"[!] Erro na conexão: {e}")
        return None

def extrair_mensagens(db_path):
    conn = conectar_db(db_path)
    if not conn:
        return []

    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT messages._id, messages.key_remote_jid, messages.key_from_me,
                   messages.data, messages.timestamp, messages.media_wa_type
            FROM messages
            WHERE messages.data IS NOT NULL
            ORDER BY messages.timestamp DESC
            LIMIT 100
        """)
        resultados = cursor.fetchall()
        conn.close()

        mensagens = []
        for mid, jid, from_me, texto, ts, tipo in resultados:
            mensagens.append({
                "ID": mid,
                "Contato": jid,
                "Direção": "Enviado" if from_me == 1 else "Recebido",
                "Mensagem": texto,
                "Timestamp": converter_timestamp(ts),
                "Tipo": tipo
            })
        return mensagens
    except Exception as e:
        print(f"[!] Erro ao extrair mensagens: {e}")
        return []

def salvar_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    print(f"[✓] Mensagens salvas em: {nome_arquivo}")

def main():
    db_path = input("Caminho do arquivo msgstore.db (SQLite): ").strip()

    if not os.path.exists(db_path):
        print("[!] Arquivo não encontrado.")
        return

    mensagens = extrair_mensagens(db_path)
    if mensagens:
        salvar_json(mensagens, "mensagens_whatsapp.json")
    else:
        print("[!] Nenhuma mensagem extraída.")

if __name__ == "__main__":
    main()
