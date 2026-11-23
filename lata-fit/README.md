# E-mails Latam Fit

Formato **MJML** (ver `../CLAUDE.md` e `../FLASHCRM-EMAIL-E-FLUXOS-PARA-DEV.md`): o arquivo entregue é o
`.mjml`, importado no Flash pelo favorito "Importar MJML". O `.html` ao lado é só o MJML compilado (preview e
e-mail de teste), gerado por `python tools/render.py lata-fit/<template>.mjml ...` ou
`npx -y mjml@4.15.3 lata-fit/<template>.mjml -o lata-fit/<template>.html`.

- Loja Shopify: `e11jwv-hs.myshopify.com` (CLI em 04/11/2026 com leitura e escrita de files, orders, customers, products, discounts e inventory) · site `https://www.latamfit.com.br`
- Cupons: são mais de 500 ativos (520 em 04/11/2026). Para procurar um, use `codeDiscountNodeByCode` ou pagine a lista: um `first: 60` parece completo e não é.
- Base do CDN: `https://cdn.shopify.com/s/files/1/0829/8731/9551/files/`
- Instagram `https://www.instagram.com/latam.fit/` · WhatsApp `https://wa.me/5534997121131` (34 99712-1131) ·
  SAC `sac@latamfit.com.br`
- Rodapé legal: endereço do cadastro de cobrança da Shopify = Rua José Elias, 71, sala 116 · Uberlândia/MG ·
  38411-217 (**confirmar**). Razão social e CNPJ: **faltam** (não estão no site nem na Shopify).
- Logo em alta no Files: `latam_fit_rosa2_custom.png` (2480×890, rosa `#cc3b53`, transparente). Nos e-mails ele
  é recolorido pelo `_recortes.py` (o vermelho do layout é `#bf4523`).
- Cores: verde de texto/botão/rodapé `#648247` · logo `#bf4523` · cartão bege `#f1f2e4` · seção `#f8f5f7` ·
  branco `#fefdfd` · rótulos pequenos `#00401f` · divisores `#d6e0c5` · fundo externo do e-mail `#f1f2e4`.
- Prefixos no Files: `lf-lg-` (lançamento Goiabinha), `lf-pb-` (Pré Black), `lf-ca-` (carrinho abandonado), `lf-p30-` (Pré Black 30% OFF, 3 e-mails). `lf-epb-` (e-mail Pré Black refeito em 09/11/2026, na **turbo-starter**).

## lancamento-goiabinha.mjml

"A Goiabinha ganhou chocolate branco!" (e-mail de campanha, sem variável além do `{{link_optout}}`). Layout de
origem: `email-que-deve-ser-copiado/EMAIL 01 - LANÇAMENTO GOIABINHA COM CHOCOLATE BRANCO_.png` (600×2471), com os
recortes `emial-mkt-latam_01..07.png` (as mesmas faixas do PNG inteiro).

**O xadrez em volta do layout não é do design**: é o fundo de transparência do visualizador onde o PNG foi
printado. O e-mail é só o cartão de x 13-587 / y 5-2456 (575px), escalado para 600px em
`assets/lancamento-goiabinha/_design.png` e para 2x (Real-ESRGAN) em `_design-2x.png`. Coordenadas abaixo são do
`_design.png` (1x). Os recortes saem do `assets/lancamento-goiabinha/_recortes.py`.

Fotos de produto e logo vêm dos **originais da loja** (`assets/lancamento-goiabinha/_fontes/`), não do print 1x,
e são encaixadas na posição do layout por template matching:

