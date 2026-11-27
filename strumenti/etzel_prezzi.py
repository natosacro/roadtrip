# Prezzi Etzelpark Benzin (E0 95) delle stazioni sul percorso, dalla pagina pubblica dei Standorte.
# Scrive ../etzel.json, che l'app mostra nelle note "pieno conveniente". Uso: python3 strumenti/etzel_prezzi.py
import json, os, re, html, subprocess, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://etzelparkbenzin.ch/standorte'
STAZIONI = {'ostermundigen': 'Ostermundigen BE', 'bellinzona': 'Bellinzona TI', 'dintikon': 'Dintikon AG'}

pagina = ''
for _ in range(3):
    r = subprocess.run(['curl', '-sS', '-L', '-m', '40', '-A', 'Mozilla/5.0', URL], capture_output=True, text=True, errors='ignore')
    pagina = r.stdout
    if 'Standort' in pagina:
        break
testo = re.sub(r'<(script|style).*?</\1>', '', pagina, flags=re.S)
righe = [x.strip() for x in html.unescape(re.sub(r'<[^>]+>', '\n', testo)).split('\n') if x.strip()]
# nella lista completa ogni stazione ha prezzi e "Stand <data>"; si parte da lì
inizio = righe.index('Standortliste') if 'Standortliste' in righe else 0
dati = {}
for sid, nome in STAZIONI.items():
    try:
        i = righe.index(nome, inizio)
    except ValueError:
        continue
    blocco = righe[i:i + 40]
    fine = next((k for k, x in enumerate(blocco) if x == 'Stand'), None)
    if fine is None:
        continue
    prezzi = {}
    for k in range(fine):
        if blocco[k] in ('E0 95', 'E0 98', 'B0 Diesel') and re.fullmatch(r'\d+\.\d+', blocco[k + 1]):
            prezzi[blocco[k]] = float(blocco[k + 1])
    m = re.fullmatch(r'(\d\d)\.(\d\d)\.(\d{4})', blocco[fine + 1])
    if 'E0 95' in prezzi and m:
        dati[sid] = {'e95': prezzi['E0 95'], 'data': f'{m.group(3)}-{m.group(2)}-{m.group(1)}'}
if not dati:
    print(json.dumps({'letto': False}))
    raise SystemExit(0)   # niente errore: l'app continua con l'ultimo file salvato
out = {'fonte': 'etzelparkbenzin.ch', 'verificato': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'stazioni': dati}
json.dump(out, open(os.path.join(BASE, 'etzel.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out))
