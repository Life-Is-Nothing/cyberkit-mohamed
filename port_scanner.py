#!/usr/bin/env python3
# Port Scanner (educational) - ibramoha2
# Usage sur vos propres systemes uniquement.
import socket, argparse, threading
from datetime import datetime

results = []
lock = threading.Lock()

def scan(ip, port):
    try:
        s = socket.socket()
        s.settimeout(0.5)
        if s.connect_ex((ip, port)) == 0:
            try: svc = socket.getservbyport(port)
            except: svc = 'unknown'
            with lock:
                results.append(port)
                print(f'  [+] {port}/tcp OPEN ({svc})')
        s.close()
    except: pass

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-t', '--target', required=True)
    ap.add_argument('-p', '--ports', default='1-1024')
    args = ap.parse_args()
    ip = socket.gethostbyname(args.target)
    s, e = map(int, args.ports.split('-'))
    print(f'Scanning {ip} ports {s}-{e}')
    ts = []
    for p in range(s, e+1):
        t = threading.Thread(target=scan, args=(ip, p))
        ts.append(t); t.start()
        if len(ts) >= 150:
            for t in ts: t.join()
            ts = []
    for t in ts: t.join()
    print(f'{len(results)} open ports found.')
