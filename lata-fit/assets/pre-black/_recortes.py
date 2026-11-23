"""Recortes do e-mail Latam Fit — Pré Black (prefixo lf-pb-).

    python lata-fit/assets/pre-black/_recortes.py

_layout.png é o PNG do layout inteiro (600x2727), com a moldura xadrez azul/creme em volta do cartão.
Como no lançamento Goiabinha, o e-mail é só o cartão: x 13-587 / y 12-2705 (575px) em _card.png,
escalado para 600px em _design.png. _design-2x.png = Real-ESRGAN 4x do _card.png reduzido para 1200px.
Coordenadas abaixo: 1x do _design.png (x2 no 2x).

O logo do hero sai do original da loja (_fontes/logo-latam-fit.png), encaixado por template matching.
"""
import os
import cv2
import numpy as np
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
P = 'lf-pb-'
D1 = Image.open(os.path.join(D, '_design.png')).convert('RGB')
D2 = Image.open(os.path.join(D, '_design-2x.png')).convert('RGB')
A1 = np.asarray(D1).astype(np.float32)
A2 = np.asarray(D2).astype(np.float32)

TOPO = np.array([0xf2, 0xf2, 0xf2], np.float32)   # fundo do hero
SEC = np.array([0xf9, 0xfa, 0xf9], np.float32)    # fundo do cartão
BRANCO = np.array([255, 255, 255], np.float32)    # card dos ícones
MARROM = np.array([0x6e, 0x2e, 0x1e], np.float32) # títulos e ícones
LOGO = (0xbf, 0x45, 0x23)


