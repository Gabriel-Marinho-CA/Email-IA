"""Renderiza um template (desktop + mobile) e monta comparação lado a lado com o design.

    python tools/render.py lata-fit/lancamento-goiabinha.mjml lata-fit/assets/lancamento-goiabinha "design.png"
    python tools/render.py pep/boas-vindas.html pep/assets/boas-vindas "d:/Downloads/design.png"

Saída em tools/_render/: desktop.png, mobile.png, comparacao.png (design | desktop | mobile).

- .mjml: valida e compila com `npx mjml@4.15.3` (precisa de Node) e grava o .html ao lado, que é o
  preview / e-mail de teste. Erro de validação para o script.
- Troca as URLs do CDN pelos arquivos locais: imagem remota às vezes não carrega a tempo no
  headless e o print sai cortado (parece bug de layout, não é).
- Janela de 800px: com 600px a barra de rolagem faz a media query de mobile disparar.
- Mobile é um iframe de 375px dentro de janela larga (headless tem largura mínima).
- Remove comentários {{!-- --}} e troca {{variavel}} pelo nome, só para o preview.
"""
import os, re, subprocess, sys, time
from PIL import Image

html, assets = sys.argv[1], os.path.abspath(sys.argv[2]).replace('\\', '/')
design = sys.argv[3] if len(sys.argv) > 3 else None
out = os.path.abspath(os.environ.get('RENDER_OUT') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '_render'))
os.makedirs(out, exist_ok=True)
CHROME = next(p for p in [r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                          r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'] if os.path.exists(p))

if html.endswith('.mjml'):
    mjml = ['npx', '-y', 'mjml@4.15.3']
    r = subprocess.run(mjml + ['--validate', html], capture_output=True, text=True, shell=True)
    if r.returncode or r.stdout.strip() or r.stderr.strip():
        sys.exit(f'MJML inválido:\n{r.stdout}{r.stderr}')
    compilado = html[:-5] + '.html'
    subprocess.run(mjml + [html, '-o', compilado], check=True, shell=True)
    html = compilado
    print('compilado ->', compilado)

s = open(html, encoding='utf-8').read()
s = re.sub(r'https://cdn\.shopify\.com/s/files/[^"\')]+?/files/', f'file:///{assets}/', s)
s = re.sub(r'\{\{!--.*?--\}\}', '', s, flags=re.S)
s = re.sub(r'\{\{\s*([\w.]+)\s*\}\}', r'[\1]', s)
open(os.path.join(out, 'prev.html'), 'w', encoding='utf-8').write(s)

H = int(os.environ.get('RENDER_H', 0)) or (max(2400, Image.open(design).height + 300) if design else 2400)
HM = H + 200 if 'RENDER_H' not in os.environ else int(H * 1.6)
open(os.path.join(out, 'mob.html'), 'w', encoding='utf-8').write(
    "<html><body style='margin:0;background:#ccc'><iframe src='prev.html' "
    f"style='width:375px;height:{max(3200, HM)}px;border:0;display:block;margin:0 auto'></iframe></body></html>")


def shot(page, png, h):
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                    f'--window-size=800,{h}', f'--screenshot={os.path.join(out, png)}',
                    'file:///' + os.path.join(out, page).replace('\\', '/')], capture_output=True)


shot('prev.html', 'desktop.png', H)
shot('mob.html', 'mobile.png', HM)
time.sleep(1)
d = Image.open(os.path.join(out, 'desktop.png')).crop((100, 0, 700, H))
m = Image.open(os.path.join(out, 'mobile.png')).crop((212, 0, 588, HM))
parts = ([Image.open(design).convert('RGB')] if design else []) + [d, m]
cmp = Image.new('RGB', (sum(p.width for p in parts) + 10 * len(parts), max(p.height for p in parts)), 'white')
x = 0
for p in parts:
    cmp.paste(p, (x, 0)); x += p.width + 10
cmp.save(os.path.join(out, 'comparacao.png'))
print(os.path.join(out, 'comparacao.png'))
