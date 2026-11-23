# Referência técnica: e-mails MJML para o Flash CRM

Tudo que o SKILL.md resume, com detalhe. Levantado por engenharia reversa do front do Flash
(out/2026) e em templates reais; quando a pasta de trabalho tiver um README da marca mais novo, ele
ganha. Nada disso é API oficial: uma atualização do Flash pode mudar qualquer parte.

## 1. Importar no Flash

O editor de e-mail é **GrapesJS + plugin MJML**. Cada tag MJML vira um bloco nativo. O comando
`mjml-import` existe mas não tem botão: chama-se por um favorito do navegador.

**Criar o favorito** (uma vez por navegador): barra de favoritos (`Ctrl+Shift+B`) → botão direito →
Adicionar página → Nome `Importar MJML` → URL:

```
javascript:(()=>{for(const f of document.querySelectorAll('iframe')){let d;try{d=f.contentDocument}catch(e){continue}if(!d)continue;const v=[...d.querySelectorAll('*')].find(e=>e.__gjsv);if(v){const em=v.__gjsv.em;const ed=(em.getEditor&&em.getEditor())||em.Editor;ed.runCommand('mjml-import');return}}alert('Abra um template de e-mail no editor do Flash primeiro.')})()
```

**Usar:** Templates → Criar Template → E-mail (`/templates/novo?tipo=email`) → clicar no favorito →
apagar o conteúdo do modal "Import MJML" → colar o `.mjml` inteiro → Import → conferir → nomear →
Criar Template. Assunto e pré-header vão no passo do fluxo/campanha. Pelo console (ou pelo Claude in
Chrome): `editor.setComponents(mjml)` faz o mesmo; `editor.getHtml()` mostra o HTML compilado.

- **Import substitui o template inteiro** (não soma).
- Testado (Repeat, 16/10/2026): MJML importado salva e reabre inteiro, com variáveis e `fc-if`; o
  Flash acrescenta um `mj-head` próprio (`mj-font` + `mj-attributes`) de branding.
- O canvas do editor não mostra o padding das seções; o HTML enviado tem. Para ver o real:
  "Visualizar" ou `editor.getHtml()`.

## 2. Regras de MJML no Flash

| Bloco da paleta | MJML |
|---|---|
| Seção | `<mj-section padding="0"><mj-column></mj-column></mj-section>` |
| Texto | `<mj-text padding="10px 25px" font-size="14px" color="#1A1A1A" line-height="1.5">` |
| Imagem | `<mj-image src="" alt="" padding="10px 25px" fluid-on-mobile="true">` |
| Botão | `<mj-button background-color="#000000" color="#FFFFFF" border-radius="6px" font-size="14px" padding="10px 25px" href="#">` |
| Divisor / Espaço | `<mj-divider>` / `<mj-spacer height="32px">` |
| HTML | `<mj-raw><tr><td class="fc-html-block">…</td></tr></mj-raw>` (**dívida**: bloco só de código) |

- Tudo dentro de `mj-section` → `mj-column` (até 4 colunas por seção). `mj-wrapper` agrupa seções;
  `mj-group` impede as colunas de empilharem no celular.
- **Padding por lado** (`padding-top/right/bottom/left`), nunca o atalho: o importador põe os padrões
  por lado e o painel mostra valores errados se você usou o atalho.
- **`mj-head` só com `mj-style`.** Testado em 23/10/2026 no editor do Flash (`setComponents` →
  `getHtml()` mantém o `mj-style`; `runCommand('mjml-code-to-html')` compila sem erro e a media query
  vai para o `<head>`). Não testado: salvar e reabrir (o Flash acrescenta o `mj-head` de branding ao
  salvar). Confira o mobile no e-mail de teste. Nada de `mj-font`/webfont.
- **Sem comentários** (`<!-- -->` com `{{ }}` dentro quebra o build; comentário vira lixo no editor).
- Sem webfont: só fontes email-safe (Arial, Helvetica, Georgia, Times New Roman, Verdana, Tahoma,
  Trebuchet MS, Courier New). Stack padrão: `'Helvetica Neue', Helvetica, Arial, sans-serif`, em
  todo `mj-text`/`mj-button` (senão vale o `mj-attributes` de branding do Flash).
- `mj-text` aceita HTML inline (`<strong>`, `<em>`, `<a>`, `<br>`, `<span style>`, `<div style>`).
- CTA sempre `mj-button`, nunca imagem. Texto real, nunca dentro da arte.
- Validar e compilar antes de entregar: `npx -y mjml@4.15.3 --validate x.mjml` e
  `npx -y mjml@4.15.3 x.mjml -o x.html` (o `render.py` faz os dois). HTML final < ~102 KB (Gmail corta).

