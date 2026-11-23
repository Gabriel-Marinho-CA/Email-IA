"""Imagens do e-mail Latam Fit: carrinho abandonado (prefixo lf-ca-).

    python -I lata-fit/assets/carrinho-abandonado/_recortes.py

Sem layout do Figma: as imagens são geradas aqui, na identidade verde do Goiabinha.
Barrinhas = packshots originais da loja (_fontes/, com alfa). Coordenadas em 2x (exibição = metade).
Fundo = degradê só vertical, cortado em três peças que emendam sem marca (o corte horizontal do
background "cover" no celular não muda a cor da emenda).
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

D = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(D, '_fontes')
P = 'lf-ca-'

W = 1200
H_FUNDO = 672                  # 1x 336: seção com logo, título e parágrafo
H_PROD = 572                   # 1x 286: barrinhas
H_BORDA = 38                   # 1x 19: topo arredondado do cartão bege
H = H_FUNDO + H_PROD + H_BORDA
CARD_X0, CARD_X1, CARD_R = 34, 1168, 28   # igual ao cartão do Goiabinha

STOPS = [(0.00, (0xc4, 0xdd, 0x9b)), (0.52, (0xc6, 0xdf, 0x9c)), (1.00, (0xd5, 0xee, 0xac))]


def degrade():
    t = np.linspace(0, 1, H)
    col = np.stack([np.interp(t, [s[0] for s in STOPS], [s[1][c] for s in STOPS]) for c in range(3)], 1)
    return np.repeat(col[:, None, :], W, 1).astype(np.float32)


def barra(nome, indice=1):
    """Uma barrinha do packshot (as fotos da loja têm 2 ou 3 lado a lado)."""
    im = Image.open(os.path.join(F, nome + '.png')).convert('RGBA')
    a = np.asarray(im.getchannel('A')) > 128
    cols = a.any(0)
    runs, ini = [], None
    for x, v in enumerate(cols):
        if v and ini is None:
            ini = x
        if not v and ini is not None:
            if x - ini > 40:
                runs.append((ini, x))
            ini = None
    if ini is not None:
        runs.append((ini, len(cols)))
    x0, x1 = runs[min(indice, len(runs) - 1)]
    b = im.crop((x0, 0, x1, im.height))
    return b.crop(b.getchannel('A').getbbox())


# nome, cx, cy, rotação (positivo = topo para a esquerda), altura em 2x. Ordem = de trás para a frente.
BARRAS = [
    ('banana-amendoim', 196, 292, 27, 446),
    ('wafer-cookies', 1004, 292, -27, 446),
    ('cocada-choco', 394, 270, 13, 484),
    ('goiabinha-zero', 806, 270, -13, 484),
    ('wafer-morango', 600, 270, 0, 516),
]


def compoe(base):
    """Cola as barrinhas com sombra suave. base = RGB do trecho das barrinhas."""
    out = base.convert('RGBA')
    for nome, cx, cy, rot, alt in BARRAS:
        b = barra(nome)
        larg = round(b.width * alt / b.height)
        b = b.resize((larg, alt), Image.LANCZOS)
        if rot:
            b = b.rotate(rot, expand=True, resample=Image.BICUBIC)
        x, y = cx - b.width // 2, cy - b.height // 2
        camada = Image.new('L', out.size, 0)
        camada.paste(b.getchannel('A'), (x + 6, y + 16))
        camada = camada.filter(ImageFilter.GaussianBlur(16)).point(lambda v: int(v * 0.34))
        out.paste(Image.new('RGBA', out.size, (0x4e, 0x74, 0x2c, 255)), (0, 0), camada)
        out.alpha_composite(b, (max(x, 0), max(y, 0)), (max(-x, 0), max(-y, 0)))
    return out.convert('RGB')


def rrect_mask(size, box, r, ss=4):
    w, h = size
    m = Image.new('L', (w * ss, h * ss), 0)
    x0, y0, x1, y1 = [v * ss for v in box]
    ImageDraw.Draw(m).rounded_rectangle((x0, y0, x1 - 1, y1 - 1), r * ss, fill=255)
    return m.resize(size, Image.LANCZOS)


def jpg(im, nome):
    caminho = os.path.join(D, P + nome)
    im.convert('RGB').save(caminho, quality=88, optimize=True, progressive=True)
    print(P + nome, im.size, os.path.getsize(caminho) // 1024, 'KB')


def png(im, nome):
    caminho = os.path.join(D, P + nome)
    im.save(caminho, optimize=True)
    print(P + nome, im.size, os.path.getsize(caminho) // 1024, 'KB')


g = degrade()
ruido = np.random.default_rng(1).normal(0, 0.9, g.shape)
com_ruido = Image.fromarray(np.clip(g + ruido, 0, 255).astype(np.uint8))

jpg(com_ruido.crop((0, 0, W, H_FUNDO)), 'hero-fundo.jpg')
jpg(compoe(com_ruido.crop((0, H_FUNDO, W, H_FUNDO + H_PROD))), 'hero-produtos.jpg')

borda = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).crop((0, H - H_BORDA, W, H)).convert('RGBA')
m = rrect_mask((W, H_BORDA * 2), (CARD_X0, 0, CARD_X1, H_BORDA * 2), CARD_R).crop((0, 0, W, H_BORDA))
borda.putalpha(Image.eval(m, lambda v: 255 - v))
png(borda, 'hero-borda.png')