| Arquivo (prefixo `lf-lg-`, já no Files) | Linhas do 1x | Uso |
|---|---|---|
| `hero-fundo.jpg` | 0–365 | fundo verde do hero **sem texto** (apagado com polinômio 2D). `background-url` da 1ª `mj-section` (`cover`, `center bottom`, cor `#c3dc9a`). Logo, título, divisor e parágrafo vão por cima |
| `logo.png` | 54–90 | logo da loja recolorido `#bf4523`, com alfa (123×37) |
| `hero-produto.jpg` | 366–674 | foto do produto + selo "Lançamento" + topo arredondado do cartão bege (redesenhado nítido) |
| `icone-1..4.png` | 768–815 | ícones verdes do "Por que você vai gostar" (48×48, fundo `#f1f2e4`) |
| `card-1..3.jpg` | 1052–1242 | um card por coluna (x 0-200, 200-400, 400-600; redesenhados com a sombra interna do topo): barra com chocolate (`BarraPedeMolequeZero.png`, fundo branco removido), barra zero (`cocada_com_abacaxi_2.png`) e pote de goiabada de colher, todos da loja |
| `combo.jpg` | 1779–2195 | `Combo_Goiabada.png` da loja (com o selo "Leve 1 caixa grátis"), 390×417, centrado em x 315 como no layout (`padding-left="30px"`) |
| `selo-1..3.png` | 2212–2315 | frete grátis / direto da fábrica / Pix (104×104) |
| `logo-branco.png` | rodapé | logo branco com alfa (100×30) |
| `instagram.png` | rodapé | ícone do Instagram (60×60, fundo `#648247`) |
| `produtos.jpg` | — | os 3 cards numa imagem só, da 1ª versão (HTML). Não é usado |

**Modo escuro (em uso desde 23/10/2026, arquivos `-v2`):** o Gmail do celular no modo escuro escurece os fundos
claros mas não as imagens, e o fundo pintado nelas virava caixa branca (print do usuário). Não dá para forçar o
fundo claro no Gmail. Então as imagens que ficam sobre fundo liso viraram PNG transparente, e o modo claro ficou
idêntico: `icone-1..4-v2.png` (círculo com alfa), `selo-1..3-v2.png` e `instagram-v2.png` (traço desmisturado do
fundo), `card-1..3-v2.png` e `combo-v2.png` (PNG em paleta com alfa, 17 KB e 77 KB). O hero de baixo virou
`hero-produto-v2.jpg` (1x 366-655) + `hero-borda.png` (656-674): o topo arredondado do cartão bege é
transparente, numa seção `#f1f2e4`, e escurece junto com o cartão. As versões sem `-v2` (e `hero-produto.jpg`)
continuam no Files, mas não são usadas.

Estrutura do MJML:
- Hero: `mj-section` com `background-url`; altura (54 + 37 + 35 + 114 + 20 + 2 + 24 + 80 = 366) igual à da imagem,
  para emendar sem marca com `hero-produto.jpg`. O parágrafo usa `<div style="max-width:390px">` para quebrar
  como no layout no desktop e sozinho no celular.
- **As 4 linhas lado a lado são tabelas no bloco HTML** (`mj-raw` com `fc-html-block`), não `mj-group`: no Gmail
  do celular do usuário o `mj-group` empilhou (teste do Flash, 23/10/2026). Imagens com `width:100%; max-width`
  (nada estoura nem sem CSS; conferido renderizando sem `<style>`). No editor do Flash essas 4 linhas são blocos
  HTML.
- "Por que você vai gostar": `mj-wrapper` (fundo `#f8f5f7`, margem 17/16) com a seção do título, a seção da tabela
  de 4 células (25,09 / 25,27 / 22,89 / 26,75%, `border-left` de 1px) e uma seção com `mj-spacer` e
  `border-radius="0 0 14px 14px"`.
- Produtos: tabela de 3 células, cada uma com card, nome e descrição. O recuo lateral do texto é em % (centraliza
  sob o card e encolhe com a coluna).
- Benefícios: tabela centralizada de 378px (`max-width`), 3 células.
- Rodapé verde: tabela de 3 células `valign="middle"` (19,33 / 60,41 / 20,26%), seção com
  `border-radius="0 0 12px 12px"`. Embaixo, seção sem fundo com endereço, SAC e `{{link_optout}}`.
- O espaçamento vertical fica no padding dos elementos (não das seções) para o mobile poder mudar; a base do card
  "Por que você vai gostar" é uma seção com `mj-spacer`.

**Mobile = desktop em escala** (pedido do usuário): nada empilha. `mj-style` com
`@media only screen and (max-width:480px)` e classes `lf-*`: título do hero 26px (2 linhas), parágrafo 13,5px com
`max-width:312px` (quebra igual ao desktop em 360-390px), títulos 22px, rótulos 10px, descrições 11px, botão
180×44, combo a 65% da largura, selos 66px, rodapé 11px. `max-width:359px` (320px): rótulos 9px, descrições e
rodapé 10px, logo do rodapé 48px. Conferido em 320, 360, 375 e 390px.

Fonte: Helvetica/Arial (sem webfont no Flash). A fonte do layout é mais pesada: os títulos bold têm
`letter-spacing="-0.5px"` e ainda ficam um pouco mais leves que no design.

