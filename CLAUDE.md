# Templates de e-mail — Turbo Partners

Workspace de templates de e-mail para clientes (Flash CRM). Uma pasta por marca:

| Pasta | Marca | Loja Shopify | Formato |
|---|---|---|---|
| `numa/` | Nüma | — (CDN em `numa/README.md`) | HTML (antigo) |
| `pep/` | PEP Protein | `pep-protein.myshopify.com` · site `https://pepprotein.com.br` | HTML (antigo) |
| `repeat/` | Repeat | `y1yycy-wg.myshopify.com` (admin `repeatfoods`) · site `https://repeatonline.com.br` | **MJML** |
| `lata-fit/` | Latam Fit | `e11jwv-hs.myshopify.com` · site `https://www.latamfit.com.br` | **MJML** |
| `joie-suplementos/` | Joie Suplementos | site não é Shopify (`https://www.joiesuplementos.com.br`); imagens na `turbo-starter.myshopify.com` | **MJML** |
| `tools/` | scripts compartilhados (ver abaixo) | | |

## ⚠️ Formato: MJML, não HTML

O editor de e-mail do Flash é **GrapesJS + MJML** (desde ~ago/2026). Todo template novo é um
**`.mjml`**, importado pelo favorito "Importar MJML" (cada tag vira bloco nativo editável), com o
`.html` compilado ao lado só para preview/e-mail de teste. A referência completa é
`FLASHCRM-EMAIL-E-FLUXOS-PARA-DEV.md` (como importar, regras, variáveis, condicionais `fc-if--`,
blocos de produto). **Leia antes de escrever qualquer template.**

- HTML colado no bloco "HTML" vira um bloco só (`mj-raw`), editável só no código. É o formato antigo
  de `numa/` e `pep/` (e do `numa/README.md`, que descreve aquele pipeline). Ao refazer um deles,
  migre para MJML.
- Descadastro é `{{link_optout}}` (ou `{{unsubscribe_url}}`). O `%UNSUBSCRIBELINK%` dos templates
  antigos é do formato antigo e não aparece na lista de variáveis atual: confira num e-mail de teste
  antes de confiar nele.
- Rodapé com razão social, CNPJ e endereço. Saudação com `{{primeiro_nome}}` (`{{nome_cliente}}` é o
  nome completo). Assunto e pré-header não vão no MJML.

Para gente: `docs/emails-flash-crm.md` (página do ClickUp, curta, sem layout e sem menção a
repositório). Para o Claude: a skill `/email-flash-crm` (`.claude/skills/email-flash-crm/`:
`SKILL.md`, `referencia.md` com as regras técnicas e o `esqueleto.mjml`). Ao mudar uma regra aqui,
atualize o doc/a skill e rode `python tools/gerar_doc_skill.py`.

## Fluxo de um template novo (design em PNG → e-mail)

1. **Ler o design** (normalmente um PNG de 600px de largura, 1x, exportado do Figma).
   Medir cores e posições com PIL, não no olho: cor de fundo, cor do texto, faixas de conteúdo
   (linhas que diferem do fundo) e extensão horizontal de cada elemento (`python tools/medir.py design.png`).
   PNG com xadrez em volta = print do fundo transparente do visualizador: recorte só o cartão.
2. **Upscale para 2x**: `python tools/upscale.py design.png design-2x.png`. Recorte todos os
   assets a partir do 2x (coordenadas do 1x × 2) e exiba no tamanho 1x. Packshot e logo: prefira o
   original da loja (`/products/<handle>.json`), encaixado por template matching (Latam Fit).
3. **Decidir o que vira imagem.** Regra: texto é texto. Só vira imagem o que e-mail não
   faz: foto, produto, fonte cursiva/display, formas com recorte.
   - **Texto em cima de foto/degradê** → apaga o texto da imagem (`tools/remove_text.py`), usa a
     imagem limpa como `background-url` da `mj-section` e escreve o texto em `mj-text` por cima.
   - **Fonte cursiva/decorativa** (ex.: "de conhecer") → PNG transparente extraído com
     `remove_text.py --extrair`, com `alt` igual ao texto.
   - **Forma simples com texto** (ticket de cupom, selo) → **redesenhe a forma vazia com PIL**
     medindo o original, em vez de tentar limpar. Fica mais nítido e é mais rápido. Texto por cima.
   - **Parte de baixo de um hero** (produto/foto) → imagem normal. Corte o hero onde o fundo é
     liso para não ter emenda visível.
   - Colunas que empilham no celular → uma imagem por coluna, não uma faixa só.
4. **Montar o MJML** a partir de `.claude/skills/email-flash-crm/esqueleto.mjml` (padrões abaixo).
5. **Compilar, renderizar e comparar**: `python tools/render.py lata-fit/x.mjml lata-fit/assets/x design.png`
   valida, compila (grava o `.html` ao lado) e gera `tools/_render/comparacao.png` (design | desktop |
   mobile). Olhe a imagem e ajuste até bater.
