---
name: email-flash-crm
description: Cria ou ajusta templates de e-mail marketing em MJML para o Flash CRM a partir de um layout PNG/JPG do Figma (600px de largura). Mede o layout, faz upscale 2x, recorta os assets, monta o MJML (blocos nativos do editor GrapesJS do Flash, importados pelo favorito "Importar MJML"), compila, renderiza e compara com o layout e sobe as imagens no Files da Shopify da loja do cliente. Use sempre que pedirem um e-mail ou template novo para uma marca (PEP, Nüma, Repeat, Latam Fit ou marca nova), "monta esse e-mail", "transforma esse PNG em e-mail", ajuste em template existente, dúvida sobre variáveis do Flash ({{primeiro_nome}}, {{carrinho_url}}, {{link_optout}}, fc-if--) ou para subir imagens de e-mail na Shopify.
argument-hint: <marca> <caminho do layout> [o que é o e-mail, cupom, links]
---

# Template de e-mail para o Flash CRM

O Flash CRM dispara os e-mails das automações dos clientes da Turbo. O layout vem do Figma como
PNG; a entrega é um **`.mjml`** com texto real, imagens no CDN da Shopify da loja do cliente e as
variáveis do Flash, mais o `.html` compilado ao lado (preview e e-mail de teste).

**Por que MJML:** o editor de e-mail do Flash é GrapesJS + MJML (desde ~ago/2026). MJML importado
pelo favorito "Importar MJML" vira blocos nativos (Texto, Imagem, Botão) editáveis no painel. HTML
colado no bloco "HTML" vira um bloco só (`mj-raw`), editável só no código. Os templates antigos da
PEP e da Nüma são desse jeito (HTML); ao refazer, migre para MJML.

