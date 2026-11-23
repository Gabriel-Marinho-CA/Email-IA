"""Aumenta um design exportado em 1x para 2x (retina) com Real-ESRGAN.

    python tools/upscale.py "d:/Downloads/design.png" pep/assets/boas-vindas/_design-2x.png

Roda 4x com o modelo realesrgan-x4plus (GPU via Vulkan) e reduz para 2x com Lanczos —
fica mais limpo que um 2x direto. Recorte os assets DEPOIS, a partir do 2x (coordenadas x2).
"""
import os, subprocess, sys, tempfile
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
EXE = os.path.join(HERE, 'bin', 'esrgan', 'realesrgan-ncnn-vulkan.exe')

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')  # ESRGAN não gosta de RGBA
with tempfile.TemporaryDirectory() as tmp:
    a, b = os.path.join(tmp, 'in.png'), os.path.join(tmp, 'out.png')
    im.save(a)
    subprocess.run([EXE, '-i', a, '-o', b, '-n', 'realesrgan-x4plus'], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    Image.open(b).resize((im.width * 2, im.height * 2), Image.LANCZOS).save(dst)
print(dst, (im.width * 2, im.height * 2))