6. **Subir as imagens** na Shopify (seção abaixo) e colocar as URLs do CDN no MJML.
7. **Última renderização** antes de entregar. No Flash: Templates → Criar Template → E-mail →
   favorito **Importar MJML** → colar o `.mjml` → Import → nomear → Criar Template.

## Padrões MJML que funcionaram

Detalhes e exemplos em `.claude/skills/email-flash-crm/referencia.md` §5 e nos `.mjml` de `repeat/`
e `lata-fit/`.

- **Padding sempre por lado** (`padding-top/right/bottom/left`), nunca o atalho. Fonte e cor em todo
  `mj-text`/`mj-button` (`'Helvetica Neue', Helvetica, Arial, sans-serif`).
- **Mobile = desktop em escala.** `mj-head` só com `mj-style` funciona: testado em 23/10/2026 no
  editor do Flash (`setComponents` + `mjml-code-to-html`): a media query chega ao HTML. **Salvar não
  foi testado**: conferir no e-mail de teste. Padrão: `css-class` nos elementos e
  `@media only screen and (max-width:480px)` com `!important` (texto: `.cls div {font-size}`;
  espaçamento: `.cls {padding-*}`, porque a classe fica no `<td>` do elemento; imagem:
  `.cls table, .cls td {width}` + `.cls img {width;height}`). Padding de **seção** não dá para mudar por
  classe: ponha o espaçamento vertical no elemento. Segundo degrau `max-width:359px` para 320px.
  Conferir em 320/360/375/390.
- **Texto em cima de foto:** `mj-section background-url background-size="cover"
  background-position="center bottom"` (o MJML gera o VML do Outlook). `background-color` = cor do
  **meio** da imagem. A altura da seção (paddings + line-heights) bate com a da imagem.
- **Card arredondado:** `mj-wrapper` (fundo de fora + margem) com `mj-section`s do card;
  `border-radius="0 0 14px 14px"` na última.
- **Colunas que não empilham: tabela, não `mj-group`.** O `mj-group` passa no render local mas
  **empilhou no Gmail do celular** (teste do Flash, 23/10/2026). Linha lado a lado = `<mj-column><mj-raw><tr><td
  style="padding:0;" class="fc-html-block"><table width="100%">…</table></td></tr></mj-raw></mj-column>` (o formato do
  bloco HTML do Flash), com células em %, imagens `width:100%; max-width:Npx` e as classes de mobile nas
  células/imagens. Contrapartida: no editor do Flash essa linha é um bloco HTML (edita no código).
- **Quebras do layout:** `<br>` só em linha curta; parágrafo com
  `<div style="max-width:Npx; margin:0 auto;">` (no celular quebra sozinho).
- **Botão:** `mj-button` com `line-height` + `inner-padding` para a altura e `width` em px.
- **Fonte condensada** (código de cupom etc.):
  `'Helvetica Neue Condensed', 'Roboto Condensed', 'Arial Narrow', 'Helvetica Neue', Arial, sans-serif`.
- `mj-image` fluida **sem** `height` (distorce no celular); ícone/logo com `width` + `height`.
- **Modo escuro do Gmail** escurece fundo de seção mas não imagem: ícone/selo/packshot/card sobre fundo liso
  vai em PNG transparente, senão vira caixa branca (detalhes em `referencia.md` §4, exemplo em `lata-fit/`).

## ⚠️ Sem comentários

Nem `<!-- -->` no MJML (com `{{ }}` dentro quebra o build e vira lixo no editor) nem `{{!-- --}}`
(aparece como texto). Anotações vão no `README.md` da marca. Nos `.html` antigos (PEP/Nüma), só os
condicionais do Outlook (`<!--[if mso]>`).

## Subir imagens na Shopify

```bash
# uma vez por loja (abre o navegador, o usuário autoriza):
shopify store auth --store <loja>.myshopify.com --scopes read_files,write_files
# sempre antes de subir: o nome já existe?
python tools/upload_shopify.py <loja>.myshopify.com check <prefixo>
python tools/upload_shopify.py <loja>.myshopify.com upload <pasta> arq1.jpg arq2.png
```
- A autorização fica salva **na máquina**, não no chat: um chat novo já consegue subir. Confira
  com `shopify store auth list` (a `pep-protein` foi autorizada em 25/09/2026). O token é "online"
  e expira: se o `check`/`upload` der erro de autenticação ou escopo, rode o `shopify store auth`
  de novo (em background, porque ele espera o usuário aprovar no navegador) e peça para o usuário
  aprovar. Outras lojas nessa lista podem ter sido autorizadas com outros escopos, então teste
  com `check` antes.
- **Prefixe todo arquivo** com marca + template (`pep-bv-` = PEP boas-vindas). O Files da
  Shopify é plano: nome repetido vira `nome_<uuid>.png` e a URL do HTML quebra.
- Nunca reenvie com o mesmo nome para "atualizar". Use um nome novo (`-v2`) e troque no template.
- Use a URL sem o `?v=...`. Base da PEP: `https://cdn.shopify.com/s/files/1/0994/1008/4203/files/`.
- Link padrão dos CTAs: busque `shop { primaryDomain { url } }` e confirme que a página existe.

