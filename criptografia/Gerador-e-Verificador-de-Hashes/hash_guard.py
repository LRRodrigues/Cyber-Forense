#!/usr/bin/env python3
import os
import time
import json
import hmac
import hashlib
from base64 import b64encode
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.backends import default_backend
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ========= CONFIGURAÇÃO ============
DIR_MONITORADO = "/caminho/para/monitorar"  # <-- personalize
HMAC_KEY = b'sua_chave_hmac_super_secreta'
CHAVE_PRIVADA_PEM = "chave_privada.pem"
MANIFESTO = "manifest_integridade.json"
ALGORITMO_HASH = "sha256"
# ===================================

def carregar_chave_privada(path):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

def calcular_hash_hmac(arquivo):
    h = hmac.new(HMAC_KEY, digestmod=hashlib.new(ALGORITMO_HASH))
    with open(arquivo, "rb") as f:
        for bloco in iter(lambda: f.read(4096), b""):
            h.update(bloco)
    return h.hexdigest()

def assinar_timestamp(priv_key, timestamp):
    assinatura = priv_key.sign(
        timestamp.encode(),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return b64encode(assinatura).decode()

def atualizar_manifesto(arquivo, acao):
    priv_key = carregar_chave_privada(CHAVE_PRIVADA_PEM)
    hash_hmac = calcular_hash_hmac(arquivo)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    assinatura = assinar_timestamp(priv_key, timestamp)

    entrada = {
        "arquivo": arquivo,
        "acao": acao,
        "hash_hmac": hash_hmac,
        "timestamp": timestamp,
        "assinatura": assinatura
    }

    if not os.path.exists(MANIFESTO):
        dados = []
    else:
        with open(MANIFESTO, "r") as f:
            dados = json.load(f)

    dados.append(entrada)
    with open(MANIFESTO, "w") as f:
        json.dump(dados, f, indent=4)

    print(f"[+] {acao.upper()} registrado: {arquivo}")

class MonitorHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            atualizar_manifesto(event.src_path, "modificado")

    def on_created(self, event):
        if not event.is_directory:
            atualizar_manifesto(event.src_path, "criado")

    def on_deleted(self, event):
        if not event.is_directory:
            atualizar_manifesto(event.src_path, "excluído")

if __name__ == "__main__":
    print(f"[+] Monitorando alterações em: {DIR_MONITORADO}")
    observer = Observer()
    observer.schedule(MonitorHandler(), DIR_MONITORADO, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
