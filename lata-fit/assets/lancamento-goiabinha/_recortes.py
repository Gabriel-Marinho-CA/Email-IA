"""Recortes do e-mail Latam Fit — lançamento Goiabinha com chocolate branco (prefixo lf-lg-).

    python lata-fit/assets/lancamento-goiabinha/_recortes.py

O PNG do layout veio com o xadrez de transparência do visualizador em volta: o e-mail de verdade é
o cartão de x 13-587 / y 5-2456 (575px). _design.png é esse cartão escalado para 600px e
_design-2x.png o mesmo em 2x (Real-ESRGAN). Coordenadas abaixo: 1x do _design.png (x2 no 2x).

Fotos de produto e logo saem dos originais da loja (_fontes/, baixados do CDN da Latam Fit), não do
print 1x: ficam nítidas em 2x. A posição/escala de cada uma é achada por template matching contra
o layout.
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(D, '_fontes')
P = 'lf-lg-'
D1 = Image.open(os.path.join(D, '_design.png')).convert('RGB')
D2 = Image.open(os.path.join(D, '_design-2x.png')).convert('RGB')
A2 = np.asarray(D2).astype(np.float32)

CARD = (0xf1, 0xf2, 0xe4)      # cartão "Por que você vai gostar"
CARD3 = (0xf1, 0xf1, 0xe3)     # cards de produto
SEC = (0xf8, 0xf5, 0xf7)       # fundo das seções 2-4
WHITE = (0xfe, 0xfd, 0xfd)     # fundo da seção do combo
GREEN = (0x64, 0x82, 0x47)     # texto, botão, rodapé
RED = (0xbf, 0x45, 0x23)       # logo do hero


def jpg(im, name):
    im.convert('RGB').save(os.path.join(D, P + name), quality=88, optimize=True, progressive=True)
    print(P + name, im.size)


def png(im, name):
    im.save(os.path.join(D, P + name), optimize=True)
    print(P + name, im.size)


def png8(im, name, cores=256):
    """PNG com alfa em paleta (foto com transparência fica 4-5x menor que PNG cheio)."""
    q = im.quantize(cores, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
    q.save(os.path.join(D, P + name), optimize=True)
    print(P + name, im.size, os.path.getsize(os.path.join(D, P + name)) // 1024, 'KB')


def rrect_mask(size, box, r, ss=4):
    """Máscara (L) de retângulo arredondado com antialias por supersampling."""
    w, h = size
    m = Image.new('L', (w * ss, h * ss), 0)
    x0, y0, x1, y1 = [v * ss for v in box]
    ImageDraw.Draw(m).rounded_rectangle((x0, y0, x1 - 1, y1 - 1), r * ss, fill=255)
    return m.resize(size, Image.LANCZOS)


def snap(im, bg, tol=12):
    """Pixels quase iguais ao fundo viram exatamente o fundo (o upscale desloca a cor)."""
    a = np.asarray(im.convert('RGB')).astype(int)
    m = np.abs(a - np.array(bg)).sum(2) < tol
    a[m] = bg
    return Image.fromarray(a.astype(np.uint8))


# ---------------------------------------------------------------- hero
# Texto (logo, título, divisor, parágrafo) sai do fundo; vira HTML por cima de hero-fundo.jpg.
H_TXT = 740                     # 2x: tudo acima disto que for texto é apagado (1x 370)
reg = A2[:H_TXT]
med = np.median(reg, axis=1, keepdims=True)
mask = (np.abs(reg - med).sum(2) > 18).astype(np.uint8) * 255
mask[:, :170] = 0
mask[:, 1030:] = 0
mask[700:, 850:] = 0            # selo "Lançamento"
mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)
halo = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=14)

FIT_H = 800
h, W = FIT_H, 1200
yy, xx = np.mgrid[0:h, 0:W]
xn, yn = xx / W, yy / h
A = np.stack([(xn ** i * yn ** j).ravel() for i in range(5) for j in range(5 - i)], 1)
keep = np.ones((h, W), bool)
keep[:H_TXT] &= halo == 0
keep[700:, 850:] = False        # selo
keep[790:, :] = False           # produto
keep = keep.ravel()
fit = np.empty((h, W, 3), np.float32)
for c in range(3):
    coef, *_ = np.linalg.lstsq(A[keep], A2[:h, :, c].ravel()[keep], rcond=None)
    fit[..., c] = (A @ coef).reshape(h, W)
fit += np.random.default_rng(1).normal(0, 1.0, fit.shape)
soft = np.zeros((h, W), np.float32)
soft[:H_TXT] = np.clip(cv2.GaussianBlur(halo, (0, 0), 6) / 255.0 * 1.8, 0, 1)
hero = A2[:1350].copy()
hero[:h] = A2[:h] * (1 - soft[..., None]) + fit * soft[..., None]
hero[:4] = hero[4]              # borda clara do export no topo
hero = Image.fromarray(np.clip(hero, 0, 255).astype(np.uint8))

# topo do cartão "Por que você vai gostar" (y 656-674) redesenhado nítido em cima do verde
card_m = rrect_mask(hero.size, (34, 1312, 1168, 1400), 28)
hero.paste(Image.new('RGB', hero.size, CARD), (0, 0), card_m)

jpg(hero.crop((0, 0, 1200, 732)), 'hero-fundo.jpg')      # 1x 600x366, fundo do <td> com texto
jpg(hero.crop((0, 732, 1200, 1350)), 'hero-produto.jpg')  # 1x 600x309

# ---------------------------------------------------------------- logos (original da loja)
logo = Image.open(os.path.join(F, 'logo-latam-fit.png')).convert('RGBA')
logo = logo.crop(logo.getchannel('A').getbbox())


def logo_cor(cor, largura):
    alt = round(largura * logo.height / logo.width / 2) * 2
    a = logo.getchannel('A').resize((largura, alt), Image.LANCZOS)
    im = Image.new('RGBA', a.size, cor + (0,))
    im.putalpha(a)
    return im


png(logo_cor(RED, 246), 'logo.png')               # 1x 123x37
png(logo_cor((255, 255, 255), 200), 'logo-branco.png')  # 1x 100x30


# ---------------------------------------------------------------- ícones
def icone(cx, cy, lado, bg, nome):
    x0, y0 = round((cx - lado / 2) * 2), round((cy - lado / 2) * 2)
    png(snap(D2.crop((x0, y0, x0 + lado * 2, y0 + lado * 2)), bg), nome)


for i, cx in enumerate((90.5, 229, 359, 495), 1):            # 1x 48x48, cartão #f1f2e4
    icone(cx, 791.5, 48, CARD, f'icone-{i}.png')
for i, cx in enumerate((173, 299, 425), 1):                   # 1x 104x104, fundo branco
    icone(cx, 2264, 104, WHITE, f'selo-{i}.png')
icone(516, 2499, 60, GREEN, 'instagram.png')                  # 1x 60x60, rodapé verde


# ---------------------------------------------------------------- template matching
def melhor(regiao, prod, escalas):
    """Acha escala e posição (no 2x) do produto RGBA dentro da região do layout."""
    best = None
    for s in escalas:
        p = prod.resize((max(1, round(prod.width * s)), max(1, round(prod.height * s))), Image.LANCZOS)
        rgb = np.asarray(p.convert('RGB')).astype(np.float32)
        a = np.asarray(p.getchannel('A')).astype(np.float32) / 255
        if rgb.shape[0] > regiao.shape[0] or rgb.shape[1] > regiao.shape[1]:
            continue
        m3 = np.repeat(a[..., None], 3, 2)
        res = cv2.matchTemplate(regiao, rgb, cv2.TM_SQDIFF, mask=m3)
        _, _, loc, _ = cv2.minMaxLoc(res)
        sc = res[loc[1], loc[0]] / m3.sum()
        if best is None or sc < best[0]:
            best = (sc, s, loc, p)
    return best


def tira_branco(im):
    """Fundo branco ligado à borda vira transparente (barra com chocolate veio em RGB)."""
    a = np.asarray(im.convert('RGB'))
    claro = (a.min(2) >= 246).astype(np.uint8)
    n, lab = cv2.connectedComponents(claro)
    borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fundo = np.isin(lab, list(borda))
    alpha = np.where(fundo, 0, 255).astype(np.uint8)
    alpha = cv2.erode(alpha, np.ones((3, 3), np.uint8))
    alpha = cv2.GaussianBlur(alpha, (0, 0), 0.8)
    out = im.convert('RGBA')
    out.putalpha(Image.fromarray(alpha))
    return out.crop(out.getchannel('A').getbbox())


def encaixa(prod, caixa, rots, larg_alvo):
    """caixa = região do layout em 1x (x0, y0, x1, y1). Devolve (produto redimensionado, x, y) no 2x."""
    x0, y0, x1, y1 = caixa
    reg1 = np.asarray(D1.crop(caixa)).astype(np.float32)
    cands = []
    for r in rots:
        p = prod.rotate(r, expand=True, resample=Image.BICUBIC) if r else prod
        p = p.crop(p.getchannel('A').getbbox())
        s0 = larg_alvo / p.width
        b = melhor(reg1, p, [s0 * f for f in np.arange(0.85, 1.16, 0.015)])
        cands.append((b[0], r, b[1], b[2], p))
    sc, r, s1, loc1, p = min(cands, key=lambda c: c[0])
    print(f'   1x: rot {r}  escala {s1:.4f}  pos ({x0 + loc1[0]}, {y0 + loc1[1]})  erro {sc:.1f}')
    reg2 = A2[y0 * 2:y1 * 2, x0 * 2:x1 * 2]
    b = melhor(reg2, p, [s1 * 2 * f for f in np.arange(0.97, 1.031, 0.005)])
    print(f'   rot {r}  escala {b[1]:.4f}  pos 2x ({x0 * 2 + b[2][0]}, {y0 * 2 + b[2][1]})  erro {b[0]:.1f}')
    return b[3], x0 * 2 + b[2][0], y0 * 2 + b[2][1]


# ---------------------------------------------------------------- cards "Time goiaba completo!"
Y0, Y1 = 1052, 1243                  # 1x
cv = Image.new('RGB', (1200, (Y1 - Y0) * 2), SEC)
cva = Image.new('RGBA', cv.size, (0, 0, 0, 0))   # mesma coisa sem o fundo da seção (modo escuro)


def cola(layer_dst, im, xy):
    camada = Image.new('RGBA', layer_dst.size, (0, 0, 0, 0))
    camada.paste(im, xy)
    layer_dst.alpha_composite(camada)


T, B = 18, 6                         # sombra interna: topo 9px, base 3px (1x)
c0, c1, c2 = np.array((0xde, 0xde, 0xd1)), np.array(CARD3), np.array((0xef, 0xef, 0xe0))
for x0, x1 in ((24, 191), (215, 383), (407, 574)):
    box = (x0 * 2, (1053 - Y0) * 2, x1 * 2, (1240 - Y0) * 2)
    h = box[3] - box[1]
    col = np.tile(c1, (h, 1)).astype(np.float32)
    t = np.arange(T) / T
    col[:T] = c0 + (c1 - c0) * (1 - (1 - t) ** 2)[:, None]
    col[h - B:] = c1 + (c2 - c1) * (np.arange(B) / B)[:, None]
    tex = Image.fromarray(np.repeat(col[:, None, :], box[2] - box[0], 1).astype(np.uint8))
    full = Image.new('RGB', cv.size, CARD3)
    full.paste(tex, box[:2])
    m = rrect_mask(cv.size, box, 26)
    cv.paste(full, (0, 0), m)
    fa = full.convert('RGBA')
    fa.putalpha(m)
    cva.alpha_composite(fa)

print('barra com chocolate')
barra_choc = tira_branco(Image.open(os.path.join(F, 'barra-chocolate.png')))
p, x, y = encaixa(barra_choc, (2, 1060, 214, 1236), (90, 270), 187)
cv.paste(p, (x, y - Y0 * 2), p)
cola(cva, p, (x, y - Y0 * 2))
print('barra zero')
barra_zero = Image.open(os.path.join(F, 'barra-zero.png')).convert('RGBA')
barra_zero = barra_zero.crop(barra_zero.getchannel('A').getbbox())
p, x, y = encaixa(barra_zero, (198, 1060, 404, 1236), (90, 270), 183)
cv.paste(p, (x, y - Y0 * 2), p)
cola(cva, p, (x, y - Y0 * 2))
print('pote')
pote = Image.open(os.path.join(F, 'pote-goiabada.png')).convert('RGBA')
pote = pote.crop(pote.getchannel('A').getbbox())
p, x, y = encaixa(pote, (405, 1062, 576, 1236), (0,), 120)
cv.paste(p, (x, y - Y0 * 2), p)
cola(cva, p, (x, y - Y0 * 2))
jpg(cv, 'produtos.jpg')              # 1x 600x191 (versão HTML antiga, uma imagem só)
for i in range(3):                   # MJML: uma imagem por coluna (x 0-200, 200-400, 400-600), 1x 200x191
    jpg(cv.crop((i * 400, 0, i * 400 + 400, cv.height)), f'card-{i + 1}.jpg')
    png8(cva.crop((i * 400, 0, i * 400 + 400, cv.height)), f'card-{i + 1}-v2.png')

# ---------------------------------------------------------------- combo
print('combo')
combo = Image.open(os.path.join(F, 'combo-goiabada.png')).convert('RGBA')
combo = combo.crop(combo.getchannel('A').getbbox())
p, x, y = encaixa(combo, (130, 1768, 500, 2200), (0,), 319)
CX0, CX1 = 120, 510                  # 1x, centro 315 como no layout
cy0, cy1 = y // 2 - 4, (y + p.height) // 2 + 4
cb = Image.new('RGB', ((CX1 - CX0) * 2, (cy1 - cy0) * 2), WHITE)
cb.paste(p, (x - CX0 * 2, y - cy0 * 2), p)
print('   combo 1x y', cy0, cy1)
jpg(cb, 'combo.jpg')

# ---------------------------------------------------------------- modo escuro (arquivos -v2)
# O Gmail no modo escuro escurece os fundos claros, mas não as imagens: todo fundo "pintado" na imagem
# vira uma caixa clara. Aqui saem as versões com fundo transparente (e o topo do cartão bege separado
# do hero, para o cartão escurecer junto com a seção).
cba = Image.new('RGBA', cb.size, (0, 0, 0, 0))
cola(cba, p, (x - CX0 * 2, y - cy0 * 2))
png8(cba, 'combo-v2.png')


def tira_fundo(im, bg, tinta):
    """Fundo liso vira transparente; o traço fica com a cor desmisturada do fundo."""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    bg, tinta = np.array(bg, np.float32), np.array(tinta, np.float32)
    alfa = np.clip(((bg - a) * (bg - tinta)).sum(2) / ((bg - tinta) ** 2).sum(), 0, 1)
    alfa[alfa < 0.05] = 0
    cor = (a - (1 - alfa[..., None]) * bg) / np.maximum(alfa[..., None], 1e-3)
    return Image.fromarray(np.dstack([np.clip(cor, 0, 255), alfa * 255]).astype(np.uint8), 'RGBA')


def circulo(im, bg):
    """Círculo chapado sobre fundo liso: alfa = círculo desenhado com antialias; borda na cor do círculo."""
    a = np.asarray(im.convert('RGB')).astype(int)
    ys, xs = np.where(np.abs(a - np.array(bg)).sum(2) >= 30)
    cx, cy = (xs.min() + xs.max() + 1) / 2, (ys.min() + ys.max() + 1) / 2
    r = (xs.max() - xs.min() + ys.max() - ys.min() + 2) / 4
    ss = 4
    m = Image.new('L', (im.width * ss, im.height * ss), 0)
    ImageDraw.Draw(m).ellipse(((cx - r) * ss, (cy - r) * ss, (cx + r) * ss, (cy + r) * ss), fill=255)
    m = np.asarray(m.resize(im.size, Image.LANCZOS))
    verde = a[(m > 250) & (a[..., 1] - a[..., 0] > 30)]
    cor = np.median(verde, axis=0)
    rgb = a.copy()
    rgb[(m > 0) & (m < 250)] = cor
    return Image.fromarray(np.dstack([rgb, m]).astype(np.uint8), 'RGBA')


def recorte(cx, cy, lado):
    x0, y0 = round((cx - lado / 2) * 2), round((cy - lado / 2) * 2)
    return D2.crop((x0, y0, x0 + lado * 2, y0 + lado * 2))


for i, cx in enumerate((90.5, 229, 359, 495), 1):
    png(circulo(recorte(cx, 791.5, 48), CARD), f'icone-{i}-v2.png')
for i, cx in enumerate((173, 299, 425), 1):
    png(tira_fundo(recorte(cx, 2264, 104), WHITE, GREEN), f'selo-{i}-v2.png')
ig = np.asarray(recorte(516, 2499, 60).convert('RGB')).astype(np.float32)
alfa = np.clip(((ig - np.array(GREEN)) / (255 - np.array(GREEN))).mean(2), 0, 1)
png(Image.fromarray(np.dstack([np.full(alfa.shape + (3,), 255), alfa * 255]).astype(np.uint8), 'RGBA'),
    'instagram-v2.png')

jpg(hero.crop((0, 732, 1200, 1312)), 'hero-produto-v2.jpg')          # 1x 366-655 (600x290)
borda = hero.crop((0, 1312, 1200, 1350)).convert('RGBA')                # 1x 656-674 (600x19)
borda.putalpha(Image.eval(card_m.crop((0, 1312, 1200, 1350)), lambda v: 255 - v))
png(borda, 'hero-borda.png')