## Ferramentas (`tools/`)

| Script | O que faz |
|---|---|
| `medir.py` | cor de fundo + faixas de conteúdo do design (y0-y1, x0-x1). `--lim` sobe o limiar se o JPG tiver ruído. |
| `upscale.py` | 1x → 2x com Real-ESRGAN (`bin/esrgan`, GPU/Vulkan). 4x + Lanczos p/ 2x. Texto grande fica nítido; letra minúscula (rótulo de lata) vira rabisco, porque não dá pra recuperar o que não está no 1x. Nesse caso peça export 2x do Figma. |
| `remove_text.py` | apaga texto claro de fundo **liso** ajustando um polinômio 2D (não use `cv2.inpaint`: deixa manchas no glow do texto). `--extrair` salva um trecho do texto como PNG com alfa. A regra de "o que é texto" está calibrada para texto claro em céu azul; ajuste para outras cores. Fundo com textura/foto → IA (ChatGPT) ou Figma. |
| `render.py` | preview desktop + mobile + comparação com o design. Aceita `.mjml` (valida e compila com `npx mjml@4.15.3`, grava o `.html` ao lado) ou `.html`. Troca o CDN por arquivo local (imagem remota às vezes não carrega no headless e o print sai cortado, **não é bug de layout**). A altura acompanha o design; sem design, `RENDER_H=<px>` (o padrão de 2400 corta e-mail longo). Com várias sessões em paralelo, use `RENDER_OUT=<pasta>` para não sobrescrever o `_render` de outra. |
| `upload_shopify.py` | `check` / `upload` no Files via Shopify CLI (stagedUploadsCreate → POST → fileCreate → espera READY). |
| `gerar_doc_skill.py` | gera `docs/emails-flash-crm.html` (doc com os prints embutidos, para copiar do Chrome e colar no ClickUp), copia os scripts acima para `scripts/` da skill e monta `docs/email-flash-crm.zip` (a skill que vai anexada no ClickUp). |

Dependências já instaladas: Python com Pillow, numpy, opencv (`cv2`), requests; Node (`npx mjml@4.15.3`);
Shopify CLI; Chrome. Se o `tools/bin/esrgan` sumir: baixar
`https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip`
e deixar só `realesrgan-ncnn-vulkan.exe`, as DLLs e `models/realesrgan-x4plus.*`.

## Ambiente

- Windows. **O Bash tool trava** neste workspace (comandos simples dão timeout): use PowerShell.
- No PowerShell, grave arquivos com `[IO.File]::WriteAllText($f, $s, (New-Object Text.UTF8Encoding $false))`:
  `Set-Content`/`Get-Content` sem `-Encoding utf8` corrompem acentos.
- Chrome headless: janela de 800px para desktop (com 600px a barra de rolagem ativa a media
  query de mobile); mobile via `<iframe style="width:375px">`.

## Onde paramos (atualize ao fim de cada sessão)

**17/11/2026 — Joie Suplementos Black Friday e-mail 03, 30% OFF + brindes (`joie-suplementos/black-17-11.mjml`): montado, aguardando aprovação.**
- Só PNG (sem PSD); o link do Figma no `Figma.docx` deu "sem acesso" no MCP. Imagens na **turbo-starter** com prefixo `joie-b17-`
  (11, todas 200). Detalhes no `joie-suplementos/README.md`.
- O ESRGAN clareia fundos quase pretos (+2 a +8 níveis): o `_recortes.py` corrige o 2x pela média do 1x (vale para outros
  e-mails escuros). Fundo com texto por cima em `background-size="100% 100%"` (cortina continua alinhada no celular).
- Pendências: confirmar que os 30% são automáticos (layout sem cupom), link `/produtos/c`, CNPJ.

**12/11/2026 — Joie Suplementos Black Friday semana 02, brindes (`joie-suplementos/black-friday-brindes.mjml`): montado, aguardando aprovação.**
- Layout PNG + PSD do designer (as 3 fatias com texto na imagem não foram usadas). Imagens na **turbo-starter** com prefixo
  `joie-bfb-` (10, todas 200). Este PSD é Apple RGB, mas o PNG exportado usa os valores crus: sem conversão (verde `#bfe132`).
  Detalhes no `joie-suplementos/README.md`.
- O `black-friday-aquecimento.mjml` e os assets do e-mail 01 **não estão mais no disco** (só o README e o CDN).
- Pendências: "Ganhe Ganhe Própolis" e "259,90" sem R$ corrigidos no texto; duas faixas "ACIMA DE R$299"; link do botão
  (`/produtos/c`); CNPJ.

**09/11/2026 — Latam Fit e-mail Pré Black refeito (`lata-fit/email-preblack.mjml`): montado, aguardando aprovação.**
- Mesmo Figma do `pre-black-30off-1` (`16001:8889`), refeito do zero com export novo (idêntico). Imagens na **turbo-starter** com prefixo `lf-epb-` (14, todas 200). Detalhes no `lata-fit/README.md`.