Links:
- Hero, cards de produto, botão e combo → `https://www.latamfit.com.br/collections/goiabinhas/products/combo-goiabada-zero-acucar-barrinha-de-goiabada-e-goiabada-cremosa-em-pote` (pedido do usuário).
- Logos → home. WhatsApp do rodapé → `wa.me`. Ícone → Instagram. SAC → `mailto:`.

Assunto sugerido: "A Goiabinha ganhou chocolate branco! 🍫" · Pré-header: "A goiabinha macia que você já
conhece, agora com cobertura sabor chocolate branco e zero adição de açúcares." (os dois vão no passo da campanha/fluxo).

Pendências / perguntar:
- Razão social e CNPJ para o rodapé; confirmar o endereço.
- O 1º card diz "Goiabinha · a clássica" mas a imagem é da Goiabinha **com chocolate** (igual ao layout).

## pre-black.mjml

"Pré Black" (e-mail 3 da campanha, sem variável além do `{{link_optout}}`). Layout de origem:
`email-novo/PRÉ BLACK - EMAIL 3 COMPLETO.png` (600×2727, copiado para `assets/pre-black/_layout.png`), com os
recortes do designer `email-mkt-latam-3_01..08.png` (as mesmas faixas).

**Moldura xadrez:** aqui ela é do design (PNG opaco, xadrez ondulado azul `#91c6dc` / creme `#faf6ec`), não
transparência do visualizador; provavelmente a verde do Goiabinha também era. Seguindo o Goiabinha (já enviado
assim), o e-mail é só o cartão: x 13-587 / y 12-2705 (575px) em `_card.png`, escalado para 600px em `_design.png`;
`_design-2x.png` = Real-ESRGAN 4x do `_card.png` reduzido para 1200px. Corpo do e-mail `#faf6ec`. O topo do cartão
(arredondado no layout) ficou reto. Coordenadas abaixo: 1x do `_design.png`. Recortes em `assets/pre-black/_recortes.py`.

| Arquivo (prefixo `lf-pb-`, já no Files) | Linhas do 1x | Uso |
|---|---|---|
| `hero-topo.jpg` | 0–232 | barrinhas dos cantos + selo "PRÉ" + logo + "BLACK" (fonte display: imagem, `alt="Pré Black Latam Fit"`). Fundo `#f2f2f2` limpo; logo = original da loja recolorido `#bf4523`, por template matching |
| `produtos.jpg` | 400–880 | barrinhas voando + selo "30% OFF". Fundo é degradê `#f2f2f2` → `#f9faf9`: acertado linha a linha para emendar sem marca com o parágrafo (em cima) e o cupom (embaixo); a sombra vai até a caixa do cupom |
| `icone-1..4.png` | 1221–1277 | sem lactose / sem glúten / veganas / proteicas, 64×56, traço marrom `#6e2e1e` desmisturado do branco (alfa) |
| `caixas-mistas.png` | 1400–1832, x 337–600 | pilha de barrinhas da direita, PNG em paleta com alfa (fundo `#f9faf9` liso → transparente; modo escuro) |
| `combo.png` | 1892–2312, x 0–254 | pilha da esquerda, idem |
| `lf-lg-logo-branco.png`, `lf-lg-instagram-v2.png` | rodapé | reaproveitados do Goiabinha (cópias locais só para o preview) |

Texto real: parágrafo e botão do hero, cupom inteiro (`PREBLACK` em `mj-text`, 78px bold, `letter-spacing -3.5px`),
títulos marrons `#6e2e1e`, rótulos dos ícones, as duas colunas de texto, botões e rodapé. Cores: roxo do botão
`#5d3795`, rosa `#e8345c`, caixa do cupom e rodapé `#91c6dc`, texto do hero `#2f2f2f`, texto cinza `#424242`.

Estrutura: card dos ícones e as duas linhas lado a lado ("Quer provar" / "Já sabe") são tabelas no bloco HTML
(`mj-raw`), com células e recuos em % e o card branco como tabela de 78% (`max-width:468px`), então escalam
juntos no celular. Cupom = `mj-wrapper` (margens 44/46) + `mj-section` `border-radius 18px`. Rodapé igual ao do
Goiabinha (azul, 18,62 / 62,20 / 19,18%). Mobile = desktop em escala: `max-width:480px` (classes `pb-*`), degrau
`374px` (parágrafos das colunas a 12px para quebrar igual em 360) e `359px`. Conferido em 320/360/375/390 e sem
`<style>` (nada estoura nem empilha). Render alinhado com o layout (deslocamento vertical 0).

