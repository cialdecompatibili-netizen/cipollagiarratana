import json, os, glob
R = r"C:\Users\mirco\Desktop\repository\cipollagiarratana"
def rd(rel): return open(os.path.join(R, rel), encoding="utf-8").read()
def wr(rel, t):
    p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(t)
def rep(t, a, b):
    assert t.count(a) == 1, a[:60]
    return t.replace(a, b)

# 1) masthead: le varianti entrano nel catalogo del carrello (id prodotto-codice)
m = rd("_includes/masthead.html")
var_loop = ('{%- for v in b.varianti -%}{%- assign nz_vl = v.tr[lg] | default: v.etichetta -%}{"id":{{ b.id | append: "-" | append: v.codice | jsonify }},"p":{{ v.prezzo_centesimi | default: 0 | jsonify }},'
 '"n":{{ b.tr[lg].nome | default: b.nome | append: " - " | append: nz_vl | jsonify }},"t":{{ b.tipo | default: "fisico" | jsonify }},'
 '"u":{{ nz_pu | jsonify }},"i":{% if b.immagine and b.immagine != "" %}{{ "/" | append: b.immagine | relative_url | jsonify }}{% else %}""{% endif %},'
 '"e":{{ b.icona | default: "" | jsonify }}},{%- endfor -%}')
m = rep(m, "{%- endunless -%}{%- endfor -%}{%- endcapture -%}", var_loop + "{%- endunless -%}{%- endfor -%}{%- endcapture -%}")
wr("_includes/masthead.html", m)

# 2) scheda prodotto: bottoni variante + JS
L = rd("_layouts/negozio-prodotto.html")
L = rep(L, "{%- assign nz_dig = false -%}", "{%- assign nz_dig = false -%}{%- assign nz_v0 = nz_p.varianti | first -%}")
old_attr = 'data-id="{{ nz_p.id }}" data-nome="{{ nz_p.tr[page.lang].nome | default: nz_p.nome | escape }}" data-prezzo="{{ nz_p.prezzo_centesimi | default: 0 }}"'
new_attr = ('data-base="{{ nz_p.tr[page.lang].nome | default: nz_p.nome | escape }}" data-id-base="{{ nz_p.id }}" '
 'data-id="{{ nz_p.id }}{% if nz_v0 %}-{{ nz_v0.codice }}{% endif %}" '
 'data-nome="{{ nz_p.tr[page.lang].nome | default: nz_p.nome | escape }}{% if nz_v0 %} - {{ nz_v0.tr[page.lang] | default: nz_v0.etichetta | escape }}{% endif %}" '
 'data-prezzo="{% if nz_v0 %}{{ nz_v0.prezzo_centesimi }}{% else %}{{ nz_p.prezzo_centesimi | default: 0 }}{% endif %}"')
L = rep(L, old_attr, new_attr)
btns = ('{%- if nz_v0 -%}\n<div class="nz-var-box"><p class="nz-var-t">{{ nz_p.tr[page.lang].varianti_titolo | default: nz_p.varianti_titolo | escape }}</p><div class="nz-var-lista" role="group">\n'
 '{%- for v in nz_p.varianti -%}<button type="button" class="nz-var{% if forloop.first %} on{% endif %}" data-codice="{{ v.codice }}" data-prezzo="{{ v.prezzo_centesimi }}" '
 'data-nome="{{ v.tr[page.lang] | default: v.etichetta | escape }}" aria-pressed="{% if forloop.first %}true{% else %}false{% endif %}">{{ v.tr[page.lang] | default: v.etichetta | escape }}</button>{%- endfor -%}\n</div></div>\n{%- endif -%}\n')
L = rep(L, '<div class="nz-pp-acq">', btns + '<div class="nz-pp-acq">')
js = ("<script>(function(){var s=document.querySelector('.nz-scheda');if(!s||!document.querySelector('.nz-var'))return;"
 "var base=s.getAttribute('data-base'),id=s.getAttribute('data-id-base'),pr=s.querySelector('.nz-pp-prezzo'),f;"
 "try{f=new Intl.NumberFormat(document.documentElement.lang||'it',{style:'currency',currency:'EUR'});}catch(e){f=new Intl.NumberFormat('it',{style:'currency',currency:'EUR'});}"
 "var bs=document.querySelectorAll('.nz-var');bs.forEach(function(b){b.addEventListener('click',function(){"
 "bs.forEach(function(x){x.classList.remove('on');x.setAttribute('aria-pressed','false');});b.classList.add('on');b.setAttribute('aria-pressed','true');"
 "s.dataset.id=id+'-'+b.dataset.codice;s.dataset.nome=base+' - '+b.dataset.nome;s.dataset.prezzo=b.dataset.prezzo;"
 "if(pr)pr.textContent=f.format(Number(b.dataset.prezzo)/100);});});})();</script>\n")
