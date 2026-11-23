"""Mede um design: cor de fundo e faixas de conteúdo (linhas que diferem do fundo).

    python tools/medir.py "d:/Downloads/design.png"
    python tools/medir.py design.png --lim 40 --fundo 5 5

Imprime o tamanho, a cor de fundo (hex) e, para cada faixa, as linhas y0-y1, as colunas x0-x1
ocupadas e a altura. É daqui que saem as coordenadas dos recortes (no 1x; no 2x, multiplique por 2).

--lim N       diferença mínima (soma RGB) para contar como conteúdo. Padrão 30. Suba se o fundo
              tiver ruído de JPG ou degradê leve.
--fundo X Y   pixel usado como cor de fundo. Padrão 5 5.
"""
import argparse
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('design')
ap.add_argument('--lim', type=int, default=30)
ap.add_argument('--fundo', nargs=2, type=int, default=(5, 5))
a = ap.parse_args()

im = np.asarray(Image.open(a.design).convert('RGB')).astype(int)
bg = im[a.fundo[1], a.fundo[0]]
print(f'{im.shape[1]}x{im.shape[0]}  fundo #{bg[0]:02x}{bg[1]:02x}{bg[2]:02x}')

diff = np.abs(im - bg).sum(2) > a.lim
start = None
for y, v in enumerate(list(diff.any(1)) + [False]):
    if v and start is None:
        start = y
    elif not v and start is not None:
        xs = np.where(diff[start:y].any(0))[0]
        print(f'y {start:>5}-{y - 1:<5} x {xs.min():>3}-{xs.max():<3} altura {y - start}')
        start = None