Links:
- Hero, produtos e "MONTAR MINHA LISTA" → `/collections/all`.
- Ícones → `/collections/frontpage` (é a coleção "Sem Lactose"), `/sem-gluten`, `/vegano`, `/com-proteina`.
- Caixas mistas → `/collections/caixas-mistas`; "Caixa Mista Rosa"/"Latam Protein" no texto → página de cada produto.
- Combo e "MONTAR MEU COMBO" → `/collections/monte-sua-caixa` (os 3 "Monte seu combo").
- Conferidos pelo Admin (existem, ativos, com produtos); o site devolveu 429 para o script em 30/10, abrir antes de enviar.

Cupom na Shopify: `PREBLACK` existe, **30% no pedido inteiro, ativo de 28/10/2026 08:00 a 15/11/2026 23:30** (horário
de Brasília).

Assunto sugerido: "Começou o Pré Black: 30% OFF com o cupom PREBLACK" · Pré-header: "Anota o cupom e deixa a sua
lista pronta. Vale para o pedido inteiro."

Pendências / perguntar:
- "Vale a partir de segunda, 26/10." está como no layout, mas o cupom começou em 28/10 (quarta) e já está ativo;
  sugestão: "Válido até 15/11."
- "Coloque na agenda!" não tem nada embaixo no layout (parece faltar as datas). Ficou igual.
- Moldura xadrez: de fora, como no Goiabinha. Dá para pôr de volta como fundo, se quiserem.
- Fotos das barrinhas = upscale do print 1x (letra miúda das embalagens não fica nítida). Export 2x do Figma melhora.
- Ideia não feita: CTAs com `/discount/PREBLACK?redirect=/collections/all` (aplica o cupom sozinho).
- Razão social e CNPJ do rodapé (mesma pendência do Goiabinha).
- `mj-style`, `mj-group`, `border-radius` por canto e `background-url` passaram no import + compilação do editor do
  Flash (teste sem salvar, 23/10/2026); salvar e o envio real não foram testados (os
  templates da Repeat não usam). Conferir no editor e no e-mail de teste.

## carrinho-abandonado.mjml (1 de 3)

1º e-mail da régua de carrinho abandonado, sem cupom. Os outros dois estão na seção seguinte. **Sem layout do Figma**: design feito a partir da identidade do Goiabinha
(verde, cartão bege, rodapé verde), porque o tema azul/roxo do Pré Black é de campanha. Imagens geradas em
`assets/carrinho-abandonado/_recortes.py` a partir dos packshots da loja (`_fontes/`, com alfa). Previews com dados
de exemplo em `_preview-desktop.png` e `_preview-mobile.png` (320/360/375/390).

| Arquivo | Exibição | Uso |
|---|---|---|
| `lf-ca-hero-fundo.jpg` | 600×336 | `background-url` da 1ª seção: degradê só vertical (emenda igual em qualquer largura). Logo, título, divisor e parágrafo por cima |
| `lf-ca-hero-produtos.jpg` | 600×286 | 5 barrinhas em leque (Bananita + Amendoim, Cocada com chocolate, Wafer Morango, Goiabinha Zero, Wafer Cookies), recortadas dos packshots de 2-3 barras, com sombra |
| `lf-ca-hero-borda.png` | 600×19 | fim do degradê com o topo arredondado do cartão vazado (modo escuro: o cartão escurece junto) |
| `lf-lg-logo`, `lf-lg-logo-branco`, `lf-lg-selo-1..3-v2`, `lf-lg-instagram-v2` | | reaproveitados do Goiabinha (cópias locais só para o preview) |

Estrutura:
- **Cartão bege sem `mj-wrapper`:** seções de primeiro nível com fundo `#f8f5f7`, padding lateral 17/16 e
  `mj-column background-color="#f1f2e4"`. Motivo: `fc-if--` só foi visto em seção de primeiro nível (blocos do Flash e
  templates da Repeat); dentro de `mj-wrapper` não foi testado, e se falhasse sairiam "Oi, Ana!" e "Oi!" juntos.
