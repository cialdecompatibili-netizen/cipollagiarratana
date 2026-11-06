# GUIDA-SVILUPPO: logo CIPOLLA DI GIARRATANA (bulbo bianco schiacciato con meridiani, collo e due foglie) sui colori di _data/tema.json.
# Uso dalla radice: python automation/logo_cipolla.py   -> scrive favicon.svg, favicon-32/192/512.png, logo-72.png, apple-touch-icon.png, favicon.ico (assets/images e radice).
import json, math, os
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, 'assets', 'images')
def hx(s): s = s.lstrip('#'); return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
def mix(a, b, t): return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
def h(c): return '#%02x%02x%02x' % c
tema = json.load(open(os.path.join(ROOT, '_data', 'tema.json'), encoding='utf-8'))
acc, dark = hx(tema.get('accent', '#8a5a00')), hx(tema.get('accent_dark', '#4a3000'))
TOP = mix(acc, (255, 255, 255), .10); BOT = mix(dark, acc, .20)
C1, C2 = (253, 249, 238), (232, 219, 188)      # bulbo: alto / basso
LINE = (214, 198, 160); ROOT_C = (205, 190, 152)
G1, G2 = (122, 168, 74), (84, 132, 52)          # foglie
CX, CY, RX, RY = 32.0, 38.0, 21.5, 15.5
def ell(n=96): return [(CX + RX * math.cos(2 * math.pi * i / n), CY + RY * math.sin(2 * math.pi * i / n)) for i in range(n)]
def meridiano(k, n=40): return [(CX + k * RX * math.sin(math.pi * i / n), CY - RY * math.cos(math.pi * i / n)) for i in range(n + 1)]
def foglia(bx, by, ang, ln, w, n=24):
    a = math.radians(ang); dx, dy = math.sin(a), -math.cos(a); px, py = -dy, dx; pts = []
    for i in range(n + 1):
        t = i / n; off = w * math.sin(math.pi * t) * (1 - .25 * t); pts.append((bx + dx * ln * t + px * off, by + dy * ln * t + py * off))
    for i in range(n, -1, -1):
        t = i / n; off = w * math.sin(math.pi * t) * (1 - .25 * t); pts.append((bx + dx * ln * t - px * off, by + dy * ln * t - py * off))
    return pts
BULBO = ell(); COLLO = [(27.2, 27), (29.6, 15.5), (34.4, 15.5), (36.8, 27)]
LEAVES = [foglia(31, 17.5, -32, 14.5, 2.6), foglia(33, 17.5, 32, 14.5, 2.6)]
MERID = [meridiano(k) for k in (-.52, .52, -.8, .8)] + [[(CX, CY - RY), (CX, CY + RY)]]
RADICI = [[(32, 53), (32, 57.5)], [(28.8, 52.4), (27, 56.4)], [(35.2, 52.4), (37, 56.4)]]
def P(pts): return ' '.join('%.2f,%.2f' % p for p in pts)
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs>'
  '<linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
  '<linearGradient id="b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
  '<rect width="64" height="64" rx="14" fill="url(#s)"/>' % (h(TOP), h(BOT), h(C1), h(C2)))
for l in LEAVES: svg += '<polygon points="%s" fill="%s"/>' % (P(l), h(G1))
for r in RADICI: svg += '<polyline points="%s" fill="none" stroke="%s" stroke-width="1.3" stroke-linecap="round"/>' % (P(r), h(ROOT_C))
svg += '<polygon points="%s" fill="%s"/><polygon points="%s" fill="url(#b)"/>' % (P(COLLO), h(C2), P(BULBO))
for m in MERID: svg += '<polyline points="%s" fill="none" stroke="%s" stroke-width="1" stroke-linecap="round" opacity=".85"/>' % (P(m), h(LINE))
svg += '</svg>\n'
open(os.path.join(IMG, 'favicon.svg'), 'w', encoding='utf-8', newline='\n').write(svg)
def render(N, tondo=True):
    S = 4; M = N * S; k = M / 64.0
    im = Image.new('RGBA', (M, M), (0, 0, 0, 0))
    g = Image.new('RGB', (1, M))
    for y in range(M): g.putpixel((0, y), mix(TOP, BOT, y / (M - 1)))
    mask = Image.new('L', (M, M), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, M - 1, M - 1), radius=int(M * 14 / 64) if tondo else 0, fill=255)
    im.paste(g.resize((M, M)).convert('RGBA'), (0, 0), mask)
    d = ImageDraw.Draw(im); sc = lambda pts: [(x * k, y * k) for x, y in pts]
    for l in LEAVES: d.polygon(sc(l), fill=G1 + (255,))
    for r in RADICI: d.line(sc(r), fill=ROOT_C + (255,), width=max(2, int(1.3 * k)), joint='curve')
    d.polygon(sc(COLLO), fill=C2 + (255,))
    bb = Image.new('RGBA', (M, M), (0, 0, 0, 0)); bg = Image.new('RGB', (1, M))
    for y in range(M):
        t = (y - (CY - RY) * k) / (2 * RY * k); bg.putpixel((0, y), mix(C1, C2, min(1, max(0, t))))
    bm = Image.new('L', (M, M), 0); ImageDraw.Draw(bm).polygon(sc(BULBO), fill=255)
    bb.paste(bg.resize((M, M)).convert('RGBA'), (0, 0), bm); im.alpha_composite(bb)
    d = ImageDraw.Draw(im)
    for m in MERID: d.line(sc(m), fill=LINE + (225,), width=max(1, int(1.0 * k)), joint='curve')
    return im.resize((N, N), Image.LANCZOS)
for n, name in ((32, 'favicon-32.png'), (72, 'logo-72.png'), (192, 'favicon-192.png'), (512, 'favicon-512.png')): render(n).save(os.path.join(IMG, name))
render(180, tondo=False).convert('RGB').save(os.path.join(IMG, 'apple-touch-icon.png'))
ico = render(256); ico.save(os.path.join(IMG, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)]); ico.save(os.path.join(ROOT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
print('logo cipolla scritto', h(TOP), h(BOT))