## 3. Variáveis, condicionais e produtos

> `{{nome_cliente}}` é o **nome completo**. Para "Olá, Maria" use `{{primeiro_nome}}`.

| Contexto | Variáveis | Pode em `fc-if` |
|---|---|---|
| Cliente (qualquer fluxo e campanha) | `primeiro_nome` `nome_cliente` `sobrenome` `email` `telefone` | ✅ |
| Pedido (`fluxo:pedido`) | `numero_pedido` `status_pedido` `url_rastreio` `codigo_rastreio` `transportadora` `status_entrega` | ✅ |
| | `valor_pedido` | — |
| Pagamento (`fluxo:pedido`) | `pix_copia_cola` `boleto_url` `boleto_linha_digitavel` `url_pagamento` | ✅ |
| Cashback (`fluxo:cashback`) | `valor_cashback` `cupom` `data_vencimento` `data_ativacao` `desconto_max` | ✅ |
| | `compra_minima` | — |
| Carrinho (`fluxo:carrinho`) | `carrinho_url` `carrinho_produto_nome` `carrinho_produto_imagem` `carrinho_url_caminho` `produtos_carrinho` | ✅ |
| | `carrinho_total` `carrinho_qtd_itens` `carrinho_frete` | — |
| Links (todos) | `link_optout` ou `unsubscribe_url` (**um dos dois obrigatório no rodapé**) | — |

Fora do contexto do fluxo a variável sai vazia. `%UNSUBSCRIBELINK%` era do formato antigo: não use.

**Seção condicional** (`css-class` na `mj-section`): `fc-if--VARIAVEL` (aparece se tem valor),
`fc-ifnot--VARIAVEL` (aparece se vazia). Saudação padrão: duas seções, `fc-if--primeiro_nome` com
"Oi, {{primeiro_nome}}!" e `fc-ifnot--primeiro_nome` com "Oi!". `fc-nostack` (colunas não
empilham) existe mas não foi testado em envio: prefira `mj-group`.

**Condicional Handlebars** (bloco "Condicional"): `<mj-raw>{{#if x}}</mj-raw>` … `<mj-raw>{{/if}}</mj-raw>`.
O subset de Handlebars levantado no formato antigo: `{{#if}}` só testa vazio/não vazio (não compara
valor); dentro de `{{#each}}` sempre `this.campo`; `{{else}}` dentro de `{{#each}}` vaza como texto;
`@index`, `@root`, `produtos.0.nome`, Liquid e Mustache saem literais.

**Produtos de carrinho/pedido:** blocos nativos "Produtos do Carrinho" / "Produtos do Pedido"
(marcadores `<!-- eb:produtos-carrinho … -->` em `mj-raw`). Recomendação: importar **sem** o bloco e
arrastar o nativo depois do import (garante a config que o painel espera). Fora do fluxo certo o
bloco some do envio sem aviso. Para um card simples do 1º produto: `{{carrinho_produto_imagem}}` +
`{{carrinho_produto_nome}}` numa seção `fc-if--carrinho_produto_imagem`.

## 4. O que vira imagem

Regra: **texto é texto**. Só vira imagem o que e-mail não faz.

| No layout | Como fica |
|---|---|
| Foto, produto, ilustração, elemento girado/com blur, texto em curva | Imagem. Corte onde o fundo é liso para não ter emenda |
| Texto sobre foto ou degradê | apaga o texto (`scripts/remove_text.py` ou polinômio 2D com máscara própria); a imagem limpa vira `background-url` da `mj-section`; texto em `mj-text` por cima |
| Fonte cursiva/display, logo | PNG com alfa, `alt` = o texto. Logo: use o original da loja recolorido |
| Forma simples com texto (ticket, selo, card) | Redesenhe a forma com PIL medindo o original (antialias por supersampling); texto por cima |
| Parte de baixo de um hero (produto/foto) | Imagem normal, cortada onde o fundo é liso |

- **Originais da loja > print.** Packshot e logo da Shopify (`/products/<handle>.json`) em alta, colados
  na posição do layout por template matching: `cv2.matchTemplate(regiao, produto_rgb, cv2.TM_SQDIFF,
  mask=alfa)` varrendo escala (e rotação 90/270 se o packshot está em pé), primeiro no 1x e refinando no
  2x. Packshot com fundo branco: componentes conectados de pixels quase brancos que tocam a borda viram
  transparência.