- Condicionais: `fc-if`/`fc-ifnot--primeiro_nome` (saudação) e `fc-if`/`fc-ifnot--carrinho_produto_imagem` (linha do
  produto, ou "Seu carrinho continua do jeitinho que você deixou." se vier sem imagem).
- Linha do produto: tabela no bloco HTML (`mj-raw`): imagem à esquerda, nome + `{{carrinho_qtd_itens}}` +
  `{{carrinho_total}}` à direita, sem empilhar. Mostra só o 1º produto; "Itens no carrinho" conta o resto. Para listar
  todos: bloco nativo "Produtos do Carrinho", arrastado depois do import.
- Mobile = desktop em escala (classes `ca-*`, degraus 480 e 359). Conferido em 320/360/375/390, com nome de produto
  longo, sem nome/imagem, sem `<style>` (nada empilha nem estoura) e na simulação de modo escuro (sem caixa clara).

Links: hero, foto do produto e os 2 botões → `{{carrinho_url}}`. WhatsApp → `wa.me`. Logos → home. Ícone → Instagram.

Selos conferidos no site em 04/11/2026: "Frete grátis acima de R$99", "Até 3x sem juros", "Direto da Fábrica". Pix não
apareceu no texto da home (vem do layout do Goiabinha).

Assunto sugerido: "Seu lanche ficou no carrinho" · Pré-header: "Faltou só um passo para o seu pedido sair. É só voltar
e finalizar."

Pendências / perguntar:
- **Plano do Flash:** em 30/10 as 9 automações da conta estavam inativas porque o plano não permite automação (ver
  `D:\Turbo\latam fit\CLAUDE.md`). Sem isso, a régua não dispara.
- Formato de `{{carrinho_total}}` (se já vem com "R$") e `{{carrinho_produto_imagem}}` dentro do `mj-raw`: não conferidos
  em envio real. Fora do fluxo as variáveis saem vazias, então o e-mail de teste pode não mostrar a linha do produto.
- Razão social e CNPJ do rodapé (mesma pendência dos outros; não estão na home nem nos termos do site).

## carrinho-abandonado-10off.mjml e carrinho-abandonado-15off.mjml (2 e 3 de 3)

Regra passada pelo usuário em 04/11/2026: "enviava o primeiro email, após 2 hrs o segundo com 10 e depois um terceiro com
15%. Se formos enviar só um podemos já colocar o cupom." Se for um só, use o de 10% (o texto não cita e-mail anterior).

| E-mail | Espera | Título | Cupom | Assunto sugerido | Pré-header sugerido |
|---|---|---|---|---|---|
| `carrinho-abandonado` | a definir | Seu lanche ficou no carrinho! | nenhum | Seu lanche ficou no carrinho | Faltou só um passo para o seu pedido sair. É só voltar e finalizar. |
| `-10off` | 2 h depois do 1º | Seu carrinho ganhou 10% OFF! | `CARRINHO10` | Seu carrinho ganhou 10% OFF | Use o cupom CARRINHO10 e finalize o seu pedido. |
| `-15off` | a definir | Seu desconto subiu para 15% OFF! | `CARRINHO15` | Seu desconto subiu para 15% OFF | Use o cupom CARRINHO15 e finalize o seu pedido. |

Cupons (já existiam na loja, **não foram criados nem alterados**; lidos em 04/11/2026, os dois com 0 usos):
| Código | Desconto | Vale para | Mínimo | Por cliente | Validade | Combina com |
|---|---|---|---|---|---|---|
| `CARRINHO10` | 10% | pedido inteiro, todos os clientes | não | **sem limite** | desde 21/09/2026, sem fim | nada |
| `CARRINHO15` | 15% | pedido inteiro, todos os clientes | não | um uso | desde 22/10/2026, sem fim | nada |

Mesmo layout e imagens do 1º e-mail (nada novo no Files). O que muda: título com o desconto em `#bf4523`, parágrafo, "Total
sem cupom" (`{{carrinho_total}}` é o valor antes do desconto), botão "FINALIZAR COM X% OFF" e o cupom: tabela no bloco HTML
(`mj-raw`), borda tracejada, código em texto real para poder copiar. A borda arredondada precisa de `border-collapse:separate`
(o reset do MJML colapsa e deixa o canto reto). Base do código 38px: com 46px estourava o cartão sem `<style>`. Conferido em
320/360/375/390, nome longo, sem dados, sem `<style>` e na simulação de modo escuro. A simulação só escurece fundos, não
clareia texto como o Gmail: os textos `#00401f` ficam apagados nela. Conferir o modo escuro de verdade no celular.

