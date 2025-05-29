#!/usr/bin/env python3

import os
import sys
import xmltodict
import pandas as pd
from Evtx.Evtx import Evtx

def extrair_eventos(arquivo_evtx):
    print(f"[+] Lendo arquivo: {arquivo_evtx}")
    eventos = []

    with Evtx(arquivo_evtx) as log:
        for record in log.records():
            try:
                xml = xmltodict.parse(record.xml())
                eventos.append(xml)
            except Exception as e:
                print(f"[!] Erro ao converter evento: {e}")
                continue
    return eventos

def salvar_csv(eventos, saida):
    print(f"[+] Extraindo campos e salvando em CSV: {saida}")
    dados = []

    for evento in eventos:
        try:
            e = evento['Event']
            dados.append({
                'EventID': e['System']['EventID']['#text'] if isinstance(e['System']['EventID'], dict) else e['System']['EventID'],
                'TimeCreated': e['System']['TimeCreated']['@SystemTime'],
                'Provider': e['System']['Provider']['@Name'],
                'Level': e['System'].get('Level', 'N/A'),
                'Computer': e['System']['Computer'],
                'Message': str(e.get('EventData', {}))
            })
        except Exception as ex:
            continue

    df = pd.DataFrame(dados)
    df.to_csv(saida, index=False)
    print("[✓] Exportado com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 parse_evtx.py <arquivo.evtx>")
        sys.exit(1)

    evtx_file = sys.argv[1]
    if not os.path.exists(evtx_file):
        print(f"[!] Arquivo não encontrado: {evtx_file}")
        sys.exit(1)

    eventos = extrair_eventos(evtx_file)
    salvar_csv(eventos, "eventos_extraidos.csv")
