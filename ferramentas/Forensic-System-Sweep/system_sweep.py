# system_sweep.py

import os
import platform
import socket
import json
import psutil
import netifaces
import distro
import hashlib
import hmac
import time
import subprocess
import paramiko
from datetime import datetime

# ===================== CONFIGURAÇÕES =====================
OUTPUT_DIR = "./output"
SECRET_KEY = b"CHAVE_SECRETA_SUPER_FORTE_32BYTES"  # Trocar por chave segura
TIMESTAMP = datetime.utcnow().isoformat()
FILENAME = f"sweep_{TIMESTAMP}.json"

REMOTE_HOSTS = []  # Ex: [("192.168.1.100", "user", "password")]

# ===================== FUNÇÕES BASE =====================
def get_hostname():
    return socket.gethostname()

def get_ip_mac():
    interfaces = {}
    for iface in netifaces.interfaces():
        try:
            addr = netifaces.ifaddresses(iface)
            ip = addr[netifaces.AF_INET][0]['addr'] if netifaces.AF_INET in addr else None
            mac = addr[netifaces.AF_LINK][0]['addr'] if netifaces.AF_LINK in addr else None
            interfaces[iface] = {'ip': ip, 'mac': mac}
        except Exception:
            continue
    return interfaces

def get_system_info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "distro": distro.name(pretty=True),
        "uptime": subprocess.getoutput("uptime -p"),
        "timezone": subprocess.getoutput("timedatectl | grep 'Time zone'")
    }

def get_cpu_memory_disk():
    return {
        "cpu_cores": psutil.cpu_count(logical=True),
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict()
    }

def get_users_and_auth():
    try:
        users = subprocess.getoutput("cut -d: -f1 /etc/passwd").splitlines()
        sudoers = subprocess.getoutput("getent group sudo")
        ssh_keys = subprocess.getoutput("find /home -name 'authorized_keys'")
        return {"users": users, "sudoers": sudoers, "ssh_keys": ssh_keys}
    except Exception as e:
        return {"error": str(e)}

def get_network_ports():
    try:
        ports = subprocess.getoutput("ss -tulnp")
        return ports
    except:
        return "Erro ao obter portas."

def get_processes():
    proc_list = []
    for p in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
        proc_list.append(p.info)
    return proc_list

def get_logs():
    logs = {
        "auth.log": subprocess.getoutput("tail -n 50 /var/log/auth.log"),
        "syslog": subprocess.getoutput("tail -n 50 /var/log/syslog")
    }
    return logs

def get_file_analysis():
    hidden = subprocess.getoutput("find /home -type f -name '.*'").splitlines()
    recent_exec = subprocess.getoutput("find /home -type f -perm -111 -mtime -7").splitlines()
    scripts = subprocess.getoutput("find /home -type f \( -name '*.sh' -o -name '*.py' \)").splitlines()
    return {
        "hidden_files": hidden,
        "recent_executables": recent_exec,
        "scripts": scripts
    }

def get_bios_info():
    try:
        bios_info = subprocess.getoutput("dmidecode -t bios")
        return bios_info
    except Exception as e:
        return f"Erro ao obter informações da BIOS: {e}"

def generate_hmac(data_str: str):
    return hmac.new(SECRET_KEY, data_str.encode(), hashlib.sha256).hexdigest()

def save_output(data, filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    json_data = json.dumps(data, indent=4)
    hmac_digest = generate_hmac(json_data)
    full_output = {
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
        "hmac": hmac_digest
    }
    with open(f"{OUTPUT_DIR}/{filename}", "w") as f:
        json.dump(full_output, f, indent=4)
    print(f"[+] Resultado salvo em: {OUTPUT_DIR}/{filename}")

# ===================== VARREDURA LOCAL =====================
def run_local_sweep():
    print("[+] Executando varredura forense local...")
    sweep = {
        "hostname": get_hostname(),
        "network": get_ip_mac(),
        "system_info": get_system_info(),
        "hardware": get_cpu_memory_disk(),
        "auth": get_users_and_auth(),
        "open_ports": get_network_ports(),
        "processes": get_processes(),
        "logs": get_logs(),
        "files": get_file_analysis(),
        "bios_info": get_bios_info()
    }
    save_output(sweep, FILENAME)

# ===================== VARREDURA REMOTA =====================
def run_remote_sweep(host, user, password):
    print(f"[+] Conectando a {host}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password, timeout=10)
        cmds = {
            "hostname": "hostname",
            "ip_mac": "ip a",
            "system": "uname -a",
            "uptime": "uptime -p",
            "timezone": "timedatectl | grep 'Time zone'",
            "cpu_mem": "free -m && lscpu",
            "users": "cut -d: -f1 /etc/passwd",
            "sudoers": "getent group sudo",
            "ssh_keys": "find /home -name 'authorized_keys'",
            "ports": "ss -tulnp",
            "processes": "ps aux",
            "logs": "tail -n 50 /var/log/auth.log; tail -n 50 /var/log/syslog",
            "hidden": "find /home -type f -name '.*'",
            "recent_exec": "find /home -type f -perm -111 -mtime -7",
            "scripts": "find /home -type f \( -name '*.sh' -o -name '*.py' \)",
            "bios_info": "dmidecode -t bios"
        }
        results = {}
        for key, cmd in cmds.items():
            stdin, stdout, stderr = client.exec_command(cmd)
            results[key] = stdout.read().decode(errors='ignore')
        filename = f"remote_sweep_{host}_{TIMESTAMP}.json"
        save_output(results, filename)
        client.close()
    except Exception as e:
        print(f"[-] Falha ao conectar com {host}: {e}")

# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    run_local_sweep()
    for host, user, pwd in REMOTE_HOSTS:
        run_remote_sweep(host, user, pwd)