**Sem falsa urgência:** os cupons não têm data de fim, então o texto não diz "última chance" nem "só hoje". Também não diz
"maior desconto", porque o `PREBLACK` (30%) está no ar até 15/11/2026.

Pendências / perguntar:
- **Quando sai o 3º e-mail e quanto tempo esperar antes do 1º:** o usuário só passou as 2 h entre o 1º e o 2º.
- **`CARRINHO10` sem limite por cliente**, ao contrário do `CARRINHO15`. Não alterei; sugestão: um uso por cliente.
- **O cupom não aplica sozinho:** `{{carrinho_url}}` é URL completa. Mesmo caso da Repeat. Testar num envio real
  `https://www.latamfit.com.br/discount/CARRINHO10?redirect={{carrinho_url_caminho}}`.
- **Até 15/11 o `PREBLACK` (30%) vale mais que os dois.** E quem tem o "Monte seu combo" (20% automático) no carrinho não
  acumula: por isso o aviso "Não acumula com outras promoções" no cupom.
- **Frete grátis:** não é desconto automático nem de código (só `EXPERIMENTA1` e `FRETE1` são de frete), então deve ser regra
  de frete, que não dá para ler sem o escopo `read_shipping`. Testar um pedido pouco acima de R$ 99: com o cupom o total
  pode cair abaixo do mínimo.
- **Fluxo no Flash:** colocar a condição "sem pedido" antes de cada e-mail e `permitir_reentrada: false`, porque o `CARRINHO15`
  é de um uso por cliente (como no fluxo da Repeat). Não criado: falta o OK do usuário.

## pre-black-30off-1.mjml, -2.mjml e -3.mjml

Pré Black "30% OFF no site todo" com o cupom `PREBLACK`, em três versões do mesmo layout (sem variável além do
`{{link_optout}}`). Layouts no Figma `eoBcJ0dDWQb9SLDOgFzM8P` ("Latam Fit (Copy)"), frames "E-mail preblack":

| Arquivo | Frame | O que muda |
|---|---|---|
| `pre-black-30off-1` | `16001:8889` | Caixa Surpresa "De R$ 139 por R$ 97,30 com cupom" |
| `pre-black-30off-2` | `16005:2` | Caixa Surpresa "De R$ 210 por R$ 139,00 com cupom" |
| `pre-black-30off-3` | `16005:192` | sem o bloco da Caixa Surpresa |

**Os três saem de `assets/pre-black-30off/_montar.py`**: ajuste lá e rode de novo (`python lata-fit/assets/pre-black-30off/_montar.py`),
senão as versões se desencontram. Recortes em `_recortes.py`. Exports 2x do Figma (render vetorial, sem upscale) e imagens
originais em `assets/pre-black-30off/_figma/` (`e1/e2/e3-export-2x.png`, `-1x.png` = layouts de comparação).

| Arquivo (prefixo `lf-p30-`, no Files) | Exibição | Uso |
|---|---|---|
| `ondas.jpg` | 600×302 (2x) | fundo de ondas rosa/creme do `mj-wrapper` (repete na vertical, `background-size 600px auto`). O padrão original não é periódico: a emenda é um corte de custo mínimo |
| `hero.jpg` | 568×501 | foto dos produtos + selo "30% OFF" (1x y 676-1177). As primeiras linhas viram o rosa `#f4a8c4` chapado para emendar com a seção |
| `caixa.jpg` | 568×634 | foto da Caixa Surpresa (texto "PAGUE R$ 139 LEVE + DE R$ 210" é da foto) |
| `card-1..4.png` | 270×190 | topo de cada card dos queridinhos (degradê radial refeito pela fórmula do Figma + produto + selo), cantos de cima vazados. O nome do produto vai em célula com cor chapada (`#f1ddc8`, `#f7cfde`, `#f5e7a3`, `#c4e2f9`) e o degradê vai para essa cor nas últimas 22px |
| `icone-1..4.png` | 64×64 | sem lactose / sem glúten / proteína / veganas, círculo `#f3a7c4` com alfa |
| `logo.png`, `logo-rodape.png`, `instagram.png` | 106×32, 211×64, 48×48 | SVGs do Figma renderizados no Chrome com fundo transparente |

