"""Recortes do e-mail Black 17/11 (30% OFF) da Joie. Coordenadas no 1x (600x1861).

_design.png = FULL-Joie-Email03-BlackFriday.png; _design-2x.png = Real-ESRGAN.
Texto e formas que viram HTML saem dos fundos por interpolação harmônica (Laplace),
que não cria manchas nem extrapola cor.
"""
import os
import numpy as np
import cv2
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
P = 'joie-b17-'
D1 = np.asarray(Image.open(os.path.join(AQUI, '_design.png')).convert('RGB')).astype(np.float32)
D2 = np.asarray(Image.open(os.path.join(AQUI, '_design-2x.png')).convert('RGB')).astype(np.float32)
# O ESRGAN clareia os escuros (+2 a +8 níveis) e deixa contorno escuro nas bordas claras. Correção:
# soma ao 2x a diferença (1x - 2x reduzido) ampliada, para a média de cada 2x2 voltar a ser o pixel do 1x.
_h, _w = D1.shape[:2]
_res = D1 - D2.reshape(_h, 2, _w, 2, 3).mean((1, 3))
D2 = D2 + cv2.resize(_res, (_w * 2, _h * 2), interpolation=cv2.INTER_LINEAR)


def salva_jpg(arr, nome, q=88):
    Image.fromarray(np.clip(arr, 0, 255).round().astype(np.uint8)).save(
        os.path.join(AQUI, P + nome), quality=q, optimize=True, progressive=True)


def laplace(img, mask, iters=600):
    """Preenche mask (bool) com a solução de Laplace a partir da borda conhecida."""
    out = img.copy()
    known = (~mask).astype(np.float32)
    # chute inicial: convolução normalizada larga
    w = cv2.GaussianBlur(known, (0, 0), 40)
    for c in range(3):
        b = cv2.GaussianBlur(out[:, :, c] * known, (0, 0), 40)
        out[:, :, c] = np.where(mask, b / np.maximum(w, 1e-4), out[:, :, c])
    ys, xs = np.where(mask)
    if len(ys) == 0:
        return out
    y0, y1 = max(ys.min() - 1, 0), min(ys.max() + 2, img.shape[0])
    x0, x1 = max(xs.min() - 1, 0), min(xs.max() + 2, img.shape[1])
    sub = out[y0:y1, x0:x1]
    m = mask[y0:y1, x0:x1]
    for _ in range(iters):
        p = np.pad(sub, ((1, 1), (1, 1), (0, 0)), mode='edge')
        avg = (p[:-2, 1:-1] + p[2:, 1:-1] + p[1:-1, :-2] + p[1:-1, 2:]) / 4
        sub[m] = avg[m]
    out[y0:y1, x0:x1] = sub
    return out


def mascara_texto(img, box, lim, dil):
    """Pixels de texto (claros) dentro de box=(x0,y0,x1,y1): canal máximo acima da mediana local + lim."""
    x0, y0, x1, y1 = box
    mx = img[y0:y1, x0:x1].max(2).astype(np.uint8)
    fundo = cv2.medianBlur(mx, 31).astype(np.float32)
    m = (mx.astype(np.float32) - fundo) > lim
    m = cv2.dilate(m.astype(np.uint8), np.ones((2 * dil + 1, 2 * dil + 1), np.uint8)) > 0
    full = np.zeros(img.shape[:2], bool)
    full[y0:y1, x0:x1] = m
    return full


def ret_arredondado(shape, x0, y0, x1, y1, r, s=1, dil=0):
    """Máscara de retângulo arredondado (coordenadas 1x inclusivas, escala s)."""
    m = np.zeros(shape, np.uint8)
    X0, Y0, X1, Y1, R = x0 * s - dil, y0 * s - dil, (x1 + 1) * s - 1 + dil, (y1 + 1) * s - 1 + dil, r * s + dil
    cv2.rectangle(m, (X0 + R, Y0), (X1 - R, Y1), 1, -1)
    cv2.rectangle(m, (X0, Y0 + R), (X1, Y1 - R), 1, -1)
    for cx, cy in ((X0 + R, Y0 + R), (X1 - R, Y0 + R), (X0 + R, Y1 - R), (X1 - R, Y1 - R)):
        cv2.circle(m, (cx, cy), R, 1, -1)
    return m > 0


