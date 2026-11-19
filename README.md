# Road trip d'Avvento

App del nostro road trip in Svizzera, 8–13 dicembre 2026: mappa delle leg, programma giorno per giorno,
prossima tappa con Google Maps, strade e cantoni, rubrica, guida (mercatini, vegano, racchette, budget)
e l'autoradio con HPR3 Heartland Christmas.

Si apre su https://natosacro.github.io/roadtrip/ e si installa dal browser sulla schermata Home.

- `index.html` — tutta l'app
- `manifest.json`, `sw.js`, `icona-*.png` — installazione e funzionamento offline
- `benzina.json` — prezzo medio svizzero della benzina (TCS), aggiornato ogni 2 giorni da
  `.github/workflows/benzina.yml` con `strumenti/benzina_tcs.py`