**06/11/2026 — Joie Suplementos Black Friday aquecimento (`joie-suplementos/black-friday-aquecimento.mjml`): montado, aguardando aprovação.**
- Marca nova (`joie-suplementos/README.md`). Layout = PNG + **PSD** do designer: fundos e foto dos produtos saíram das
  camadas (sem texto, foto em 1856px). O PSD está em **Adobe RGB**: converter para sRGB (`#b6dd12` → `#a5de00`).
  psd-tools precisa ser >= 1.10 (detalhes no README). Títulos em Trade Gothic viraram imagem; o resto é texto.
- Imagens no Files da `turbo-starter` (pedido do usuário) com prefixo `joie-bfa-` (8, todas 200). A 1ª tentativa
  falhou sem `read_files`; resolveu `shopify store auth` **sem `--no-input`** com a lista de escopos do usuário
  (ver memória). Uma lista maior de escopos foi barrada pela permissão automática do Claude Code.
- Pendências: CTA (o layout não tem), CNPJ/endereço (da Receita, confirmar).

**05/11/2026 — Latam Fit Pré Black 30% OFF, 3 versões (`lata-fit/pre-black-30off-1/-2/-3.mjml`): montados, aguardando aprovação.**
- Layouts direto do Figma (MCP: `get_metadata`/`get_design_context` para fontes e medidas, `download_assets` com escala 2 para o
  export vetorial 2x, sem ESRGAN). Os três saem de `lata-fit/assets/pre-black-30off/_montar.py` (só muda o bloco da Caixa Surpresa).
  Imagens no Files com prefixo `lf-p30-` (14, todas 200). Detalhes e pendências no `lata-fit/README.md`.
- Pedido do usuário: não criar cupons (o `PREBLACK` já existe) e **não gerar imagem com IA** (Higgsfield etc.): tudo vem do export
  do Figma e de PIL.
- Pendências: o e-mail 2 diz "R$ 139,00 com cupom" mas a caixa já custa R$ 139 sem cupom; 3º card repete a Cocada; CNPJ.
- O `render.py` recorta o desktop em x=100, mas com `RENDER_H` alto o corpo saiu em x=92: a comparação parece deslocada 8px sem estar.

**04/11/2026 — Latam Fit carrinho abandonado, régua de 3 e-mails (`lata-fit/carrinho-abandonado.mjml`, `-10off`, `-15off`): montados, aguardando aprovação.**
- Sem layout: design na identidade do Goiabinha, hero gerado com os packshots da loja. Imagens no Files com prefixo
  `lf-ca-` (3, todas 200); logo, selos e rodapé reaproveitam `lf-lg-`. Detalhes no `lata-fit/README.md`.
- Regra do usuário: 1º sem cupom → 2 h → 2º com 10% → 3º com 15% (espera ainda não definida). Se for um só, usar o de 10%.
- `CARRINHO10` e `CARRINHO15` **já existiam** na Shopify (ativos, 0 usos): não criei nem alterei. O `CARRINHO10` não tem limite
  por cliente (perguntar). A loja tem 520 cupons ativos: um `first: 60` não acha tudo e me fez dizer errado que não havia cupom.
- Não importado no Flash, fluxo não criado. **O plano da conta não permitia automação em 30/10**: conferir antes de contar com o fluxo.
- Os `assets/` tinham saído das pastas das marcas em 30/10 (`D:\Turbo\email.rar`); o usuário devolveu os da Latam Fit
  em 04/11. `repeat/`, `pep/` e `numa/` continuam sem `assets/` no disco.
- Python desta máquina dá `CERTIFICATE_VERIFY_FAILED` em `www.latamfit.com.br`, mas o certificado do site é válido
  (até 21/12/2026): para ler o site use `Invoke-WebRequest`.

**30/10/2026 — Latam Fit Pré Black (`lata-fit/pre-black.mjml`): montado, aguardando aprovação.**
- Layout `lata-fit/email-novo/PRÉ BLACK - EMAIL 3 COMPLETO.png`. Imagens no Files com prefixo `lf-pb-` (8, todas 200);
  rodapé reaproveita `lf-lg-logo-branco`/`lf-lg-instagram-v2`. Detalhes no `lata-fit/README.md`.
- A moldura xadrez (azul/creme) **é design**, não transparência; ficou de fora como no Goiabinha (perguntar).
- Cupom `PREBLACK` existe (30% pedido inteiro, 28/10 a 15/11), mas o layout diz "Vale a partir de segunda, 26/10".
  "Coloque na agenda!" sem conteúdo embaixo. Os dois ficaram como no layout, pendentes.
- `latamfit.com.br/collections/*` e `/products/*` devolvem 429 para script; conferir links pelo Admin
  (`shopify store execute`) ou no navegador.

**28-29/10/2026 — Latam Fit: diagnóstico da base, Bling e migração Shoppub → foi para `D:\Turbo\latam fit`.**
- Dados de pedidos/clientes (Shopify, Bling, listas e segmentos do Flash) ficam no `CLAUDE.md` de lá. Aqui só
  e-mail e uso do Flash.