def jpg(a, name):
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(
        os.path.join(D, P + name), quality=88, optimize=True, progressive=True)
    print(P + name, a.shape[1], 'x', a.shape[0], os.path.getsize(os.path.join(D, P + name)) // 1024, 'KB')


def png8(im, name, cores=256):
    """PNG com alfa em paleta (foto com transparência fica 4-5x menor que PNG cheio)."""
    q = im.quantize(cores, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
    q.save(os.path.join(D, P + name), optimize=True)
    print(P + name, im.size, os.path.getsize(os.path.join(D, P + name)) // 1024, 'KB')


def snap(a, bg, tol):
    """Pixels quase iguais ao fundo viram exatamente o fundo (o upscale deixa ruído e caixas claras)."""
    m = np.abs(a - bg).max(2) < tol
    a[m] = bg
    return a


# ---------------------------------------------------------------- hero: barrinhas dos cantos, selo "PRÉ", logo, "BLACK"
H_TOPO = 232
topo = snap(A2[:H_TOPO * 2].copy(), TOPO, 12)
# cantos arredondados do cartão (aparecia a moldura): o topo do e-mail fica reto
ys, xs = np.mgrid[0:40, 0:40]
fora = (xs - 40) ** 2 + (ys - 40) ** 2 > 36 ** 2
CREME = np.array([0xfa, 0xf6, 0xec], np.float32)
for sl in (np.s_[:40, :40], np.s_[:40, -40:]):
    bloco = topo[sl]
    f = fora if sl[1].start is None else fora[:, ::-1]
    azul = (bloco[..., 2] - bloco[..., 0]) > 15
    creme = np.abs(bloco - CREME).max(2) < 14
    bloco[f & (azul | creme)] = TOPO

# logo: acha posição/escala do original contra o layout e cola o original recolorido
logo = Image.open(os.path.join(D, '_fontes', 'logo-latam-fit.png')).convert('RGBA')
logo = logo.crop(logo.getchannel('A').getbbox())
reg = cv2.cvtColor(A2[150:260, 500:820].astype(np.uint8), cv2.COLOR_RGB2GRAY)
best = None
for w in range(230, 270, 1):
    h = round(w * logo.height / logo.width)
    alfa = np.asarray(logo.getchannel('A').resize((w, h), Image.LANCZOS)).astype(np.float32) / 255
    tpl = (255 - alfa * (255 - 110)).astype(np.uint8)   # logo vermelho fica ~110 em cinza
    r = cv2.matchTemplate(reg, tpl, cv2.TM_SQDIFF_NORMED)
    v, _, p, _ = cv2.minMaxLoc(r)
    if best is None or v < best[0]:
        best = (v, w, h, p)
v, lw, lh, (lx, ly) = best
lx, ly = lx + 500, ly + 150
print('logo', lw, 'x', lh, 'em', lx, ly, 'erro', round(v, 4))
topo[ly - 6:ly + lh + 6, lx - 6:lx + lw + 6] = TOPO
alfa = np.asarray(logo.getchannel('A').resize((lw, lh), Image.LANCZOS)).astype(np.float32)[..., None] / 255
topo[ly:ly + lh, lx:lx + lw] = topo[ly:ly + lh, lx:lx + lw] * (1 - alfa) + np.array(LOGO, np.float32) * alfa
jpg(topo, 'hero-topo.jpg')                                    # 1x 600x232

# ---------------------------------------------------------------- produtos com o selo "30% OFF" (1x 400-880, a sombra vai até a caixa do cupom)
Y0, Y1 = 400, 880
prod = A2[Y0 * 2:Y1 * 2].copy()
# fundo é um degradê #f2f2f2 -> #f9faf9; acerta linha a linha para emendar sem marca com as seções lisas
claro = (prod.min(2) > 236) & (np.ptp(prod, axis=2) < 6)
est = np.array([np.median(prod[y][claro[y]], axis=0) if claro[y].sum() > 50 else [np.nan] * 3
                for y in range(prod.shape[0])])
idx = np.arange(len(est))
for c in range(3):
    ok = ~np.isnan(est[:, c])
    est[:, c] = np.interp(idx, idx[ok], est[ok, c])
est = cv2.GaussianBlur(est.astype(np.float32)[:, None, :], (1, 0), sigmaX=0.1, sigmaY=25)[:, 0, :]
t = np.clip(idx / (len(idx) - 1), 0, 1)[:, None]
alvo = est.copy()
alvo[:120] = TOPO + (est[120] - TOPO) * (idx[:120, None] / 120)           # topo exato #f2f2f2
alvo[-120:] = est[-121] + (SEC - est[-121]) * ((idx[-120:, None] - idx[-121]) / 120)  # base exata #f9faf9
prod += (alvo - est)[:, None, :]
lin = np.abs(prod - alvo[:, None, :]).max(2) < 4
prod[lin] = np.broadcast_to(alvo[:, None, :], prod.shape)[lin]
jpg(prod, 'produtos.jpg')                                     # 1x 600x462


# ---------------------------------------------------------------- pilhas de barrinhas: PNG com alfa (modo escuro)
def recorte_alfa(x0, y0, x1, y1, nome):
    """Fundo liso #f9faf9 vira transparente. Máscara do fundo pelo 1x (fundo exato), borda pelo 2x."""
    d1 = np.abs(A1[y0:y1, x0:x1] - SEC).max(2)
    m = (d1 <= 3).astype(np.uint8)
    n, lab = cv2.connectedComponents(m, connectivity=4)
    borda = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fundo1 = np.isin(lab, list(borda)) & (m > 0)
    fundo2 = cv2.resize(fundo1.astype(np.uint8), None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
    certo_fundo = cv2.erode(fundo2, np.ones((3, 3), np.uint8)) > 0
    certo_prod = cv2.erode(1 - fundo2, np.ones((5, 5), np.uint8)) > 0
    rgb = A2[y0 * 2:y1 * 2, x0 * 2:x1 * 2].copy()
    d2 = np.abs(rgb - SEC).max(2)
    a = np.clip((d2 - 3) / 28, 0, 1)
    a[certo_fundo] = 0
    a[certo_prod] = 1
    # cor sem o fundo misturado na borda: c = (p - (1-a)·fundo) / a
    am = np.maximum(a, 1e-3)[..., None]
    cor = np.clip((rgb - (1 - am) * SEC) / am, 0, 255)
    cor[a == 0] = 0
    im = Image.fromarray(np.dstack([cor, a * 255]).astype(np.uint8), 'RGBA')
    png8(im, nome)


recorte_alfa(337, 1400, 600, 1832, 'caixas-mistas.png')     # 1x 263x432, coluna da direita
recorte_alfa(0, 1892, 254, 2312, 'combo.png')               # 1x 254x420, coluna da esquerda


# ---------------------------------------------------------------- ícones do card branco: traço marrom desmisturado do branco
def icone(cx, nome, y0=1221, w=64, h=56):
    x0 = round((cx - w / 2) * 2)
    reg = A2[y0 * 2:(y0 + h) * 2, x0:x0 + w * 2]
    v = BRANCO - MARROM
    a = np.clip(((BRANCO - reg) @ v) / (v @ v), 0, 1)
    a[a < 0.03] = 0
    im = np.zeros(reg.shape[:2] + (4,), np.uint8)
    im[..., :3] = MARROM.astype(np.uint8)
    im[..., 3] = (a * 255).astype(np.uint8)
    Image.fromarray(im, 'RGBA').save(os.path.join(D, P + nome), optimize=True)
    print(P + nome, (w * 2, h * 2))


for i, cx in enumerate((145, 257, 362, 463), 1):            # 1x 64x56, centro = centro do rótulo
    icone(cx, f'icone-{i}.png')