L = rep(L, '<p class="nz-pp-torna">', js + '<p class="nz-pp-torna">')
wr("_layouts/negozio-prodotto.html", L)

# 3) css
css = rd("assets/css/negozio.css")
if ".nz-var-lista" not in css:
    css += ("\n/* varianti prodotto (es. numero di semi) */\n.nz-var-t{margin:.8rem 0 .4rem;font-weight:600}\n.nz-var-lista{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:1rem}\n"
     ".nz-var{padding:.45rem .9rem;border:1px solid currentColor;border-radius:.4rem;background:transparent;color:inherit;cursor:pointer;font:inherit;opacity:.75}\n"
     ".nz-var:hover{opacity:1}\n.nz-var.on{background:#7a5a1e;border-color:#7a5a1e;color:#fff;opacity:1}\n")
    wr("assets/css/negozio.css", css)

# 4) catalogo: UN prodotto con varianti
P = "_data/catalogo.json"
d = json.loads(rd(P))
d["prodotti"] = [p for p in d["prodotti"] if not p["id"].startswith("semi-cipolla-giarratana")]
vs = []
for i, n in enumerate(range(50, 501, 50)):
    vs.append({"codice": str(n), "etichetta": "%d semi" % n, "prezzo_centesimi": 300 + 200 * i, "tr": {"en": "%d seeds" % n}})
d["prodotti"].insert(0, {
 "tipo": "fisico", "id": "semi-cipolla-giarratana", "nome": "Semi di cipolla di Giarratana", "categoria": "semi",
 "prezzo_centesimi": 300,
 "varianti_titolo": "Numero di semi", "varianti": vs,
 "descrizione": "Semi di cipolla di Giarratana, Presidio Slow Food del Ragusano, da seminare in semenzaio e trapiantare nel tuo orto. Scegli la quantità.",
 "descrizione_completa": "Semi di cipolla di Giarratana, Presidio Slow Food dell'altopiano ibleo, in bustine da 50 a 500 semi.\nSi semina in semenzaio da fine ottobre e si trapianta tra febbraio e marzo; la raccolta arriva in estate.\nÈ una cipolla dolce e mai pungente, dal bulbo grande.",
 "immagine": "assets/images/prodotti/semi-cipolla-giarratana-demo.svg", "icona": "\U0001F9C5", "visibile": True,
 "tr": {"en": {"nome": "Giarratana onion seeds", "varianti_titolo": "Number of seeds",
  "descrizione": "Giarratana onion seeds, a Slow Food Presidium from the Ragusa area, to sow in a seedbed and transplant into your garden. Choose the quantity.",
  "descrizione_completa": "Giarratana onion seeds, a Slow Food Presidium from the Hyblaean plateau, in packets of 50 to 500 seeds.\nSow in a seedbed from late October and transplant between February and March; harvest comes in summer.\nA sweet, never pungent onion with a large bulb."}}})
open(os.path.join(R, P), "w", encoding="utf-8", newline="\n").write(json.dumps(d, ensure_ascii=False, indent=2))
json.loads(rd(P))

# 5) pagine e foto: via le 10, dentro la 1
for f in glob.glob(os.path.join(R, "_negozio", "semi-cipolla-giarratana-*.md")) + glob.glob(os.path.join(R, "en", "negozio", "semi-cipolla-giarratana-*.md")) + glob.glob(os.path.join(R, "assets", "images", "prodotti", "semi-cipolla-giarratana-*-demo.svg")):
    os.remove(f)
wr("assets/images/prodotti/semi-cipolla-giarratana-demo.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800"><rect width="800" height="800" fill="#f3e6c8"/><text x="400" y="440" font-size="320" text-anchor="middle">\U0001F9C5</text><text x="400" y="640" font-size="48" text-anchor="middle" fill="#7a5a1e" font-family="Georgia,serif">Foto demo</text></svg>')
wr("_negozio/semi-cipolla-giarratana.md", '---\nlayout: negozio-prodotto\ntitle: "Semi di cipolla di Giarratana"\npid: semi-cipolla-giarratana\npermalink: /negozio/semi-cipolla-giarratana/\ndescription: "Semi di cipolla di Giarratana, Presidio Slow Food del Ragusano: bustine da 50 a 500 semi."\nref: shop-prod-semi-cipolla-giarratana\n---\n')
wr("en/negozio/semi-cipolla-giarratana.md", '---\nlayout: negozio-prodotto\ntitle: "Giarratana onion seeds"\npid: semi-cipolla-giarratana\npermalink: /en/shop/giarratana-onion-seeds/\ndescription: "Giarratana onion seeds, a Slow Food Presidium from the Ragusa area: packets of 50 to 500 seeds."\nlang: en\nlocale: en\nref: shop-prod-semi-cipolla-giarratana\ntr: tradotto\n---\n')
print("OK")
