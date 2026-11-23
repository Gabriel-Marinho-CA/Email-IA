"""Recortes do e-mail Pré Black (Figma 16001:8889, refeito em 09/11/2026). Rodar: python lata-fit/assets/email-preblack/_recortes.py

Fonte: export 2x do Figma (_figma/export-2x.png, render vetorial, não precisa de upscale), a imagem original do
fundo de ondas (_figma/ondas-original.jpg) e os SVGs do Figma (logo, logo do rodapé, Instagram) renderizados no Chrome com fundo
transparente. Coordenadas em 1x (600px); o export é 2x.
"""
import os, subprocess, tempfile
import numpy as np
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(D, '_figma')
P = 'lf-epb-'
E1 = Image.open(os.path.join(F, 'export-2x.png')).convert('RGB')
CHROME = next(p for p in [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                          r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'] if os.path.exists(p))


def c2(x0, y0, x1, y1):
    return E1.crop((round(x0 * 2), round(y0 * 2), round(x1 * 2), round(y1 * 2)))


def jpg(im, nome):
    im.convert('RGB').save(os.path.join(D, P + nome), quality=88, optimize=True, progressive=True)
    print(P + nome, im.size, os.path.getsize(os.path.join(D, P + nome)) // 1024, 'KB')


def png(im, nome, paleta=False):
    if paleta:
        im = im.quantize(256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG)
    im.save(os.path.join(D, P + nome), optimize=True)
    print(P + nome, im.size, os.path.getsize(os.path.join(D, P + nome)) // 1024, 'KB')


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], float)


# 1. Fundo de ondas: ladrilho que repete na vertical (período medido na imagem original), 2x (1200px).
#    O padrão (gerado pela marca) não é periódico de verdade: a emenda é um corte de custo mínimo (image quilting)
#    entre o fim do ladrilho e as linhas que antecedem o começo dele, para a quebra correr por dentro das listras.
r = Image.open(os.path.join(F, 'ondas-original.jpg')).convert('RGB')
r = r.resize((1200, round(r.height * 1200 / r.width)), Image.LANCZOS)
A = np.asarray(r).astype(float)
a0, K = 200, 120
erro, per = min((np.abs(A[a0:a0 + 300] - A[a0 + p:a0 + p + 300]).mean(), p) for p in range(560, 640))
per += per % 2
fim = A[a0 + per - K:a0 + per]
antes = A[a0 - K:a0]
custo = np.abs(fim - antes).sum(2)
acum = custo.copy()
for x in range(1, custo.shape[1]):
    prev = acum[:, x - 1]
    acum[:, x] += np.minimum(np.minimum(prev, np.r_[np.inf, prev[:-1]]), np.r_[prev[1:], np.inf])
corte = np.zeros(custo.shape[1], int)
corte[-1] = int(np.argmin(acum[:, -1]))
for x in range(custo.shape[1] - 2, -1, -1):
    y = corte[x + 1]
    cand = [yy for yy in (y - 1, y, y + 1) if 0 <= yy < K]
    corte[x] = min(cand, key=lambda yy: acum[yy, x])
yk = np.arange(K)[:, None]
wb = np.clip((yk - corte[None, :] + 3) / 6, 0, 1)[..., None]
banda = fim * (1 - wb) + antes * wb
T = np.concatenate([A[a0:a0 + per - K], banda]).round().clip(0, 255).astype(np.uint8)
tile = Image.fromarray(T)
print('ondas: período', per, 'erro médio', round(erro, 2), 'custo do corte', round(acum[corte[-1], -1] / custo.shape[1], 1),
      'cor média', '#%02x%02x%02x' % tuple(T.reshape(-1, 3).mean(0).astype(int)))
jpg(tile, 'ondas.jpg')

# 2. Foto do hero: x 16-584, y 676-1177 (logo abaixo do botão). As primeiras linhas viram o rosa chapado do cartão
#    (#f4a8c4), só onde o pixel já é quase rosa, para emendar sem marca com a seção de cima.
ROSA = hexrgb('#f4a8c4')
h = np.asarray(c2(16, 676, 584, 1177)).astype(float)
n = 40
for y in range(n):
    w = 1 - y / n
    perto = (np.abs(h[y] - ROSA).sum(1) < 30)[:, None]
    h[y] = np.where(perto, h[y] * (1 - w) + ROSA * w, h[y])
jpg(Image.fromarray(h.round().astype(np.uint8)), 'hero.jpg')

# 3. Foto da Caixa Surpresa: x 16-584, y 1577-2211.
jpg(c2(16, 1577, 584, 2211), 'caixa.jpg')

# 4. Cards dos queridinhos (270x278, raio 32): imagem = linhas 0-190 (produto + selo); o texto vai em célula com cor
#    chapada. O degradê radial do Figma é refeito pela fórmula e, de 168 a 190, vai para a cor chapada da célula.
GRAD = {1: ('#f1e4d5', '#f1dcc5'), 2: ('#faddE8', '#f6ccdc'), 3: ('#f8efc6', '#f4e59d'), 4: ('#ddebf6', '#bfe0fa')}
POS = {1: (20, 2906), 2: (310, 2906), 3: (20, 3204), 4: (310, 3204)}
S = 4
yy, xx = np.mgrid[0:556, 0:540] / 2.0
t = np.clip(np.sqrt(((xx - 135) / 135) ** 2 + ((yy - 139) / 139) ** 2), 0, 1)[..., None]
# máscara do cartão arredondado (raio 32 em 1x) com antialias por supersampling
ys, xs = (np.mgrid[0:380 * S, 0:540 * S] + 0.5) / (2 * S)
cx = np.clip(xs, 32, 270 - 32); cy = np.clip(ys, 32, 10 ** 6)
dentro = ((xs - cx) ** 2 + (ys - cy) ** 2 <= 32 ** 2).astype(float)
alfa = dentro.reshape(380, S, 540, S).mean((1, 3))
for k, (x0, y0) in POS.items():
    c0, c1 = hexrgb(GRAD[k][0]), hexrgb(GRAD[k][1])
    G = c0 + (c1 - c0) * t
    m = (yy >= 95) & (yy < 139 + 139)
    plana = G[(yy >= 190) & (yy < 278)].mean(0)
    print('card', k, 'cor da célula #%02x%02x%02x' % tuple(plana.round().astype(int)))
    C = np.asarray(c2(x0, y0, x0 + 270, y0 + 190)).astype(float)
    Gc = G[:380]
    yrow = yy[:380]
    w = np.clip((yrow - 168) / (190 - 168), 0, 1)[..., None]
    w = w * w * (3 - 2 * w)
    out = C * (1 - w) + plana * w
    borda = (alfa < 1)[..., None]
    out = np.where(borda, Gc * (1 - w) + plana * w, out)
    rgba = np.dstack([out.round().clip(0, 255), (alfa * 255).round()]).astype(np.uint8)
    png(Image.fromarray(rgba, 'RGBA'), f'card-{k}.png', paleta=True)

# 5. Ícones do "Encontre o seu favorito": círculos 64px (#f3a7c4) em x 64/200/336/472, y 3758. Alfa = círculo
#    redesenhado; o anel de antialias recebe a cor chapada do círculo.
CIR = hexrgb('#f3a7c4')
ys, xs = (np.mgrid[0:128 * S, 0:128 * S] + 0.5) / S
ac = ((xs - 64) ** 2 + (ys - 64) ** 2 <= 64 ** 2).astype(float).reshape(128, S, 128, S).mean((1, 3))
for i, x in enumerate([64, 200, 336, 472], 1):
    C = np.asarray(c2(x, 3758, x + 64, 3822)).astype(float)
    C = np.where((ac < 1)[..., None], CIR, C)
    png(Image.fromarray(np.dstack([C.round(), (ac * 255).round()]).astype(np.uint8), 'RGBA'), f'icone-{i}.png')

# 6. SVGs do Figma (logo #cc3c53, logo do rodapé e Instagram #f8f3e7) renderizados em 2x com fundo transparente.
def svg_png(svg, w, h, nome):
    tmp = tempfile.mkdtemp()
    html = os.path.join(tmp, 'p.html')
    with open(html, 'w', encoding='utf-8') as f:
        f.write(f"<html><body style='margin:0;background:transparent'><img src='file:///{os.path.join(F, svg).replace(os.sep, '/')}' "
                f"style='display:block;width:{w * 2}px;height:{h * 2}px'></body></html>")
    shot = os.path.join(tmp, 's.png')
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    '--default-background-color=00000000', '--window-size=800,400', f'--screenshot={shot}',
                    'file:///' + html.replace(os.sep, '/')], capture_output=True)
    png(Image.open(shot).convert('RGBA').crop((0, 0, w * 2, h * 2)), nome)


svg_png('svg_11.svg', 106, 32, 'logo.png')
svg_png('svg_18.svg', 211, 64, 'logo-rodape.png')
svg_png('svg_04.svg', 48, 48, 'instagram.png')
