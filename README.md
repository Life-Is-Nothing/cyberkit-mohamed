# Outils de Securite Reseau

> Scripts Python educatifs pour l'analyse reseau et la securite defensive.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python)
![Author](https://img.shields.io/badge/Author-ibramoha2-CC0000?style=flat-square)

> Pour usage ethique uniquement — sur vos propres systemes ou avec autorisation.

## Installation
```bash
git clone https://github.com/ibramoha2/cyberkit-mohamed
cd cyberkit-mohamed
pip install -r requirements.txt
```

## Outils

| Outil | Description |
|-------|-------------|
| `port_scanner.py` | Scanner de ports TCP multi-thread |
| `log_analyzer.py` | Analyse de logs SSH (detection brute-force) |
| `banner_grab.py` | Banner grabbing sur services reseau |

## Usage
```bash
python port_scanner.py -t 127.0.0.1 -p 1-1024
python log_analyzer.py -f /var/log/auth.log
```

**Auteur :** [@ibramoha2](https://github.com/ibramoha2) | Niger