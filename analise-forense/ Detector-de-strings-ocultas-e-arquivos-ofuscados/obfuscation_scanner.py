#!/usr/bin/env python3
import os
import sys
import re
import base64
import yara
from pathlib import Path

def detectar_strings_suspeitas(conteudo):
    suspeitas = []

    base64s = re.findall(rb'([A-Za-z0-9+/]{30,}={0,2})', conteudo)
    for b in base64s:
        try:
            decodificado = base64.b64decode(b).decode('utf-8')
            if any(c.isprintable() for c in decodificado):
                suspeitas.append(("base64", b.decode()))
        except:
            continue

    patterns = {
        "shell_exec": rb'(bash|sh|powershell|cmd\.exe)',
        "scripts_embutidos": rb'<script>.*?</script>',
        "ofuscado_hex": rb'(\\x[0-9a-fA-F]{2})+',
        "powershell_encoded": rb'(?i)powershell.+-enc(odedcommand)?',
    }

    for label, pattern in patterns.items():
        matches = re.findall(pattern, conteudo)
        for match in matches:
            suspeitas.append((label, match.decode(errors="ignore")))

    return suspeitas

def carregar_yara_rules():
    regras = """
    rule ExecutavelEscondido
    {
        strings:
            $mz = "MZ"
        condition:
            $mz at 0
    }
    """
    return yara.compile(source=regras)

def escanear_arquivo(path):
    print(f"[+] Analisando: {path}")
    suspeitas = []

    with open(path, "rb") as f:
        conteudo = f.read()

    yara_rules = carregar_yara_rules()
    matches = yara_rules.match(data=conteudo)
    if matches:
        suspeitas.append(("yara", [match.rule for match in matches]))

    suspeitas += detectar_strings_suspeitas(conteudo)

    if suspeitas:
        print(f"[!] Suspeitas detectadas em {path}:")
        for tipo, dado in suspeitas:
            print(f"  -> [{tipo}] {dado[:100]}{'...' if len(dado) > 100 else ''}")
    else:
        print("[-] Nada suspeito detectado.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 obfuscation_scanner.py <arquivo>")
        sys.exit(1)

    arquivo = sys.argv[1]
    if not os.path.isfile(arquivo):
        print(f"[-] Arquivo não encontrado: {arquivo}")
        sys.exit(1)

    escanear_arquivo(arquivo)
