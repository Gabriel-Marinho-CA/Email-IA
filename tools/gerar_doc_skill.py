"""Gera o que vai para o ClickUp a partir de docs/emails-flash-crm.md e da skill.

    python tools/gerar_doc_skill.py

- docs/emails-flash-crm.html: o doc renderizado, com os prints embutidos. Abra no Chrome, Ctrl+A,
  Ctrl+C e cole na página do ClickUp (colar markdown cru no ClickUp não converte tabela/código).
- .claude/skills/email-flash-crm/scripts/: cópia dos scripts de tools/ (a skill anexada no ClickUp
  precisa rodar fora deste workspace). O bin do ESRGAN é copiado só localmente, não vai no zip.
- docs/email-flash-crm.zip: a skill para anexar no ClickUp. Descompactada em ~/.claude/skills/ vira
  ~/.claude/skills/email-flash-crm/SKILL.md.

Rode de novo sempre que mudar o doc, a skill ou um script de tools/.
"""
import base64, mimetypes, os, re, shutil, zipfile
import markdown

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RAIZ, 'docs')
SKILL = os.path.join(RAIZ, '.claude', 'skills', 'email-flash-crm')
SCRIPTS = ['medir.py', 'upscale.py', 'remove_text.py', 'render.py', 'upload_shopify.py']

md = open(os.path.join(DOCS, 'emails-flash-crm.md'), encoding='utf-8').read()
corpo = markdown.markdown(md, extensions=['tables', 'fenced_code', 'sane_lists'])


def embutir(m):
    caminho = os.path.normpath(os.path.join(DOCS, m.group(1)))
    tipo = mimetypes.guess_type(caminho)[0]
    dados = base64.b64encode(open(caminho, 'rb').read()).decode()
    return f'src="data:{tipo};base64,{dados}"'


corpo = re.sub(r'src="(\.\./[^"]+)"', embutir, corpo)
titulo = re.search(r'<h1>(.*?)</h1>', corpo).group(1)
html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>{titulo}</title>
<style>
  body {{ max-width:860px; margin:40px auto; padding:0 16px; font:16px/1.55 -apple-system, 'Segoe UI', Arial, sans-serif; color:#1f2328; background:#fff; }}
  table {{ border-collapse:collapse; margin:12px 0; }}
  th, td {{ border:1px solid #d0d7de; padding:6px 10px; text-align:left; vertical-align:top; }}
  th {{ background:#f6f8fa; }}
  code {{ background:#f6f8fa; padding:1px 4px; border-radius:4px; font-size:14px; }}
  pre {{ background:#f6f8fa; padding:12px; border-radius:6px; overflow-x:auto; }}
  pre code {{ padding:0; }}
  img {{ max-width:100%; border:1px solid #d0d7de; border-radius:6px; }}
</style></head>
<body>
{corpo}
</body></html>
"""
open(os.path.join(DOCS, 'emails-flash-crm.html'), 'w', encoding='utf-8').write(html)

destino = os.path.join(SKILL, 'scripts')
os.makedirs(destino, exist_ok=True)
for s in SCRIPTS:
    shutil.copy2(os.path.join(RAIZ, 'tools', s), destino)
esrgan = os.path.join(RAIZ, 'tools', 'bin', 'esrgan')
if os.path.isdir(esrgan) and not os.path.isdir(os.path.join(destino, 'bin', 'esrgan')):
    shutil.copytree(esrgan, os.path.join(destino, 'bin', 'esrgan'))

zip_path = os.path.join(DOCS, 'email-flash-crm.zip')
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    for pasta, dirs, arquivos in os.walk(SKILL):
        dirs[:] = [d for d in dirs if d not in ('bin', '__pycache__', '_render')]
        for a in arquivos:
            p = os.path.join(pasta, a)
            z.write(p, os.path.join('email-flash-crm', os.path.relpath(p, SKILL)))
    nomes = z.namelist()

print(os.path.join(DOCS, 'emails-flash-crm.html'))
print(zip_path)
for n in nomes:
    print('  ', n)