Texto real: tudo o resto, incluindo os dois cupons (borda tracejada), o "ticket" de preço (CSS puro: recortes laterais e
picotes de cima/baixo são `div` com `border-radius`; no Outlook vira retângulo) e os nomes dos produtos. Fonte do layout é DM Sans
+ Bricolage Grotesque; aqui Helvetica/Arial bold com `letter-spacing` ajustado para a largura bater. Cores: marrom `#5a2a1e`,
vermelho `#c8365a`, rosa do cartão `#f4a8c4`, amarelo `#f6e77e`, creme `#f8f3e7`, branco `#fefdfd`, borda do ticket `#e8dec5`.

Estrutura: topo creme → `mj-wrapper` com o fundo de ondas (margens 16, topo 20, base 40/16/23 como em cada layout) e as seções do
cartão (rosa com raio 32 em cima, cupom branco, Caixa Surpresa com raio 32 embaixo) → queridinhos (grade 2×2 em tabela no bloco
HTML) → "Encontre o seu favorito" (4 ícones em tabela) → faixa vermelha → rodapé marrom com logo, Instagram e a linha legal
(endereço, SAC, `{{link_optout}}`; não está no layout, o Flash exige). Mobile = desktop em escala (classes `p30-*`, degraus 480
e 359). Conferido em 320/360/375/390 e alinhado com o layout no desktop (o `render.py` corta em x=100, mas nesse print o corpo
começa em x=92: para comparar, recorte a partir da posição do logo).

Links (conferidos pelo Admin em 05/11/2026: produtos ativos e publicados, coleções existem):
- Hero, "APROVEITAR 30% OFF", "COMPRAR COM O CUPOM" → `/collections/all`.
- Foto e botão da Caixa Surpresa → `/products/caixa-surpresa` (R$ 139, 124 em estoque).
- Cards → Cocada com Chocolate Zero 300g, Goiabinha Zero 264g, Wafer Cookie & Cream 300g; "VER OS MAIS VENDIDOS" → `/collections/mais-vendidos`.
- Ícones → `/collections/frontpage` (Sem Lactose), `/sem-gluten`, `/com-proteina`, `/vegano`.

Cupom: `PREBLACK` existe (30%, todos os produtos, 28/10 08:00 a 15/11 23:30, sem limite por cliente). Não criei nem alterei cupom.

Assuntos sugeridos: (1) "30% OFF no site todo + Caixa Surpresa por R$ 97,30" · (2) "Pré Black: Caixa Surpresa com mais de R$ 210
em produtos" · (3) "Pré Black Latam Fit: 30% OFF no site todo". Pré-header: "Use o cupom PREBLACK até 15/11. Doces zero adição de
açúcares, wafers com proteína, caixas e combos."

Pendências / perguntar:
- **E-mail 2:** "por R$ 139,00 com cupom", mas a Caixa Surpresa já custa R$ 139 sem cupom; com o `PREBLACK` sai R$ 97,30 (é o
  e-mail 1). Ou o texto perde o "com cupom", ou existe outro cupom para ela. No parágrafo, "pagando apenas 139,00" virou "R$ 139,00.".
- O 3º card repete a Cocada com Chocolate (igual ao layout). Trocar por outro produto?
- Razão social e CNPJ do rodapé (mesma pendência dos outros).
- Modo escuro do Gmail: a célula do nome nos cards e os fundos escurecem, as imagens não (topo do card pastel, base escura;
  foto do hero com o rosa dela). Alternativa: nome do produto fora do card, embaixo.
- Sem `<style>` (cliente que descarta CSS) o cupom com a pílula e os botões não cabem abaixo de ~470px.
- Ideia não feita: CTAs com `/discount/PREBLACK?redirect=/collections/all` (aplica o cupom sozinho).

## email-preblack.mjml (09/11/2026)

- Refeito a pedido do usuário a partir do Figma `16001:8889`, o mesmo layout do `pre-black-30off-1` (o export 2x saiu idêntico).
- Sai de `assets/email-preblack/_recortes.py` + `_montar.py` (cópias dos scripts do `pre-black-30off`, só com outro prefixo e CDN).
- Imagens no Files da `turbo-starter.myshopify.com` (não da loja da Latam Fit), prefixo `lf-epb-`, 14 arquivos, todos 200.
- Mesmas pendências do `pre-black-30off-1`: o 3º card repete a Cocada (está assim no Figma), CNPJ no rodapé.
