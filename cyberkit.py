#!/usr/bin/env python3
"""
CyberKit Mohamed — Penetration Testing & Audit Toolkit
Author: Mohamed Adoungouss Ibrahim (@ibramoha2)
Version: 1.0.0
"""

import subprocess
import sys
import os
import socket
import datetime
from typing import Optional

BANNER = r"""
  ____      _               _  ___ _   
 / ___|   _| |__   ___ _ __| |/ (_) |_ 
| |  | | | | '_ \ / _ \ '__| ' /| | __|
| |__| |_| | |_) |  __/ |  | . \| | |_ 
 \____\__, |_.__/ \___|_|  |_|\_\_|\__|
      |___/   Mohamed Adoungouss Ibrahim
      
[*] Penetration Testing & Audit Toolkit v1.0
[*] For authorized security testing only
"""

def run_cmd(cmd: str) -> str:
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "[!] Timeout"
    except Exception as e:
        return f"[!] Error: {e}"

def nmap_scan(target: str, scan_type: str = "basic") -> str:
    scans = {
        "basic":    f"nmap -sV -sC -T4 {target}",
        "full":     f"nmap -sV -sC -p- -T4 {target}",
        "udp":      f"nmap -sU --top-ports 100 {target}",
        "vuln":     f"nmap --script vuln {target}",
        "stealth":  f"nmap -sS -T2 -f {target}",
        "web":      f"nmap -sV -p 80,443,8080,8443 --script http-title,http-headers {target}",
    }
    cmd = scans.get(scan_type, scans["basic"])
    print(f"[*] Running: {cmd}")
    return run_cmd(cmd)

def port_check(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=3):
            return True
    except:
        return False

def whois_lookup(domain: str) -> str:
    return run_cmd(f"whois {domain} 2>/dev/null | head -40")

def dns_recon(domain: str) -> str:
    output = []
    output.append(f"[*] DNS Recon for {domain}")
    output.append(run_cmd(f"dig A {domain} +short"))
    output.append(run_cmd(f"dig MX {domain} +short"))
    output.append(run_cmd(f"dig NS {domain} +short"))
    output.append(run_cmd(f"dig TXT {domain} +short"))
    return "\n".join(output)

def http_headers(url: str) -> str:
    return run_cmd(f"curl -sI {url} 2>/dev/null | head -30")

def ssl_check(domain: str) -> str:
    return run_cmd(f"echo | openssl s_client -connect {domain}:443 2>/dev/null | openssl x509 -noout -text 2>/dev/null | head -30")

def save_report(content: str, target: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{target.replace('.','_')}_{timestamp}.txt"
    os.makedirs("reports", exist_ok=True)
    with open(f"reports/{filename}", "w") as f:
        f.write(content)
    return filename

def menu():
    print(BANNER)
    print("=" * 50)
    print("[1] Nmap Scan")
    print("[2] DNS Recon")
    print("[3] WHOIS Lookup")
    print("[4] HTTP Headers")
    print("[5] SSL Certificate Check")
    print("[6] Port Check")
    print("[0] Quitter")
    print("=" * 50)

def main():
    menu()
    while True:
        try:
            choice = input("\n[cyberkit]> ").strip()
            if choice == "0":
                print("[*] Bye!")
                break
            elif choice == "1":
                target = input("[*] Cible (IP/domaine) : ").strip()
                scan_type = input("[*] Type [basic/full/vuln/udp/stealth/web] : ").strip() or "basic"
                result = nmap_scan(target, scan_type)
                print(result)
                if input("[*] Sauvegarder le rapport ? [o/N] ").lower() == "o":
                    fname = save_report(result, target)
                    print(f"[+] Rapport sauvegardé : {fname}")
            elif choice == "2":
                domain = input("[*] Domaine : ").strip()
                print(dns_recon(domain))
            elif choice == "3":
                domain = input("[*] Domaine/IP : ").strip()
                print(whois_lookup(domain))
            elif choice == "4":
                url = input("[*] URL (ex: https://example.com) : ").strip()
                print(http_headers(url))
            elif choice == "5":
                domain = input("[*] Domaine : ").strip()
                print(ssl_check(domain))
            elif choice == "6":
                host = input("[*] Host : ").strip()
                port = int(input("[*] Port : ").strip())
                status = "OUVERT ✅" if port_check(host, port) else "FERMÉ ❌"
                print(f"[*] {host}:{port} → {status}")
            else:
                print("[!] Choix invalide")
        except KeyboardInterrupt:
            print("\n[*] Interrupted")
            break

if __name__ == "__main__":
    main()
