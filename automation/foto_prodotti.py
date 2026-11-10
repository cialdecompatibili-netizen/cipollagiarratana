# -*- coding: utf-8 -*-
"""Genera le foto prodotto mancanti (immagine vuota nel catalogo) con gemini_auto\img.py, le collega al catalogo e fa push.
Uso: python automation/foto_prodotti.py [--no-push] [id ...]   (senza id = tutti quelli senza foto)
Foto SENZA testo (sito multilingua), sfondo bianco, webp in assets/images/prodotti/<id>.webp"""
import csv, json, os, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(R, '_data', 'catalogo.json')
OUT = os.path.join(R, 'assets', 'images', 'prodotti')
IMG = r'C:\Users\mirco\Desktop\gemini_auto\img.py'
EXTRA = ('ABSOLUTELY NO TEXT of any kind: no letters, no numbers, no words, no dates, no logos, no brand names. '
         'Labels and covers must be completely blank. The image must be language-neutral. Plain pure white #FFFFFF background.')
G = 'Giarratana onion (very large, sweet, flat-round, pale golden-yellow skin)'
SOGG = {
 'cipolla-fresca-1kg': 'three large ' + G + ' bulbs stacked on a small kraft paper bag',
 'cipolla-fresca-5kg': 'open wooden crate full of large ' + G + ' bulbs',
 'cipolla-fresca-10kg': 'big wooden crate overflowing with large ' + G + ' bulbs, slatted wood',
 'cipolla-gigante-1pz': 'one single huge ' + G + ' bulb, whole, with a half cut open beside it showing white layers',
 'confettura-220': 'small glass jar of golden onion jam with blank rustic cloth lid cover, a spoon of jam beside it',
 'confettura-peperoncino-220': 'small glass jar of onion and chili jam, amber with red chili flakes, blank label, one red chili beside it',
 'confettura-vino-220': 'small glass jar of deep burgundy red-wine onion jam, blank label, small bunch of grapes beside it',
 'agrodolce-280': 'glass jar of small pearl onions in sweet and sour brine, golden-brown, blank label',
 'sottolio-280': 'glass jar of sliced onions preserved in olive oil, with a sprig of rosemary, blank label',
 'crema-190': 'small glass jar of smooth creamy onion spread, pale beige, blank label, a bread slice with spread beside it',
 'sugo-300': 'glass jar of onion and tomato pasta sauce, rich red, blank label, a fresh basil leaf beside it',
 'pesto-130': 'small glass jar of onion and almond pesto, pale green-beige, blank label, a few almonds beside it',
 'salsa-formaggi-120': 'small glass jar of golden onion sauce, a small wedge of aged cheese beside it, blank label',
 'essiccata-60': 'kraft pouch with a window showing dried onion flakes, a small pile of dried onion flakes beside it, blank label',
 'polvere-50': 'small glass spice jar of fine onion powder, a little wooden spoon with powder beside it, blank label',
 'chips-40': 'kraft paper bag of crispy onion chips, a few golden onion chips spilled beside it, blank label',
 'semi-bustina': 'small paper seed packet of onion seeds, blank cover, a few black seeds spilled beside it',
 'semi-10g': 'small glass vial of black onion seeds with kraft tag, blank, black seeds in a tiny wooden spoon beside it',
 'piantine-12': 'tray of twelve young green onion seedlings in small pots, fresh soil, garden light',
 'kit-coltiva': 'grow-your-own kit: rustic planter pot with soil, seed packet and small wooden garden tools, blank labels',
 'guida-coltivazione': 'closed paperback book standing, completely blank cover with a hand-drawn illustration of a large onion plant, no text',
 'ricettario': 'closed hardcover cookbook, blank cover with a simple illustration of a large golden onion, no text, wooden spoon beside it',
 'guida-conservare': 'closed paperback guide book with blank cover illustration of preserve jars, no text, a jar beside it',
 'box-assaggio': 'open gift box with small jars of onion jam, onion cream and sweet and sour onions, plus onion chips pouch, blank labels, kraft filling',
 'box-cucina': 'open wooden box with large onion bulbs, jar of onion sauce, jar of onion pesto, dried onion pouch, blank labels',
 'box-natale': 'Christmas gift box with red ribbon, jars of onion jam and onion cream, large onion bulb, pine sprig and small baubles, blank labels',
}

def sh(*a):
    return subprocess.run(a, cwd=R, capture_output=True, text=True, encoding='utf-8', errors='replace')

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    push = '--no-push' not in sys.argv
    d = json.load(open(CAT, encoding='utf-8'))
    prod = d['prodotti']
    os.makedirs(OUT, exist_ok=True)
    todo = [p['id'] for p in prod if p['id'] in SOGG and (args and p['id'] in args or not args and not p.get('immagine'))]
    todo = [i for i in todo if not os.path.exists(os.path.join(OUT, i + '.webp')) or args]
    print('da generare:', len(todo), todo)
    if todo:
        lista = os.path.join(R, 'automation', 'tmp_lista.csv')
        os.makedirs(os.path.dirname(lista), exist_ok=True)
        with open(lista, 'w', encoding='utf-8', newline='') as f:
            w = csv.writer(f, delimiter=';')
            for i in todo: w.writerow([i, SOGG[i], 'prodotto'])
        r = subprocess.run([sys.executable, IMG, '--lista', lista, '--out', OUT, '--extra', EXTRA], cwd=R, text=True, encoding='utf-8', errors='replace')
        print('img.py exit', r.returncode)
    ok = []
    for p in prod:
        f = os.path.join(OUT, p['id'] + '.webp')
        if p['id'] in SOGG and os.path.exists(f) and (not p.get('immagine') or p['id'] in args):
            p['immagine'] = 'assets/images/prodotti/' + p['id'] + '.webp'; ok.append(p['id'])
    if not ok:
        print('nessuna foto da collegare'); return
    json.dump(d, open(CAT, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
    print('collegate:', len(ok), ok)
    if push:
        sh('git', 'add', '-A', 'assets/images/prodotti', '_data/catalogo.json')
        print(sh('git', 'commit', '-m', 'Foto prodotti: ' + ', '.join(ok)).stdout[-300:])
        print(sh('git', 'push').stderr[-300:])

if __name__ == '__main__':
    main()