- `remove_text.py` funciona para fundo **liso** (polinômio 2D; não use `cv2.inpaint`). A regra de "o
  que é texto" dele está calibrada para texto claro em céu azul. Texto escuro em fundo claro: máscara =
  pixels que diferem da mediana da linha (>18 na soma RGB), dilatada.
- Elemento sobreposto a outro (selo encostando no produto, topo de card em cima da foto): fica na
  imagem. Corrija a cor do card no `_recortes.py` para a cor exata do MJML, senão a emenda aparece.
- PNG do Figma vem com o fundo do frame: em degradê aparece caixa. Reexporte transparente ou flood fill
  a partir dos cantos.
- **Modo escuro (Gmail no celular):** escurece os fundos claros das seções, mas não mexe nas imagens, e
  não dá para forçar o modo claro. Imagem com o fundo da seção pintado vira caixa clara. Ícones, selos,
  packshots, cards e combos sobre fundo liso vão em **PNG transparente**: traço fino →
  desmistura do fundo (`alfa = projeção de (fundo − pixel) em (fundo − cor do traço)`); círculo chapado →
  círculo redesenhado como alfa; foto com alfa original → PNG em paleta (`quantize(256, FASTOCTREE)`,
  fica 4-5x menor). Pedaço de card desenhado em cima de uma foto: separe numa faixa PNG com o card
  vazado, numa seção com a cor do card. Confira com uma simulação (troque as cores de fundo do preview
  por cinza-escuro) e veja se sobra alguma caixa.

## 5. Padrões de layout em MJML (o que funcionou)

- **Texto em cima de foto (hero):** `mj-section background-url="…" background-size="cover"
  background-position="center bottom" background-repeat="no-repeat" background-color="<cor do meio>"`.
  O MJML gera o VML do Outlook. A altura da seção = soma dos paddings e line-heights: faça bater com a
  altura da imagem para a emenda com a imagem de baixo ficar invisível (no celular a seção cresce e o
  `cover` segura).
- **Card arredondado em várias seções:** `mj-wrapper` com o fundo de fora e `padding-left/right` (a
  margem do card) + `mj-section` com o fundo do card; `border-radius="0 0 14px 14px"` na última (topo
  pode vir na imagem de cima). Outlook: canto reto.
- **Colunas que não empilham: tabela dentro do bloco HTML, não `mj-group`.** O `mj-group` funciona no
  render local mas **empilhou no Gmail do celular** (teste real do Flash, Latam Fit, 23/10/2026). Célula de
  tabela nenhum cliente empilha:
  `<mj-column><mj-raw><tr><td style="padding:0;" class="fc-html-block"><table role="presentation" width="100%"
  cellpadding="0" cellspacing="0" border="0"><tr><td width="33%" valign="top" align="center" style="width:33.33%;
  font-family:…; font-size:…; color:…">…</td>…</tr></table></td></tr></mj-raw></mj-column>`.
  - Fonte, cor e tamanho no `style` de cada célula (o `mj-raw` não herda nada do `mj-text`).
  - Imagem fluida: `width="N"` + `style="display:block; width:100%; max-width:Npx; height:auto; margin:0 auto"`.
    Assim, mesmo se o cliente descartar o `<style>`, nada estoura a tela.
  - Grupo estreito e centralizado: `<table align="center" width="378" style="width:100%; max-width:378px;
    margin:0 auto">`.
  - Divisor vertical: `border-left:1px solid …` na célula. A altura iguala sozinha.
  - Recuo lateral de texto em **%** (`padding:0 5% 0 12%`), que encolhe com a coluna.
  - Mobile: a classe fica na própria célula/imagem/div (`.cls { font-size:… }`, sem o ` div`).
  - Contrapartida: no editor do Flash essa linha é um bloco HTML (edita no código).
  - Teste extra: renderize uma cópia do preview sem nenhum `<style>` e veja se algo empilha ou estoura.
- **Quebra de linha do layout:** `<br>` só em linha curta (nome, rótulo, endereço). Parágrafo:
  `<div style="max-width:Npx; margin:0 auto;">`, com N calculado para a Arial quebrar onde o layout
  quebra; no celular ele quebra sozinho.
- **Botão de altura fixa:** `line-height` + `inner-padding` (60px = `line-height="24px"` +
  `inner-padding="18px 10px"`), `width` em px.