**26/10/2026 — Latam Fit: Lançamento Goiabinha ENVIADO para a base.**
- Campanha 971 (original): o usuário criou "Agendar envio" **sem data** e ela **disparou na hora**; cancelada
  com 600 envios (arquivada). Cópia 978: **duplicar campanha não leva a lista**, só os segmentos → foi para 12.
- Reenvio = rascunho 979 ("(Copia) (Copia)"): audiência lista 374 + segmento 2271, **"Não enviar para"** o
  segmento novo "Latam Fit - Ja recebeu Lancamento Goiabinha (excluir)" ("Recebeu email" da campanha 971 OU 978,
  610 pessoas). Disparado com OK explícito: **2.039 destinatários** (26/10 11:35). Total da base ≈ 2.651.
- Regras do Flash aprendidas: **salvar/criar campanha com "Enviar agora" dispara; "Agendar" sem data também
  disparou**. Duplicar cria rascunho com "Salvar Alterações" (que também dispara). "Calcular destinatários"
  falhou na tela de edição: contar pelo Preview de segmento (`Recebeu email` → Campanha → qual). O Chrome com o
  Flash logado é o **DESKTOP-CAPG5K1** (`4b34c536`); screenshot funciona nele.

**23/10/2026 — Latam Fit lançamento Goiabinha (`lata-fit/lancamento-goiabinha.mjml`): montado, aguardando aprovação.**
- Marca nova (`lata-fit/README.md`). Layout em `lata-fit/email-que-deve-ser-copiado/`. O xadrez em volta do PNG é
  o fundo de transparência do visualizador, não design: o e-mail é o cartão de 575px escalado para 600.
- Feito primeiro em HTML (erro: segui a skill antiga) e convertido para **MJML** a pedido do usuário. Na mesma
  sessão a skill, este arquivo, o doc do ClickUp e o `render.py` (aceita `.mjml`) passaram a ser MJML.
- Fotos e logo vêm dos originais da loja (`_fontes/`), encaixados por template matching no `_recortes.py`.
  Imagens no Files com prefixo `lf-lg-`. Todos os CTAs → página do combo de goiabada (link do usuário).
- Pendências: CNPJ/razão social do rodapé; o endereço veio do cadastro de cobrança da Shopify (confirmar); o 1º
  card diz "a clássica" mas mostra a Goiabinha com chocolate (igual ao layout); `mj-group` não testado no editor do Flash.
- Risco a avisar: os templates antigos (PEP/Nüma) usam `%UNSUBSCRIBELINK%`, que não está na lista atual de variáveis.
- Mesma data, depois: mobile virou "desktop em escala" (`mj-style` + `mj-group`, testado no editor do Flash sem
  salvar) e imagens em PNG transparente para o modo escuro (`-v2`). O `mj-group` empilhou no Gmail do celular do
  usuário (2 testes): as 4 linhas lado a lado viraram tabela no bloco HTML (`mj-raw`). Falta o teste no celular
  dessa versão.
- **Público "comprou de 31 a 180 dias" (subagente, 23/10):** no Flash existe a automação **2178** (inativa,
  gatilho "Cliente fez um pedido" + filtro "≥1 pedido entre 26/04 e 22/09", entrada "Sempre"): manda para quem
  acabou de comprar, não para a base. O Flash só tem pedidos desde 21/09/2026 (Shopify conectada em 09/10; a
  Shoppub não está integrada): "Dias desde a última compra entre 31 e 180" dá **8 contatos**, e 19.811 dos 20.855
  contatos estão sem nenhum pedido (base migrada da Shoppub). Para o público real precisa de export da Shoppub
  (lista) ou importar o histórico, decisão do usuário. "Entre datas" do Flash corta o último dia (meia-noite UTC).
- **Criado no Flash (23/10, a pedido):** segmento "Latam Fit - Ultima compra 31 a 180 dias (opt-in email)"
  (`recencia` entre 31 e 180 **E** `opt_in_email` = Sim; Preview: 6 contatos). Campanha "Lançamento Goiabinha com
  chocolate branco" **preenchida e não criada**: a tela de nova campanha não tem rascunho (só "Enviar agora", que
  dispara ao clicar em "Criar Campanha", ou "Agendar envio" com data). Ficou na aba do Chrome com o segmento, o
  template 4362, o assunto, o pré-header e "Agendar envio" sem data. O usuário vai subir o MJML novo no 4362 à mão.
  No construtor, `form_input` em rádio não muda o estado do React: clicar no `<label>` (aparece o campo de data).
  Digitação com `type` perdeu letras; preencher texto com `form_input`.
