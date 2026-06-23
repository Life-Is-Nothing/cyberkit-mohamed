#!/usr/bin/env python3
# SSH Log Analyzer - ibramoha2
# Detecte les tentatives de brute-force dans auth.log
import argparse, re
from collections import defaultdict

def analyze(filepath, threshold=10):
    failed = defaultdict(int)
    success = []
    with open(filepath, errors='ignore') as f:
        for line in f:
            m = re.search(r'Failed password.*from ([0-9.]+)', line)
            if m: failed[m.group(1)] += 1
            m = re.search(r'Accepted .* for (\w+) from ([0-9.]+)', line)
            if m: success.append((m.group(1), m.group(2)))
    print(f'\n=== SSH Log Analysis: {filepath} ===')
    print(f'\n[!] IPs avec +{threshold} echecs:')
    attackers = {ip:c for ip,c in failed.items() if c >= threshold}
    if attackers:
        for ip, c in sorted(attackers.items(), key=lambda x:-x[1]):
            print(f'  {ip:20s} {c} tentatives')
    else:
        print('  Aucune trouvee.')
    print(f'\n[+] Dernieres connexions reussies:')
    for user, ip in success[-5:]:
        print(f'  {user} depuis {ip}')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--file', default='/var/log/auth.log')
    ap.add_argument('--threshold', type=int, default=10)
    args = ap.parse_args()
    analyze(args.file, args.threshold)
