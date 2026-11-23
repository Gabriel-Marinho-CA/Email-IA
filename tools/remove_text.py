"""Apaga texto claro de cima de um fundo liso (céu, degradê) e opcionalmente extrai um trecho
do texto como PNG transparente.

    python tools/remove_text.py hero-2x.png hero-limpo.png --faixa 0 760 --ate 620
    python tools/remove_text.py hero-2x.png hero-limpo.png --faixa 0 760 --ate 620 \
        --extrair 414 540 de-conhecer.png

--faixa Y0 Y1   região (em px da imagem) onde o fundo é reconstruído
--ate Y         nenhum texto abaixo desta linha (protege o produto/foto)
--extrair Y0 Y1 ARQ   recorta as linhas Y0-Y1 do texto como PNG com alfa

Por que não cv2.inpaint: texto de design costuma ter glow suave em volta. O inpaint deixa manchas
fantasmas. Aqui o fundo fora do texto é ajustado por um polinômio 2D (grau 4), que reproduz
degradê perfeitamente, e entra só dentro de um halo largo em volta do texto, com borda suave.
Funciona para fundo LISO. Para fundo com textura/foto, use IA (ChatGPT/Figma) em vez disto.
"""
import argparse
import cv2, numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('dst')
ap.add_argument('--faixa', nargs=2, type=int, required=True)
ap.add_argument('--ate', type=int)
ap.add_argument('--extrair', nargs=3)
a = ap.parse_args()

img = np.array(Image.open(a.src).convert('RGB')).astype(np.float32)
Y0, Y1 = a.faixa
W = img.shape[1]
reg = img[Y0:Y1].astype(np.int16)
r, g, b = reg[..., 0], reg[..., 1], reg[..., 2]
# texto = pixels claros/amarelados sobre azul. Ajuste esta regra para outras cores de fundo.
mask = ((((r > 110) & (g > 150)) | (r - b > -40)).astype(np.uint8) * 255)
if a.ate is not None:
    mask[max(a.ate - Y0, 0):] = 0
mask = cv2.dilate(mask, np.ones((7, 7), np.uint8), iterations=2)
halo = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=28)  # engloba o glow

h = Y1 - Y0
yy, xx = np.mgrid[0:h, 0:W]
xn, yn = xx / W, yy / h
A = np.stack([(xn ** i * yn ** j).ravel() for i in range(5) for j in range(5 - i)], 1)
keep = halo.ravel() == 0
fit = np.empty((h, W, 3), np.float32)
for c in range(3):
    coef, *_ = np.linalg.lstsq(A[keep], img[Y0:Y1, :, c].ravel()[keep], rcond=None)
    fit[..., c] = (A @ coef).reshape(h, W)
fit += np.random.default_rng(1).normal(0, 1.2, fit.shape)  # grão, senão fica plástico
soft = np.clip(cv2.GaussianBlur(halo, (0, 0), 18)[..., None] / 255.0 * 1.6, 0, 1)
clean = img.copy()
clean[Y0:Y1] = img[Y0:Y1] * (1 - soft) + fit * soft
clean = np.clip(clean, 0, 255).astype(np.uint8)
Image.fromarray(clean).save(a.dst)
print('fundo limpo ->', a.dst)

if a.extrair:
    e0, e1, out = int(a.extrair[0]), int(a.extrair[1]), a.extrair[2]
    o, bg = img[e0:e1], clean[e0:e1].astype(np.float32)
    d = np.linalg.norm(o - bg, axis=2)
    color = o[d > np.percentile(d, 99.3)].mean(axis=0)
    # alfa = quanto cada pixel "andou" do fundo em direção à cor do texto
    alpha = np.clip(np.sum((o - bg) * (color - bg), axis=2) /
                    np.maximum(np.sum((color - bg) ** 2, axis=2), 1), 0, 1)
    alpha[alpha < 0.08] = 0
    ys, xs = np.nonzero(alpha > 0.15)
    x0, x1, t0, t1 = max(xs.min() - 4, 0), xs.max() + 5, max(ys.min() - 4, 0), ys.max() + 5
    rgba = np.zeros((t1 - t0, x1 - x0, 4), np.uint8)
    rgba[..., :3] = np.clip(color, 0, 255).astype(np.uint8)
    rgba[..., 3] = (alpha[t0:t1, x0:x1] * 255).astype(np.uint8)
    Image.fromarray(rgba).save(out)
    print('texto ->', out, 'cor', color.round(), 'tamanho', rgba.shape[1::-1],
          'posição', (x0, e0 + t0))