def retangulo(shape, x0, y0, x1, y1, s=2):
    """Retângulo (coordenadas 1x inclusivas) na escala s. O ESRGAN deixa um contorno escuro em volta
    das letras: apagar o bloco de texto inteiro limpa o contorno junto (o fundo ali é liso)."""
    m = np.zeros(shape, bool)
    m[y0 * s:(y1 + 1) * s, x0 * s:(x1 + 1) * s] = True
    return m


def faixa2(y0, y1):
    return D2[y0 * 2:y1 * 2].copy()


# 1) topo: logo + "TODO O SITE COM 30% OFF" + divisor, sobre a cortina (y 0-300)
salva_jpg(faixa2(0, 300), 'topo.jpg')

# 2) fundo do parágrafo + cards de brinde (y 300-616): sem texto e sem os cards
f = faixa2(300, 616)
m = retangulo(f.shape[:2], 136, 312 - 300, 464, 364 - 300)  # parágrafo (y 319-358, x 143-456)
for cx in (112, 312):                                      # cards x 112-287 / 312-487, y 395-611
    m |= ret_arredondado(f.shape[:2], cx, 395 - 300, cx + 175, 611 - 300, 12, 2, dil=4)
salva_jpg(laplace(f, m, 1500), 'fundo-brindes.jpg')

# 3) corpo dos cards (abaixo do cabeçalho verde, acima da legenda): y 446-571
salva_jpg(D2[446 * 2:572 * 2, 112 * 2:288 * 2], 'robo.jpg', 90)
salva_jpg(D2[446 * 2:572 * 2, 312 * 2:488 * 2], 'relogio.jpg', 90)

# 4) base dos cards (y 572-611), sem a legenda: background do <td> da legenda, em 1x
for nome, cx in (('base-1.jpg', 112), ('base-2.jpg', 312)):
    b = D1[572:612, cx:cx + 176].copy()
    mb = mascara_texto(b, (6, 2, 170, 26), 22, 1)
    salva_jpg(laplace(b, mb, 400), nome, 92)

# 5) produtos (y 616-890)
salva_jpg(faixa2(616, 890), 'produtos.jpg')

# 6) fundo do 1º botão (y 890-1041): sem o botão (x 151-449, y 900-962, raio 16)
f = faixa2(890, 1042)
m = ret_arredondado(f.shape[:2], 151, 900 - 890, 449, 962 - 890, 16, 2, dil=6)
salva_jpg(laplace(f, m, 1500), 'fundo-botao.jpg')

# 7) topo do card "E você também aproveita" (y 1072-1267): título em Trade Gothic
salva_jpg(faixa2(1072, 1268), 'aproveita.jpg')

# 8) fundo do corpo do card (y 1268-1472): brilho nas margens, miolo coberto pela coluna
salva_jpg(faixa2(1268, 1473), 'fundo-card.jpg')

# 9) fundo final (y 1473-1860): sem parágrafo, botão e "Brindes enquanto..."
f = faixa2(1473, 1861)
o = 1473
m = retangulo(f.shape[:2], 110, 1538 - o, 490, 1631 - o)    # parágrafo (y 1545-1625)
m |= retangulo(f.shape[:2], 150, 1729 - o, 450, 1754 - o)   # "Brindes enquanto..." (y 1735-1748)
m |= ret_arredondado(f.shape[:2], 151, 1651 - o, 449, 1713 - o, 16, 2, dil=6)
salva_jpg(laplace(f, m, 1500), 'fundo-final.jpg')

for n in sorted(os.listdir(AQUI)):
    if n.startswith(P):
        im = Image.open(os.path.join(AQUI, n))
        print(n, im.size, os.path.getsize(os.path.join(AQUI, n)) // 1024, 'KB')
