import json, os
R = r"C:\Users\mirco\Desktop\repository\cipollagiarratana"
P = os.path.join(R, "_data", "catalogo.json")
d = json.load(open(P, encoding="utf-8"))
OLD = "semi-cipolla-giarratana"
IM = os.path.join(R, "assets", "images", "prodotti"); os.makedirs(IM, exist_ok=True)
def svg(pid, label):
    open(os.path.join(IM, pid + "-demo.svg"), "w", encoding="utf-8", newline="\n").write(
     '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800"><rect width="800" height="800" fill="#f3e6c8"/>'
     '<text x="400" y="440" font-size="320" text-anchor="middle">\U0001F9C5</text>'
     '<text x="400" y="640" font-size="48" text-anchor="middle" fill="#7a5a1e" font-family="Georgia,serif">' + label + '</text></svg>')
def w(rel, t):
    p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(t)
prods = []
for n in range(50, 501, 50):
    pid = "semi-cipolla-giarratana-%d" % n
    prods.append(dict(id=pid, tipo="fisico", cat="semi", prezzo=300 + (n // 50 - 1) * 200 if n > 50 else 300,
      it=("Semi di cipolla di Giarratana, %d semi" % n,
          "Bustina da %d semi di cipolla di Giarratana, Presidio Slow Food del Ragusano, da seminare in semenzaio." % n,
          "Bustina da %d semi di cipolla di Giarratana, Presidio Slow Food dell'altopiano ibleo.\nSi semina in semenzaio da fine ottobre e si trapianta tra febbraio e marzo; la raccolta arriva in estate." % n),
      en=("Giarratana onion seeds, %d seeds" % n,
          "Packet of %d Giarratana onion seeds, a Slow Food Presidium from the Ragusa area, to sow in a seedbed." % n,
          "Packet of %d Giarratana onion seeds, a Slow Food Presidium from the Hyblaean plateau.\nSow in a seedbed from late October and transplant between February and March; harvest comes in summer." % n),
      pe="giarratana-onion-seeds-%d" % n, label="%d semi" % n))
prods += [
 dict(id="confettura-cipolla-giarratana", tipo="fisico", cat="secchi", prezzo=650,
  it=("Confettura di cipolla di Giarratana", "Confettura dolce di cipolla di Giarratana, da abbinare a formaggi e carni.", "Confettura dolce di cipolla di Giarratana, Presidio Slow Food.\nOttima con formaggi stagionati e carni."),
  en=("Giarratana onion jam", "Sweet Giarratana onion jam, perfect with cheese and meat.", "Sweet jam made with Giarratana onion, a Slow Food Presidium.\nGreat with aged cheese and meat."),
  pe="giarratana-onion-jam", label="Confettura"),
 dict(id="cipolla-giarratana-fresca", tipo="fisico", cat="freschi", prezzo=900,
  it=("Cipolle di Giarratana fresche", "Cipolle di Giarratana fresche, dolci e mai pungenti, disponibili nella stagione del raccolto.", "Cipolle di Giarratana fresche, dolci e mai pungenti, dal bulbo grande.\nDisponibili da fine luglio a fine agosto, in base al raccolto."),
  en=("Fresh Giarratana onions", "Fresh Giarratana onions, sweet and never pungent, available in the harvest season.", "Fresh Giarratana onions, sweet and never pungent, with a large bulb.\nAvailable from late July to late August, depending on the harvest."),
  pe="fresh-giarratana-onions", label="Fresche"),
 dict(id="guida-coltivazione-giarratana", tipo="digitale", cat="libri", prezzo=900,
  it=("Guida alla coltivazione della cipolla di Giarratana", "Guida digitale per coltivare e conservare la cipolla di Giarratana.", "Guida in formato digitale per coltivare e conservare la cipolla di Giarratana: semina, trapianto, raccolta."),
  en=("Giarratana onion growing guide", "Digital guide to growing and storing the Giarratana onion.", "Digital guide to growing and storing the Giarratana onion: sowing, transplanting, harvest."),
  pe="giarratana-onion-growing-guide", label="Guida"),
]
d["prodotti"] = [p for p in d["prodotti"] if p["categoria"] not in ("semi", "secchi", "freschi", "libri")]
for p in prods:
    svg(p["id"], p["label"])
    d["prodotti"].append({"tipo": p["tipo"], "id": p["id"], "nome": p["it"][0], "categoria": p["cat"],
      "prezzo_centesimi": p["prezzo"], "descrizione": p["it"][1], "descrizione_completa": p["it"][2],
      "immagine": "assets/images/prodotti/%s-demo.svg" % p["id"], "icona": "\U0001F9C5", "visibile": True,
      "tr": {"en": {"nome": p["en"][0], "descrizione": p["en"][1], "descrizione_completa": p["en"][2]}}})
    w("_negozio/%s.md" % p["id"], '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /negozio/%s/\ndescription: "%s"\nref: shop-prod-%s\n---\n' % (p["it"][0], p["id"], p["id"], p["it"][1], p["id"]))
    w("en/negozio/%s.md" % p["id"], '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /en/shop/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-prod-%s\ntr: tradotto\n---\n' % (p["en"][0], p["id"], p["pe"], p["en"][1], p["id"]))
open(P, "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
json.load(open(P, encoding="utf-8"))
for rel in ["_negozio/%s.md" % OLD, "en/negozio/%s.md" % OLD, "assets/images/prodotti/%s-demo.svg" % OLD]:
    f = os.path.join(R, rel)
    if os.path.exists(f): os.remove(f)
print("OK", len(prods))