- **Shopify da Latam Fit (CLI agora com `read_orders,read_customers`, 23/10): o histórico da Shoppub ESTÁ na
  Shopify.** A API de pedidos só mostra 60 dias sem `read_all_orders` (eu concluí errado que não havia histórico).
  Pelos segmentos de cliente (`customerSegmentMembers`, sem esse limite): última compra 25/04-22/09 = **3.048**
  clientes (2.647 inscritos em e-mail); ≥1 pedido = 14.079; última compra depois de 22/09 = 1.042 (≈ os 1.044 com
  pedido no Flash). **O Flash só puxou 60 dias de pedidos** ao conectar (09/10). Caminhos: segmento na Shopify
  (`last_order_date >= 2026-04-25 AND last_order_date <= 2026-09-22 AND email_subscription_status = 'SUBSCRIBED'`)
  → exportar CSV → lista no Flash + o segmento do Flash; e pedir ao suporte do Flash a importação do histórico
  completo. Clientes migrados: tag `migracao-shoppub` (19.734), metafields `custom.cpf/sexo/shoppub_id/
  cliente_desde/nascimento`.
- **Feito no Flash em 23/10 (a pedido):** lista **374** "Latam Fit - Ultima compra 25/04 a 22/09/2026 (Shopify)",
  importada de um CSV só com e-mail (2.647 do segmento da Shopify inscritos em e-mail; opt-in "Não atribuir";
  declaração LGPD marcada com OK explícito do usuário). Resultado: 2.635 atualizados, 9 inseridos, 3 pulados,
  2.644 membros; contatos 20.859 → 20.868 (sem duplicar). Segmento **2271** ajustado para 31 a **181** dias.
  Campanha preenchida (lista 374 + segmento 2271, template 4362, assunto/pré-header, "Agendar envio" sem data) e
  **não criada**. Falta: usuário subir o MJML novo no 4362, teste, data. Suporte do Flash: importar histórico.
  Consulta pela CLI no Windows: chamar `node .../@shopify/cli/bin/run.js store execute` sem `shell=True`
  (o cmd quebra a query com `<`, `>` e quebra de linha).

**20/10/2026 — Repeat: reativação ajustada, aniversário em discussão (fluxos inativos).**
- Fluxo 2058 virou "dias sem comprar": qualquer cliente, entrada a cada compra, condições "Dias desde a
  última compra ≥ 40/60/90" (campo `recencia`). Detalhes no `repeat/README.md`.
- Aniversário (2057): o usuário quer **1 e-mail só**. O gatilho do Flash não tem "mês do aniversário"
  (confirmado no painel: só "no dia", "dias antes", "dias depois"). Falta ele escolher quando enviar e
  qual cupom; o fluxo ainda está com os 2 e-mails. O texto do 4143 e do WhatsApp `_dia_15off` diz
  "o presente cresceu" e precisa mudar se ficar só ele.
- Chrome com o Flash logado: Browser 1 (Windows), deviceId `4b34c536`. O Browser 2 (macOS) está deslogado.

**19/10/2026 — Repeat: WhatsApp adicionado nas 5 automações (todas ainda inativas).**
- 7 templates de WhatsApp da Repeat criados no Flash e **aprovados pela Meta** (`repeat_carrinho_5off`,
  `repeat_segunda_compra_10off`, `repeat_aniversario_antes_10off`/`_dia_15off`,
  `repeat_reativacao_40d_5off`/`60d_10off`/`90d_15off`); cashback usa o modelo `flashcrm_bounceback_wpp`.
- Etapa de WhatsApp logo depois de cada e-mail nos fluxos 2055–2059. Detalhes e formato no `repeat/README.md`.
- Sessão do Claude Code agora com outra conta: a extensão do Chrome precisa estar logada na mesma.
  Chrome do Flash nesta sessão: deviceId `4b34c536`.

**16/10/2026 — Repeat no Flash: carrinho abandonado montado (inativo).**
- Pelo Claude in Chrome ("Browser 2", painel de parceiro operando a Repeat = empresa 467): template
  4140 (MJML do carrinho via `editor.setComponents`) e fluxo 2055 (só e-mail, espera 1h, condição sem
  pedido, nasce inativo, salvo pela mutação `useSaveAutomationFlow` como no favorito "Importar fluxo").
- 2ª compra também: template 4141 + fluxo 2056 (gatilho `cliente_fez_pedido` com filtro
  `frequency = 1`, espera 5 dias, condição ainda 1 pedido), inativo.
- Aniversário: templates 4142/4143 + fluxo 2057 (gatilho `aniversario` 7 dias antes, NIVER10 → espera
  7 dias → não comprou em 7 dias? → NIVER15; reentrada a cada 300 dias), inativo.
- Reativação: templates 4144/4145/4146 + fluxo 2058 (1º pedido → 40 d VOLTA5 → +20 d VOLTA10 → +30 d
  VOLTA15, cada passo só se ainda tem 1 pedido), inativo. 4 de 5 réguas montadas.
- Cashback: template 4147 + fluxo 2059 (toda compra, entrada "Sempre" → espera 1 dia →
  `criar_cashback` 5%/30 dias/até 25% → e-mail com `R$ {{valor_cashback}}`, `{{cupom}}`,
  `{{data_vencimento}}`), inativo. `CASHBACK5` desativado na Shopify. **As 5 réguas estão montadas.**
