import io
import os
import sys

import cv2
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
PSD = os.path.join(AQUI, '..', 'Email 02 - Black Friday - 02 - Black Friday - Semana 02 - Brindes', 'PSD',
                   'Solicitação Email Marketing - 02 - Black Friday - Semana 02 - Brindes.psd')
P = 'joie-bfb-'

design = Image.open(os.path.join(AQUI, '_design.png')).convert('RGB')
d2 = Image.open(os.path.join(AQUI, '_design-2x.png')).convert('RGB')
limpo2 = Image.open(os.path.join(AQUI, '_limpo-2x.png')).convert('RGB')


def jpg(im, nome, q=88):
    im.save(os.path.join(AQUI, P + nome), quality=q, optimize=True, progressive=True)
    print(nome, im.size, os.path.getsize(os.path.join(AQUI, P + nome)) // 1024, 'KB')


def png(im, nome, cores=None):
    if cores:
        im = im.quantize(cores, method=Image.FASTOCTREE) if im.mode == 'RGBA' else im.quantize(cores)
    im.save(os.path.join(AQUI, P + nome), optimize=True)
    print(nome, im.size, os.path.getsize(os.path.join(AQUI, P + nome)) // 1024, 'KB')


def preto_puro(im, lim=14):
    a = np.array(im).astype(np.int16)
    a[a.max(axis=2) < lim] = 0
    return Image.fromarray(a.astype(np.uint8))


def caixa2(x0, y0, x1, y1):
    return (x0 * 2, y0 * 2, x1 * 2, y1 * 2)


# fundos e foto: camadas do PSD sem texto (_limpo.png = glow + foto + retângulo preto, ESRGAN 2x)
jpg(limpo2.crop(caixa2(0, 392, 600, 490)), 'fundo-texto.jpg')
jpg(limpo2.crop(caixa2(0, 490, 600, 934)), 'produtos.jpg')
jpg(limpo2.crop(caixa2(0, 934, 600, 1145)), 'fundo-card.jpg')

# título em Trade Gothic (não sai em texto de e-mail) e faixa girada: do 2x do layout
png(preto_puro(d2.crop(caixa2(120, 210, 480, 360))), 'titulo.png', 128)
jpg(preto_puro(d2.crop(caixa2(0, 1838, 600, 1958))), 'faixa.jpg', 92)

# brindes: smart objects do PSD (1080px, fundo transparente), na posição do layout
sys.path.insert(0, os.environ.get('PSDLIB', ''))
from psd_tools import PSDImage  # noqa: E402

psd = PSDImage.open(PSD)
quadro = list(psd)[0]
brindes = {
    'Design sem nome (10)': ('melatonina.png', 33, 1182),
    'Design sem nome (11)': ('hepro.png', 308, 1182),
    'Design sem nome (12)': ('propolis.png', 33, 1444),
    'Design sem nome (13)': ('kit-serum.png', 308, 1444),
}
CW, CY0, CY1 = 140, 54, 200
for camada in quadro:
    if camada.name not in brindes:
        continue
    nome, cx, cy = brindes[camada.name]
    src = Image.open(io.BytesIO(camada.smart_object.data)).convert('RGBA')
    src = src.crop(src.getchannel('A').getbbox())
    x0, y0, x1, y1 = camada.bbox
    prod = src.resize(((x1 - x0) * 2, (y1 - y0) * 2), Image.LANCZOS)
    cl = cx + 130 - CW // 2
    tela = Image.new('RGBA', (CW * 2, (CY1 - CY0) * 2), (0, 0, 0, 0))
    tela.alpha_composite(prod, ((x0 - cl) * 2, (y0 - cy - CY0) * 2))
    png(tela, nome, 256)

# logo: o joie-bfa-logo.png do e-mail 01 tem o verde #a5de00 (convertido do Adobe RGB); este layout usa #bfe132
png(preto_puro(d2.crop(caixa2(208, 88, 392, 174))), 'logo.png', 128)
