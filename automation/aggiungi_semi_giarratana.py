import json, os
R = r"C:\Users\mirco\Desktop\repository\cipollagiarratana"
P = os.path.join(R, "_data", "catalogo.json")
d = json.load(open(P, encoding="utf-8"))
IMG = "assets/images/prodotti/semi-cipolla-giarratana-demo.svg"
os.makedirs(os.path.join(R, "assets", "images", "prodotti"), exist_ok=True)
open(os.path.join(R, IMG), "w", encoding="utf-8", newline="\n").write(
 '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800"><rect width="800" height="800" fill="#f3e6c8"/>'
 '<text x="400" y="440" font-size="320" text-anchor="middle">\U0001F9C5</text>'
 '<text x="400" y="640" font-size="44" text-anchor="middle" fill="#7a5a1e" font-family="Georgia,serif">Foto demo</text></svg>')
d["prodotti"] = [p for p in d["prodotti"] if p["id"] != "semi-1"]
d["prodotti"].insert(0, {
 "tipo": "fisico", "id": "semi-cipolla-giarratana",
 "nome": "Semi di cipolla di Giarratana", "categoria": "semi",
 "prezzo_centesimi": 400,
 "descrizione": "Bustina di semi di cipolla di Giarratana, Presidio Slow Food del Ragusano, da seminare in semenzaio e trapiantare nel tuo orto.",
 "descrizione_completa": "Bustina di semi di cipolla di Giarratana, Presidio Slow Food dell'altopiano ibleo.\nSi semina in semenzaio da fine ottobre e si trapianta tra febbraio e marzo; la raccolta arriva in estate.\nÈ una cipolla dolce e mai pungente, dal bulbo grande.",
 "immagine": IMG, "icona": "\U0001F9C5", "visibile": True,
 "tr": {"en": {
  "nome": "Giarratana onion seeds",
  "descrizione": "Packet of Giarratana onion seeds, a Slow Food Presidium from the Ragusa area, to sow in a seedbed and transplant into your garden.",
  "descrizione_completa": "Packet of Giarratana onion seeds, a Slow Food Presidium from the Hyblaean plateau.\nSow in a seedbed from late October and transplant between February and March; harvest comes in summer.\nA sweet, never pungent onion with a large bulb."}}})
open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
json.load(open(P, encoding="utf-8"))
def w(rel, t):
    p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(t)
w("_negozio/semi-cipolla-giarratana.md", '''---
layout: negozio-prodotto
title: "Semi di cipolla di Giarratana"
pid: semi-cipolla-giarratana
permalink: /negozio/semi-cipolla-giarratana/
description: "Semi di cipolla di Giarratana, Presidio Slow Food del Ragusano: bustina da seminare nel tuo orto."
ref: shop-prod-semi-cipolla-giarratana
---
''')
w("en/negozio/semi-cipolla-giarratana.md", '''---
layout: negozio-prodotto
title: "Giarratana onion seeds"
pid: semi-cipolla-giarratana
permalink: /en/shop/giarratana-onion-seeds/
description: "Giarratana onion seeds, a Slow Food Presidium from the Ragusa area: a packet to sow in your garden."
lang: en
locale: en
ref: shop-prod-semi-cipolla-giarratana
tr: tradotto
---
''')
print("OK")