- A extensão do Chrome pode cair e reconectar com outro nome/ID: o Chrome do Flash é o deviceId
  `21c5f917`. Print às vezes dá timeout com a janela coberta; conferir pelo DOM/React Query.
- Testado: template MJML importado salva e reabre inteiro. Conta mostra "Ative seus fluxos com um
  plano": ativar pode depender de plano. Ligar só depois do OK do usuário (dispara pra cliente real).
**16/10/2026 — Repeat: 2ª compra, aniversário (2) e reativação (3): montados, aguardando aprovação.**
- Feitos por 3 subagentes em paralelo no mesmo pipeline do carrinho. Templates `segunda-compra`,
  `aniversario-antes`/`-dia`, `reativacao-40`/`-60`/`-90` (`.mjml` + `.html`), prefixos `rep-sc-`,
  `rep-an-`, `rep-re-`. Detalhes, assuntos e pendências no `repeat/README.md`.
- Cupons criados na Shopify: `SEGUNDA10`, `NIVER10`, `NIVER15`, `VOLTA5`, `VOLTA10`, `VOLTA15` (pedido
  inteiro, um uso por cliente, só combinam com frete). Fora do carrinho, os CTAs usam
  `/discount/CODIGO?redirect=...` e aplicam o cupom sozinhos.
- `NIVER15` não fica limitado ao dia do aniversário (Shopify não sabe a data): "só hoje" é só no texto.
**16/10/2026 — Repeat carrinho abandonado (`repeat/carrinho-abandonado.mjml`): montado, aguardando aprovação.**
- Marca nova, em **MJML** (base: `FLASHCRM-EMAIL-E-FLUXOS-PARA-DEV.md`, import pelo favorito
  "Importar MJML"). Sem PNG do Figma: design feito do brandbook com logo, formas e fontes extraídos do
  PDF (`repeat/assets/_marca`, helpers em `marca.py`) e packshots da loja. Prefixo `rep-ca-`.
- Cupom = `5%CARRINHO`, que já existia na loja. CTAs → `{{carrinho_url}}`. Pendências no `repeat/README.md`.
**16/10/2026 — Repeat cashback (`repeat/cashback.mjml`): guardado, vai mudar.**
- Feito primeiro por engano (o pedido era carrinho). O usuário quer manter e depois mudar para "5% de
  cashback em cada compra (acumulativo)", com `{{cupom}}`/`{{valor_cashback}}` do Flash. Prefixo `rep-cb-`.
  A regra `CASHBACK5` (5%, sem limite por cliente, só combina com frete) ficou criada na Shopify.
- `tools/render.py` ganhou `RENDER_H` (altura da janela) para e-mails mais longos que 2400px.

**30/09/2026 — Doc para o ClickUp + skill: prontos.**
- Doc do ClickUp enxuto a pedido do usuário: só funcionalidades (criar no Flash, variáveis, o que
  quebra, imagens na Shopify, uso do Claude). **Nada de layout e nada de Git/repositório** no doc.
  Os detalhes de layout ficaram em `referencia.md` da skill.
- Colar markdown cru no ClickUp não funcionou: o caminho é abrir `docs/emails-flash-crm.html` no
  Chrome, Ctrl+A, Ctrl+C e colar. A skill vai anexada no ClickUp (`docs/email-flash-crm.zip`), por
  isso ela é autocontida (scripts dentro dela). Gerar os dois com `tools/gerar_doc_skill.py`.
- Prints em `prints-do-flash/` (`card-carrinho-numa.png`, `passo-1..4-*.png`), embutidos no HTML.
- No Flash o template é um bloco **HTML** só, com o arquivo inteiro colado em "Código HTML" e o campo
  "Estilos (CSS)" vazio. **Confirmar com o usuário** que é assim (deduzido dos prints e do erro de
  `mj-font` do `<head>`).
- **Achado, não corrigido (perguntar):** em `numa/carrinho-abnadonado.html` o botão "Voltar pro meu
  carrinho" fora do Outlook aponta para `https://sejanuma.com.br`; só o VML usa `{{carrinho_url}}`.

