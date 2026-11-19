# Prezzo medio svizzero della benzina dalla pagina pubblica del TCS ("Benzinpreise in der Schweiz und in Europa").
# Scrive ../benzina.json, che l'app legge per il budget. Uso: python3 strumenti/benzina_tcs.py
import json, os, re, html, subprocess, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://www.tcs.ch/de/camping-reisen/reiseinformationen/wissenswertes/fahrkosten-gebuehren/benzinpreise.php'

pagina = ''
for _ in range(3):
    r = subprocess.run(['curl', '-sS', '-L', '-m', '40', '-A', 'Mozilla/5.0', URL], capture_output=True, text=True)
    pagina = r.stdout
    if 'Schweiz' in pagina:
        break
testo = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style).*?</\1>', '', pagina, flags=re.S))))
# es. "Schweiz 1.89 2 2.29 Unverändert gültig seit: 18.11.2026"
m = re.search(r'Schweiz (\d+(?:\.\d+)?) (\d+(?:\.\d+)?) (\d+(?:\.\d+)?) (?:\d+(?:\.\d+)? )?\w+ g\w+ltig seit: (\d\d)\.(\d\d)\.(\d{4})', testo)
if not m:
    print(json.dumps({'letto': False}))
    raise SystemExit(0)   # niente errore: l'app continua a usare l'ultimo prezzo salvato
p95, p98, dsl = (round(float(x), 2) for x in m.group(1, 2, 3))
f = os.path.join(BASE, 'benzina.json')
dati = {
    'fonte': 'TCS',
    'data': f'{m.group(6)}-{m.group(5)}-{m.group(4)}',
    'bleifrei95': p95, 'super98': p98, 'diesel': dsl,
    'verificato': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
}
json.dump(dati, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(dati))
