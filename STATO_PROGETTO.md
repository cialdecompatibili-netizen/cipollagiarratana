# Cipolla Giarratana - stato del progetto

Ultimo aggiornamento: 09/11/2026 (sera).
Repo: `cialdecompatibili-netizen/cipollagiarratana` (cartella `Desktop\repository\cipollagiarratana`). Clone di mistraltemplate1.
Sito: https://cialdecompatibili-netizen.github.io/cipollagiarratana/ - shop: `/negozio/`.
Nota: la cartella `cipolla-giarratana` (con trattino) e' vecchia, senza remote: NON usarla.

## Fatto
- 7 categorie, 26 prodotti IT+EN, menu, home (commit 08/11).
- Foto prodotto con Gemini (09/11): 18 su 26 generate e collegate (webp in `assets/images/prodotti/<id>.webp`, campo `immagine` in `_data/catalogo.json`). Foto senza testo, sfondo bianco, controllate a campione (2 viste, ok).
- Perche' mancavano: il campo `immagine` era vuoto su tutti i prodotti (il template mostra la foto solo se compilato).

## Da fare (domani)
1. Foto mancanti (8 prodotti): `piantine-12`, `kit-coltiva`, `guida-coltivazione`, `ricettario`, `guida-conservare`, `box-assaggio`, `box-cucina`, `box-natale`.
   Comando: `python automation/foto_prodotti.py` (senza argomenti fa solo i prodotti senza foto, poi collega al catalogo e fa commit+push; `--no-push` per provare). Costa ~3 crediti Gemini a foto.
2. Guardare le 16 foto non ancora viste (testo storpiato, marche inventate, sfondo grigio) e rifare quelle storte: `python automation/foto_prodotti.py <id>` (rigenera quell'id).
3. Verificare online dopo la build (shop, prodotto IT e EN, foto): non ancora controllato.
4. Prezzi e testi dei prodotti sono segnaposto da confermare con Mirco.

## Note tecniche
- Generatore immagini unico: `Desktop\gemini_auto\img.py` (guida `Desktop\gemini_auto\IMMAGINI_API.md`). Crediti: `python Desktop\gemini_auto\img.py --crediti`. A fine serata: account 1 reset 21:31, account 3 (pieno) reset 20:56.
- Soggetti delle foto (in inglese, senza testo) stanno in `automation/foto_prodotti.py` (dizionario `SOGG`).
- Sito multilingua: le foto non devono avere scritte.
- Pubblicazione contenuti in generale: `python automation/sviluppa.py`.