**Arquivos desta skill** (`SKILL_DIR` nos comandos abaixo = a pasta mostrada em "Base directory for
this skill" quando a skill carrega):
- `referencia.md`: como importar no Flash (código do favorito), regras de MJML do Flash, variáveis,
  condicionais, o que vira imagem, padrões de layout em MJML e regras da Shopify. **Leia antes de
  escrever o MJML.**
- `esqueleto.mjml`: ponto de partida de todo template novo.
- `esqueleto.html`: formato antigo (HTML no bloco HTML). Só para ajustar template antigo que ainda
  está nesse formato.
- `scripts/`: `medir.py`, `upscale.py`, `remove_text.py`, `render.py`, `upload_shopify.py`.

**Pasta de trabalho** (o diretório onde o Claude Code foi aberto): uma subpasta por marca, com
`<marca>/README.md`, `<marca>/<template>.mjml` (+ `.html` compilado) e `<marca>/assets/<template>/`.
Se existir um `CLAUDE.md` ou um `<marca>/README.md`, leia antes: têm a loja, as cores, o rodapé
(razão social/CNPJ), os prefixos usados e as decisões anteriores, e ganham desta skill quando
divergirem.

## 0. Confirmar antes de começar

| Item | Se não vier |
|---|---|
| Marca e loja Shopify | Procure no `CLAUDE.md`/README da marca; se não achar, pergunte. O domínio `.myshopify.com` sai do `https://<site>/meta.json` |
| Caminho do layout | Pergunte |
| Nome do template (`kebab-case`) e prefixo dos arquivos (`<marca>-<sigla>-`, ex. `pep-r90-`) | Proponha e rode o `check` do prefixo (passo 6) |
| Qual e-mail/fluxo é | Deduza do texto do layout |
| Link dos CTAs | Carrinho abandonado: `{{carrinho_url}}`. Demais: `/collections/all` do domínio da loja. Anote como pendência |
| Cupom | Fixo no texto, igual ao layout. Anote `{{cupom}}` como alternativa |
| Rodapé legal | Razão social, CNPJ e endereço (o Flash pede). README da marca; senão `shop { billingAddress }` na Shopify e pergunte o CNPJ |

Só pare para perguntar o que bloqueia. O resto vira pendência no fim.

## 1. Ler o layout

```powershell
New-Item -ItemType Directory -Force <marca>/assets/<template>
Copy-Item "<layout>" <marca>/assets/<template>/_design.png
python "SKILL_DIR/scripts/medir.py" <marca>/assets/<template>/_design.png
```

O `medir.py` dá a cor de fundo e cada faixa de conteúdo (y0-y1, x0-x1). Use essas medidas para cores,
espaçamentos e recortes; nunca estime no olho. Olhe a imagem para entender o que é cada faixa.

PNG com **xadrez cinza/verde em volta** é print do fundo transparente do visualizador, não design:
recorte só o cartão do e-mail e escale para 600px.

## 2. Upscale 2x

```powershell
python "SKILL_DIR/scripts/upscale.py" <marca>/assets/<template>/_design.png <marca>/assets/<template>/_design-2x.png
```

Precisa do Real-ESRGAN em `SKILL_DIR/scripts/bin/esrgan/` (`realesrgan-ncnn-vulkan.exe`, DLLs e
`models/realesrgan-x4plus.*`, de
`https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip`).
Sem ele, peça o export 2x do Figma. Com outras sessões usando a GPU ele pode travar: rode o exe
direto com `-t 128` (caminho absoluto). Recortes sempre do 2x (coordenadas do 1x × 2), exibidos em 1x.

**Fotos de produto e logo:** antes de recortar do print, procure o original na loja
(`https://<site>/products/<handle>.json`, `/collections/<handle>/products.json`, logo no `<img>` do
header). Original em alta + template matching contra o layout (`referencia.md` §4) fica muito mais
nítido que o upscale de um print 1x.

## 3. Decidir o que vira imagem

Texto é texto; só vira imagem o que e-mail não faz (tabela completa em `referencia.md` §4). Escreva
os recortes num `<marca>/assets/<template>/_recortes.py` (JPG `quality=88, optimize=True,
progressive=True`; PNG para alfa e ícones pequenos chapados), com o prefixo do template em todo nome.
Imagens de coluna que empilham no celular: uma imagem por coluna, não uma faixa inteira.

## 4. Montar o MJML

Copie `SKILL_DIR/esqueleto.mjml` para `<marca>/<template>.mjml` e construa a partir dele.

Não esqueça (detalhes em `referencia.md`):
- `mj-body width="600px"`; tudo em `mj-section` → `mj-column`; `mj-wrapper` para card que atravessa
  várias seções. Linha que **não pode empilhar** no celular: tabela no bloco HTML (`mj-raw` com
  `fc-html-block`, `referencia.md` §5). O `mj-group` empilhou no Gmail do celular.
- **Padding sempre por lado** (`padding-top/right/bottom/left`), nunca o atalho `padding="..."`.
- **Sem comentários**, sem webfont. Fonte e cor em todo `mj-text`/`mj-button`
  (`'Helvetica Neue', Helvetica, Arial, sans-serif`). `mj-head` só com `mj-style`.
- **Mobile = desktop em escala:** linhas lado a lado em tabela (acima), imagens fluidas, e
  fontes/espaçamentos menores por `css-class` + media query no `mj-style`
  (`referencia.md` §5). Espaçamento vertical no elemento, não na seção. `<br>` só em linha curta; para
  imitar a quebra do layout em parágrafo, `<div style="max-width:Npx; margin:0 auto;">` (com outro N
  no mobile).
- `mj-image` com `alt`, `width` e URL absoluta; `height` só em ícone/logo (em imagem fluida distorce).
- CTA sempre `mj-button` (mesmo `href` das imagens clicáveis).
- Rodapé com razão social, CNPJ, endereço e `<a href="{{link_optout}}">`. Assunto e pré-header
  **não** vão no MJML (ficam no passo do fluxo).

## 5. Compilar, renderizar e comparar

```powershell
$env:RENDER_OUT = "_render/<template>"
python "SKILL_DIR/scripts/render.py" <marca>/<template>.mjml <marca>/assets/<template> <marca>/assets/<template>/_design.png
```

O `render.py` valida e compila o `.mjml` com `npx mjml@4.15.3` (grava o `.html` ao lado) e gera
`_render/<template>/comparacao.png` (layout | desktop | mobile). Ajuste até bater: alturas, quebras,
cores, emendas imagem/texto. Confira o mobile em 320, 360, 375 e 390px (iframes lado a lado de cada
largura apontando para o `prev.html` do `RENDER_OUT`). Sempre com `RENDER_OUT` próprio (outras sessões podem estar
renderizando). E-mail longo: `RENDER_H=2700`. Imagem faltando no preview costuma ser o CDN no
headless, não bug de layout: o script já troca o CDN pelo arquivo local.

## 6. Subir as imagens

```powershell
python "SKILL_DIR/scripts/upload_shopify.py" <loja>.myshopify.com check <prefixo>
python "SKILL_DIR/scripts/upload_shopify.py" <loja>.myshopify.com upload <marca>/assets/<template> arq1.jpg arq2.png
```

- Sempre `check` antes (e um `check` de um arquivo que existe, para saber que a consulta funciona);
  nunca reenvie com o mesmo nome (`-v2`); URL sem `?v=`.
- Loja não autorizada / erro de autenticação ou escopo: rode
  `shopify store auth --store <loja>.myshopify.com --scopes read_files,write_files` em background
  (espera o usuário aprovar no navegador) e peça a aprovação.
- Imagem que já existe em outro template da marca (logo, ícone): reaproveite a URL.
- Confira que toda URL do `.mjml` responde 200.

## 7. Entregar

1. Render final com as URLs do CDN.
2. Seção do template no `<marca>/README.md`: layout de origem, tabela de arquivos (recorte do 1x e
   uso), o que é texto, links e pendências. Marca nova: crie o README com loja, domínio, base do CDN,
   cores, rodapé legal e prefixos.
3. Se houver `CLAUDE.md` com "Onde paramos", adicione a entrada (data, status, prefixo, pendências).
4. Resposta curta: o que ficou pronto, a comparação e as pendências (links, cupom, CNPJ, texto do
   layout com problema). Lembre o que falta no Flash: Templates → Criar Template → E-mail → favorito
   **Importar MJML** → colar o `.mjml` → Import → conferir → nomear → Criar Template → e-mail de teste.
   Assunto e pré-header no passo do fluxo (sugira os dois).

## Ambiente

- Dependências: Python 3 com `pillow numpy opencv-python requests`, Node (para `npx mjml`), Google
  Chrome, Shopify CLI.
- Windows: se o Bash travar, use PowerShell. Grave arquivos com a ferramenta Write ou
  `[IO.File]::WriteAllText($f, $s, (New-Object Text.UTF8Encoding $false))`; `Set-Content` sem
  `-Encoding utf8` corrompe acento.
- Chrome headless: janela de 800px no desktop (com 600px a barra de rolagem ativa o mobile);
  mobile via `<iframe style="width:375px">`. O `render.py` já faz isso.