- **Imagem fluida:** sem `height` (com `height` distorce no celular). Ícone/logo: `width` + `height`.
  Imagem descentralizada no layout: `padding-left` na `mj-image` desloca o centro.
- **Rodapé em 3 colunas (logo | texto | ícone):** tabela no bloco HTML com células em % e
  `valign="middle"`; espaçamento vertical como padding da célula do texto.
- **Mobile = desktop em escala** (pedido do usuário, Latam Fit): nada empilha; linhas lado a lado em
  tabela (acima), e um `mj-style` com
  `@media only screen and (max-width:480px)` reduzindo fontes e espaçamentos (~0,6-0,7 do desktop, texto
  corrido ≥ 12,5px, rótulo ≥ 10px). Onde a `css-class` cai no HTML compilado:
  - `mj-text` / `mj-image` / `mj-button` / `mj-divider` / `mj-spacer`: no `<td>` do elemento. Então
    `.cls { padding-top:… }` muda o espaçamento; `.cls div { font-size:…; line-height:… }` o texto;
    `.cls div div { max-width:… }` o `<div>` de quebra do parágrafo; `.cls table, .cls td { width }` +
    `.cls img { width; height }` a imagem; `.cls table {width}` + `.cls a {width; font-size; padding}`
    o botão; `.cls p { width }` o divisor; `.cls div { height; line-height }` o spacer.
  - `mj-group` / `mj-section`: na `<div>` de fora. `.grupo { width:63% !important }` estreita um grupo.
    O padding da seção fica num `<td>` sem classe: **não dá para mudar**. Ponha o espaçamento vertical
    no padding do primeiro/último elemento (ou numa seção com `mj-spacer`).
  - Imagem descentralizada que tem que encolher: `.cls { padding-left:5% } .cls table { width:65% }
    .cls td { width:auto }`.
  - Segundo degrau `@media only screen and (max-width:359px)` para 320px (rótulo 9px, rodapé 10px).
  - Largura do `max-width` de parágrafo no mobile: meça com PIL (Arial) para a quebra cair onde cai no
    desktop em 360-390px (ex.: 13,5px com 312px).
- Seção sem `background-color` mostra o `mj-body background-color` (útil para a linha legal embaixo
  de um rodapé com cantos arredondados).

## 6. Dimensões

| Item | Padrão |
|---|---|
| Largura | `mj-body width="600px"` |
| Layout | 600px de largura, 1x. Medir com `scripts/medir.py` |
| Imagens | recortadas do 2x (coord. 1x × 2), exibidas em 1x com `width`/`alt` |
| Formato | JPG `quality=88, optimize=True, progressive=True`; PNG para alfa e ícone chapado pequeno |
| Peso | até ~200 KB por imagem; HTML compilado < ~102 KB |
| Fonte | `'Helvetica Neue', Helvetica, Arial, sans-serif`. Condensada: `'Helvetica Neue Condensed', 'Roboto Condensed', 'Arial Narrow', 'Helvetica Neue', Arial, sans-serif` |
| Mobile | `mj-style` com `max-width:480px` (e `359px`); confira em 320, 360, 375 e 390px |
| URLs | absolutas em imagem e link |

## 7. Imagens na Shopify

- Files da loja **da marca** (nunca de outro cliente). Base do CDN: `https://cdn.shopify.com/s/files/1/XXXX/XXXX/XXXX/files/`.
  Lojas conhecidas: PEP = `pep-protein.myshopify.com` (`.../1/0994/1008/4203/files/`, site `https://pepprotein.com.br`);
  Nüma = CDN `.../1/0764/2031/7229/files/` (site `https://sejanuma.com.br`); Repeat = `y1yycy-wg.myshopify.com`
  (`.../1/0780/2290/1980/files/`); Latam Fit = `e11jwv-hs.myshopify.com` (`.../1/0829/8731/9551/files/`).
- Domínio `.myshopify.com` de uma loja nova: `https://<site>/meta.json` (`myshopify_domain`).
- Auth por loja e por máquina: `shopify store auth --store <loja>.myshopify.com --scopes read_files,write_files`
  (em background; o usuário aprova no navegador). `shopify store auth list` mostra as autorizadas. O
  token expira.
- Prefixo `<marca>-<sigla do template>-` em todo arquivo; `check` antes; nunca reenviar com o mesmo
  nome (sobe `-v2`); URL sem `?v=`.
- Domínio para os CTAs: `shop { primaryDomain { url } }` via `shopify store execute`; confirme que a página existe.
