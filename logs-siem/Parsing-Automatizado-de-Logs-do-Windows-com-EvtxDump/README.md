# 📜 Parsing de Arquivos de Log do Windows (.evtx)

## 🎯 Objetivo

Automatizar a análise forense de arquivos `.evtx` (logs nativos do Windows) extraindo dados relevantes para investigação de:

- Logons suspeitos
- Escalonamento de privilégios
- Execução de binários
- Ataques internos
- Persistência

## ⚙️ Requisitos

- Python 3.8 ou superior
- Bibliotecas:

```bash
pip install python-evtx xmltodict pandas




📌 Dica Rápida de Eventos Relevantes
EventID	Descrição
4624	Logon bem-sucedido
4625	Logon falhou
4688	Novo processo criado
1102	Log do sistema foi limpo (!!!)
4697	Novo serviço instalado
7036	Serviço iniciou/parou
4720	Nova conta de usuário criada
4722	Conta de usuário ativada