**25/09/2026 — PEP bem-vindo (`pep/bem-vindo.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/email-completo (8).jpg` (600×2774). Imagens no Files com prefixo `pep-bem-`
  (não confundir com `pep-bv-`, que é o boas-vindas com cupom). Sem cupom. Detalhes no `pep/README.md`.
**25/09/2026 — PEP pedido confirmado (`pep/pedido-confirmado.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/Pós-compra - Pedido Confirmado certo.png` (600×2012). Imagens no Files com
  prefixo `pep-pc-` (não confundir com `pep-pci-`, que é o pós-compra inativo). Detalhes no `pep/README.md`.
- CTA → `https://pepprotein.com.br/account` (não há variável de rastreio). Perguntar se preferem outro link.
**25/09/2026 — PEP pedido na rua (`pep/pedido-na-rua.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/Pós-compra - Pedido na rua.png` (600×2123). Imagens no Files com prefixo `pep-pnr-`.
- Não existe variável de rastreio: botão → `https://pepprotein.com.br/account`. Detalhes no `pep/README.md`.

**25/09/2026 — PEP 60 dias (`pep/60-dias.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/email-completo (6).jpg` (600×2256). Imagens no Files com prefixo `pep-60d-`
  (`hero`, `mao`, `braco`, `framboesa`, `latas`). Sem cupom. Detalhes no `pep/README.md`.
- ESRGAN travou com 7 sessões usando a GPU ao mesmo tempo; rodar o exe direto com `-t 128` resolveu.

**25/09/2026 — PEP pós-compra inativo (`pep/pos-compra-inativo.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/Pós-compra - inativo.png` (600×2283). Imagens no Files com prefixo `pep-pci-`
  (`hero-ceu`, `ultima-entrega`, `hero-latas`, `latas`); mãozinha = `pep-bv-mao.png`.
- Cupom `PEP10` fixo no texto; CTA → `/collections/all`. **Perguntar:** o design diz "na sua
  primeira compra", mas o e-mail é para quem já comprou.
- Com várias sessões em paralelo o ESRGAN fica na fila da GPU (levou ~15 min).

**25/09/2026 — PEP que tal voltar (`pep/que-tal-voltar.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/email-completo (5).jpg` (600×2001). Imagens no Files com prefixo `pep-qtv-`
  (`voltar`, `baldes`, `cupom`, `frutas`, `latas`); logo = `pep-u24-logo.png`, mãozinha = `pep-bv-mao.png`.
- Cupom `VOLTAR10` fixo no texto; CTA → `/collections/all`. Mesmas ideias pendentes (link
  `/discount/VOLTAR10?...` ou `{{cupom}}`), perguntar antes.

**25/09/2026 — PEP recompra 60 dias (`pep/recompra-60-dias.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/email-completo (7).jpg` (600×1911). Imagens no Files com prefixo `pep-r60-`
  (`lata-asas`, `cupom-vazio`, `mao`, `braco`). Cupom `VOLTAR10` fixo. Detalhes no `pep/README.md`.

**25/09/2026 — PEP recompra (`pep/recompra.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/email-completo (4).jpg` (600×1860). Imagens no Files com prefixo `pep-rc-`
  (`lata`, `card-latas`, `latas`); logo = `pep-u24-logo.png`, mãozinha = `pep-bv-mao.png`.
- Pendente: o 3º parágrafo do design termina cortado ("...que não precisa de"). Está igual no HTML
  até o usuário mandar o texto certo.

**25/09/2026 — PEP boas-vindas (`pep/boas-vindas.html`): pronto e aprovado pelo usuário.**
- Design de origem: `d:/Downloads/boas vindas - completo_.png` (600×1944, 1x).
- Todas as imagens já estão no Files da `pep-protein` (prefixo `pep-bv-`). Em uso: `hero-ceu`,
  `de-conhecer`, `hero-latas`, `cupom-vazio`, `latas`, `mao`. `pep-bv-hero.jpg` e
  `pep-bv-cupom.png` são versões antigas (com texto na imagem), ficaram de backup.
- Título do hero e código do cupom (`PRIMEIRA10`) são texto HTML.
- CTAs → `https://pepprotein.com.br/collections/all`.
- **Pendente:** `%UNSUBSCRIBELINK%` no rodapé (quem preenche é a plataforma de envio).
- **Ideias não feitas (perguntar antes):** trocar o link dos CTAs por
  `https://pepprotein.com.br/discount/PRIMEIRA10?redirect=/collections/all` (aplica o cupom
  sozinho; confirmar que o desconto existe na loja); usar `{{cupom}}` no lugar do código fixo
  se o fluxo mandar cupom por cliente.
- Próximo passo esperado: novos templates da PEP (o usuário manda o PNG).

**24/09/2026 — PEP últimas 24h (`pep/ultimas-24h.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/email-completo (3).jpg` (600×1688). Imagens no Files com prefixo `pep-u24-`
  (`logo`, `24horas`, `balde`, `latas`); a mãozinha reaproveita `pep-bv-mao.png`.
- Cupom `VOLTAR10` fixo no texto (card e caixa). Mesmas ideias pendentes do boas-vindas:
  link `/discount/VOLTAR10?...` ou `{{cupom}}`, perguntar antes.
- Outros designs na pasta Downloads (`email-completo.jpg`, `(2)`) ainda não foram feitos.

**24/09/2026 — PEP carrinho abandonado (`pep/carrinho-abandonado.html`): montado, aguardando aprovação.**
- Design: `d:/Downloads/email-completo (1).jpg` (600×2476). Imagens no Files com prefixo `pep-ca-`
  (`hero`, `faixa-latas`, `titulo-lata`, `lata`, `latas-card`); mãozinha = `pep-bv-mao.png`.
- CTAs → `{{carrinho_url}}`. Detalhes e decisões (pílulas na imagem da lata, emenda do card) no
  `pep/README.md`.
- Várias sessões rodando em paralelo usam o mesmo `tools/_render/`: um render sobrescreve o do
  outro. Se o preview vier com outro e-mail, renderize numa pasta própria.