# E-mails PEP

Mesmo pipeline e mesmas regras dos e-mails Nüma: veja `../numa/README.md` (Handlebars subset, MJML, HTML de e-mail).

> **Formato antigo (out/2026).** Os templates daqui são HTML para o bloco "HTML" do Flash, com
> `%UNSUBSCRIBELINK%` no rodapé. Templates novos são **MJML** com `{{link_optout}}` (ver `../CLAUDE.md`).
> Ao refazer um destes, migre; antes de ativar algum, confira num e-mail de teste se o descadastro funciona.

## boas-vindas.html

Design original: `boas vindas - completo_.png` (600×1944, 1x). Os assets foram gerados em 2x
com Real-ESRGAN (`realesrgan-ncnn-vulkan`, modelo `realesrgan-x4plus`: 4x e depois reduzido
com Lanczos para 1200px). Texto grande fica nítido, mas as letrinhas miúdas dos rótulos das
latas viram rabisco (já eram ilegíveis no original). Se vier export 2x do Figma, recorta de novo
com as mesmas coordenadas ×2.

| Arquivo em `assets/boas-vindas/` | Uso |
|---|---|
| `pep-bv-hero-ceu.jpg` | metade de cima do hero, **sem o título** (removido com OpenCV + degradê reconstruído). Vai como `background` do `<td>`, com VML pro Outlook e `bgcolor #0476ce` de fallback |
| `pep-bv-de-conhecer.png` | o script "de conhecer" com fundo transparente (fonte cursiva não existe em e-mail) |
| `pep-bv-hero-latas.jpg` | metade de baixo do hero (balde + latas) |
| `pep-bv-hero.jpg` | hero antigo com o título na imagem — não é mais usado, ficou de backup (também está no Files da loja) |
| `pep-bv-cupom-vazio.png` | ticket **sem o código**, redesenhado em Python com as medidas do original. Vai como `background` (VML no Outlook, `bgcolor #f35524` de fallback) e o `PRIMEIRA10` é texto por cima — pra trocar o cupom, é só editar o texto |
| `pep-bv-cupom.png` | ticket antigo com o código na imagem — não é mais usado, backup |
| `pep-bv-latas.jpg` | as três latas + ícones de fruta |
| `pep-bv-mao.png` | mãozinha do botão (já com o laranja #f35524 de fundo) |

Os demais elementos são HTML: título "Hora de provar / o que você acabou", "E aí, vai ficar de fora?", código do cupom, texto, divisor, "10% OFF", botões (com VML pro Outlook) e pílulas.

Imagens no Files da loja **pep-protein** (`https://cdn.shopify.com/s/files/1/0994/1008/4203/files/`), subidas via `shopify store auth` + `store execute` (stagedUploadsCreate → fileCreate). Links apontam para `https://pepprotein.com.br/collections/all`.

Placeholder a preencher:
- `%UNSUBSCRIBELINK%` → rodapé de descadastro (não está no design, mas é obrigatório)

Cores: fundo `#fffcf0` · verde `#277217` · laranja `#f35524` · divisor `#480d11`.

## ultimas-24h.html

Último aviso do cupom `VOLTAR10` ("Últimas 24 horas"). Design original:
`d:/Downloads/email-completo (3).jpg` (600×1688, 1x), cópia em `assets/ultimas-24h/_design.jpg`.
Os recortes saem do `_design-2x.png` pelo `assets/ultimas-24h/_recortes.py` (roda de novo se vier
export 2x do Figma: é só substituir o `_design-2x.png`).

| Arquivo em `assets/ultimas-24h/` | Uso |
|---|---|
| `pep-u24-logo.png` | logo PEP, verde com alfa (97×45) |
| `pep-u24-24horas.png` | "24 horas" cursivo, laranja com alfa (206×44), `alt="24 horas"` |
| `pep-u24-balde.jpg` | latas no balde de gelo (600×343). Termina exatamente onde começa o card verde |
| `pep-u24-latas.jpg` | três latas no chão cinza (600×448). O rodapé continua o cinza (`#dde0e6`) |
| `pep-bv-mao.png` | cópia local da mãozinha do boas-vindas, só pro preview (no HTML usa a URL já existente) |

É HTML: "Últimas", subtítulo, o card verde (`border-radius:115px`; no Outlook fica com canto reto),
"Use o cupom", a caixa do `VOLTAR10` (borda 2px), o "*10% OFF…" e o botão (VML no Outlook).
CTAs → `https://pepprotein.com.br/collections/all`. Placeholder: `%UNSUBSCRIBELINK%`.

## carrinho-abandonado.html

"Você leu o rótulo e o rótulo passou no teste". Design original:
`d:/Downloads/email-completo (1).jpg` (600×2476, 1x), cópia em `assets/carrinho-abandonado/_design.jpg`
e upscale em `_design-2x.png`. Todos os CTAs e imagens clicáveis → `{{carrinho_url}}`.

| Arquivo em `assets/carrinho-abandonado/` (prefixo `pep-ca-`, já no Files) | Linhas do 1x | Uso |
|---|---|---|
| `pep-ca-hero.jpg` | 0–664 | hero inteiro: logo, título com contorno (display, não dá em HTML), latas e a curva branca |
| `pep-ca-faixa-latas.jpg` | 927–1131 | pílula verde com as três latas |
| `pep-ca-titulo-lata.jpg` | 1290–1462 | adesivo "O que está esperando por você na lata:" (texto com contorno + raios) |
| `pep-ca-lata.jpg` | 1510–1835 | lata inclinada + framboesas **com as pílulas "Zero açúcar" e "86 kcal" na imagem**: elas encostam na lata e e-mail não tem posicionamento absoluto. No mobile essas duas ficam pequenas (~9px) |
| `pep-ca-latas-card.jpg` | 2340–2476 | latas saindo do card verde. A tampa da lata do meio ficava **na frente** do botão: o resto do botão foi pintado de verde e a imagem entra logo abaixo do botão HTML (e-mail fica 14px mais alto que o design). Os primeiros px da curva do card foram suavizados para emendar no card HTML de largura cheia |
| `pep-bv-mao.png` | — | mãozinha: reaproveitada do boas-vindas (mesma URL) |

É HTML: os dois blocos de texto (19.5px/22.5px, quebras batendo com o design), os dois botões
(o do card tem borda branca 3px), as pílulas "20g de Whey Isolado" e "+ Gaseificação…", e o card
verde (`border-radius:60px 60px 0 0`; no mobile a margem lateral é 7.67% para alinhar com a imagem
de baixo). Placeholder: `%UNSUBSCRIBELINK%`.

## pos-compra-inativo.html

"Já faz um tempo desde a última entrega" (cliente que comprou e sumiu, cupom `PEP10`). Design
original: `d:/Downloads/Pós-compra - inativo.png` (600×2283, 1x), cópia em
`assets/pos-compra-inativo/_design.png`. Recortes pelo `_recortes.py` a partir do `_design-2x.png`.

| Arquivo em `assets/pos-compra-inativo/` (prefixo `pep-pci-`) | Linhas do 1x | Uso |
|---|---|---|
| `pep-pci-hero-ceu.jpg` | 0–320 | céu + logo, **sem o título** (convolução normalizada em volta das letras; o céu tem nuvens finas e o polinômio do `remove_text.py` deixava manchas). `background` do `<td>`, VML no Outlook, `bgcolor #4f9ad6` |
| `pep-pci-ultima-entrega.png` | 232–298 | "última entrega" cursivo, `#daf9ac` com alfa (378×66) |
| `pep-pci-hero-latas.jpg` | 320–811 | latas voando no céu |
| `pep-pci-latas.jpg` | 1589–2283 | latas nos blocos coloridos (começa logo abaixo do botão) |
| `pep-bv-mao.png` | — | mãozinha: reaproveitada do boas-vindas (mesma URL) |

É HTML: título, textos, divisor, a caixa "10% OFF…", o `PEP10` (Arial Black) e o card. O card é
uma tabela de 3 colunas (69 | 372 | 69): o laranja tem `rowspan=2` e as células laterais da 2ª
linha levam só `border-top` + `border-left/right` com raio 40px, o que desenha o topo do card
"passando por trás" do laranja. No Outlook os cantos ficam retos. O botão fica metade no creme e
metade no branco da foto: a linha dele tem `linear-gradient(#fffcf0 8px, #ffffff 8px)` (fallback
branco). No mobile o céu usa `background-size:100% auto` para emendar certinho com as latas.

⚠️ O design diz "10% OFF **na sua primeira compra**", mas o e-mail vai para quem já comprou.
Mantido igual ao design; confirmar o texto com o cliente. CTA → `https://pepprotein.com.br/collections/all`.
Placeholder: `%UNSUBSCRIBELINK%`.

## depoimentos.html

"Você ainda não provou? Eles já, e te contam melhor..." (carrinho com prova social + cupom
`VOLTAR10`). Design original: `d:/Downloads/email-completo (2).jpg` (600×2517, 1x), cópia em
`assets/depoimentos/_design.png` e upscale em `_design-2x.png`. Hero e carrinho → `{{carrinho_url}}`.

| Arquivo em `assets/depoimentos/` (prefixo `pep-dep-`, já no Files) | Recorte do 1x (x, y) | Uso |
|---|---|---|
| `pep-dep-hero.jpg` | 0–600, 0–783 | logo, mãos com latas e os adesivos girados |
| `pep-dep-braco.jpg` | 480–600, 783–840 | ponta do braço que invade o 1º parágrafo: `background` do `<td>` do texto, alinhado em cima/direita. Some no mobile (`.braco`) e no Outlook |
| `pep-dep-verde-topo.png` | 0–600, 1063–1100 | topo arredondado do bloco verde + tampa da lata |
| `pep-dep-verde-esq.jpg` / `-dir.jpg` | 0–110 / 482–600, 1100–1697 | laterais do bloco com as latas vazando. O miolo (110–482) é `<td bgcolor="#277217">` com fotos + texto em HTML, altura fixa de 597px |
| `pep-dep-verde-base.png` | 0–600, 1697–1740 | base arredondada |
| `pep-dep-victor/aline/weverton.jpg` | 110×149 | fotos dos depoimentos (borda branca e cantos já na imagem) |
| `pep-dep-carrinho.jpg` | 0–600, 2030–2517 | carrinho com as latas **com o botão "Finalizar meu pedido" na imagem**: o botão fica em cima da foto e não há o que tem atrás dele. A imagem inteira é o link. Com export do Figma sem o botão, dá para trocar por botão HTML |

No mobile as laterais e os arredondados em imagem somem (`.dsk`) e o miolo verde vira um card de
largura cheia com `border-radius:32px`. Texto 19px/22.5px (Arial fica mais largo que a fonte do
design; em 19.5px os depoimentos quebravam uma linha a mais e desalinhavam as laterais). Nos
depoimentos o line-height é 22px e os espaçadores (25/36/44/35) fecham os 597px: se mudar texto,
confira que nenhum depoimento passa de 7 linhas no desktop.

## recompra.html

"A gente percebeu que faz um tempo" (reativação de quem não compra há semanas). Design original:
`d:/Downloads/email-completo (4).jpg` (600×1860, 1x), cópia em `assets/recompra/_design.jpg` e
upscale em `_design-2x.png`. Recortes pelo `assets/recompra/_recortes.py`. CTAs →
`https://pepprotein.com.br/collections/all`.

| Arquivo em `assets/recompra/` (prefixo `pep-rc-`, já no Files) | Linhas do 1x | Uso |
|---|---|---|
| `pep-rc-lata.jpg` | 253–748 | lata de Limão Taiti embalada a vácuo com limões |
| `pep-rc-card-latas.jpg` | 1226–1320 | metade de baixo da pílula verde com as três latas. Emenda com o card HTML (`padding:0 60px`, `border-radius:106px 106px 0 0`) |
| `pep-rc-latas.jpg` | 1340–1690 | três latas com os raios verdes |
| `pep-u24-logo.png` / `pep-bv-mao.png` | — | logo e mãozinha reaproveitados (mesmas URLs) |

É HTML: título, os três parágrafos (quebras do design com `<br class="dbr">`, que somem no
mobile), o texto do card e o botão "Ver os sabores". O upscale puxou o verde do card para
`#2e7018`; o `_recortes.py` corrige para `#277217` e fixa o creme em `#fffcf0`, senão a emenda
com o HTML aparece. Placeholder: `%UNSUBSCRIBELINK%`.

**Texto do design com problema (confirmar com o cliente):** o 3º parágrafo termina cortado
("...uma lista de ingredientes que não precisa de") e "E tudo bem a rotina muda" provavelmente
pede dois-pontos ou vírgula depois de "bem". No HTML está igual ao design.

## recompra-60-dias.html

"Talvez esse seja o sinal para voltar": recompra aos 60 dias com o cupom `VOLTAR10`. Design original:
`d:/Downloads/email-completo (7).jpg` (600×1911, 1x), cópia em `assets/recompra-60-dias/_design.jpg`
e upscale em `_design-2x.png`. Recortes pelo `_recortes.py`; o `_medir.py` lista as faixas de
conteúdo. CTAs → `https://pepprotein.com.br/collections/all`. Fundo `#fffcf1` (medido).

| Arquivo (prefixo `pep-r60-`, já no Files) | Recorte do 1x (x, y) | Uso |
|---|---|---|
| `pep-r60-lata-asas.jpg` | 0–600, 270–710 | lata de Limão Taiti com asas |
| `pep-r60-cupom-vazio.png` | 0–600, 868–1092 | ticket laranja com tracejado e os dois limões, **com o miolo pintado de laranja liso** (texto apagado). `background` do `<td>` (VML no Outlook, `#f35524` de fallback). "Use o cupom / VOLTAR10 / e ganhe 10% OFF" é HTML. No mobile vira `background-size:contain` com 140px de altura e fonte menor |
| `pep-r60-mao.jpg` | 0–312, 1192–1620 | mão com a lata **e os três traços verdes** das chamadas. As chamadas são HTML na coluna da direita (288px), com espaçadores 22/45/40 alinhando com os traços. No mobile as colunas ficam 48/52% e o texto cai para 13px |
| `pep-r60-braco.jpg` | 0–92, 1620–1730 | ponta do braço ao lado de "Sua geladeira…": `background` do `<td>`, some no mobile (`.braco`) e no Outlook |
| `pep-u24-logo.png` / `pep-bv-mao.png` | — | logo e mãozinha reaproveitados (mesmas URLs) |

Texto 19.5px/25px, quebras do design com `<br class="dbr">` (com espaço antes, senão as palavras
grudam quando o `<br>` some no mobile). Placeholder: `%UNSUBSCRIBELINK%`.

## que-tal-voltar.html

"Já faz um tempo, que tal voltar?" (reativação com o cupom `VOLTAR10`). Design original:
`d:/Downloads/email-completo (5).jpg` (600×2001, 1x), cópia em `assets/que-tal-voltar/_design.jpg`
e upscale em `_design-2x.png`. Recortes pelo `assets/que-tal-voltar/_recortes.py`.
CTAs → `https://pepprotein.com.br/collections/all`.

| Arquivo em `assets/que-tal-voltar/` (prefixo `pep-qtv-`, já no Files) | Linhas do 1x | Uso |
|---|---|---|
| `pep-qtv-voltar.png` | 205–263 | "que tal voltar?" cursivo, laranja com alfa (356×58) |
| `pep-qtv-baldes.jpg` | 270–730 | os dois baldes com latas |
| `pep-qtv-cupom.jpg` | 895–1125 | ticket **vazio redesenhado em PIL** (pílula + tracejado 2.5px, traço 11.5 / vão 6.5) com os limões do original. `background` do `<td>` com VML; "Use o cupom / VOLTAR10 / e ganhe 10% OFF" é texto por cima. No mobile vira `background-size:contain` com fonte menor |
| `pep-qtv-frutas.jpg` | 1122–1546 | fundo creme só com as frutinhas das laterais; o texto dos 4 parágrafos é HTML por cima (altura fixa 424px). No mobile e no Outlook o fundo some e fica só o texto |
| `pep-qtv-latas.jpg` | 1546–1845 | as três latas. Os 4px de cima das tampas ficaram no fundo das frutas (a emenda passa abaixo dos mirtilos) |

Logo = `pep-u24-logo.png`, mãozinha = `pep-bv-mao.png` (cópias locais só para o preview).
Texto 19.5px/25px, quebras batendo com o design (`<br class="dsk">` some no mobile).
Placeholder: `%UNSUBSCRIBELINK%`.

## 60-dias.html

"60 dias sem PEP? Tá tudo bem aí?" (recompra sem cupom). Design original:
`d:/Downloads/email-completo (6).jpg` (600×2256, 1x), cópia em `assets/60-dias/_design.jpg` e upscale
em `_design-2x.png`. Recortes pelo `assets/60-dias/_recortes.py`. CTAs → `https://pepprotein.com.br/collections/all`.

| Arquivo em `assets/60-dias/` (prefixo `pep-60d-`, já no Files) | Recorte do 1x (x, y) | Uso |
|---|---|---|
| `pep-60d-hero.jpg` | 0–600, 290–726 | lata no pedestal. O degradê do pedestal passava por baixo do 1º parágrafo: os últimos 20px foram fundidos no creme |
| `pep-60d-mao.jpg` | 0–286, 1036–1458 | mão com a lata + framboesa de cima. Traz o começo dos tracinhos verdes |
| `pep-60d-braco.jpg` | 0–100, 1458–1560 | ponta do braço sob o parágrafo "Leve, refrescante…": `background` do `<td>`, some no mobile (`.braco`) e no Outlook |
| `pep-60d-framboesa.jpg` | 458–512, 1358–1414 | ícone abaixo dos tópicos |
| `pep-60d-latas.jpg` | 0–600, 1668–1975 | as três latas |

Tópicos ao lado da mão são HTML (17px/23px, laranja `#f35524` em negrito). Cada tracinho é metade
imagem (até x=286) e metade `<div>` de 4px; os `padding-top` dos `.traco` estão calibrados no pixel
para emendar. No mobile a metade HTML some (`.traco`) e fica só a ponta da imagem.
Texto 20px/25px com `<br class="br">` (some no mobile) para bater as quebras do design.
Fundo `#fffcf1`. Logo = `pep-u24-logo.png`, mãozinha = `pep-bv-mao.png`. Placeholder: `%UNSUBSCRIBELINK%`.
## pedido-na-rua.html

Pós-compra "Sua PEP já está na rua!" (pedido enviado). Design original:
`d:/Downloads/Pós-compra - Pedido na rua.png` (600×2123, 1x), cópia em
`assets/pedido-na-rua/_design.png` e upscale em `_design-2x.png`. Recortes saem do
`assets/pedido-na-rua/_recortes.py`.

| Arquivo em `assets/pedido-na-rua/` (prefixo `pep-pnr-`, já no Files) | Linhas do 1x | Uso |
|---|---|---|
| `pep-pnr-hero-ceu.jpg` | 0–372 | céu **sem texto** (`remove_text.py`): `background` do hero, VML no Outlook, `bgcolor #006ecd` |
| `pep-pnr-logo.png` | — | logo PEP branco com alfa (79×34) |
| `pep-pnr-na-rua.png` | — | "na rua!" cursivo, verde-claro com alfa (206×42) |
| `pep-pnr-hero-latas.jpg` | 372–923 | cooler amarelo com as latas na praia |
| `pep-pnr-maos.jpg` | 1400–2123 | mãos com as latas e os adesivos (20g, 66 kcal, zero açúcar) |
| `pep-bv-mao.png` | — | mãozinha do botão (mesma URL do boas-vindas) |

É HTML: título, texto do hero, botão "Rastrear meu pedido!", "ENQUANTO A CAIXA NÃO CHEGA", o texto
cinza (`#474747`) e "Falta pouco pra sua PEP chegar." (o creme vai até logo abaixo dessa linha; no
design ela fica em cima da emenda creme/foto). `e&nbsp;a` e `lata&nbsp;aberta` forçam as quebras do
design no desktop (Arial é mais larga).

**Rastreio:** a plataforma não tem variável de código/link de rastreio. O botão vai para
`https://pepprotein.com.br/account` (login → pedidos do cliente). Se o fluxo passar a mandar um link
de rastreio, trocar o `href` do botão (e do VML). Fotos: cooler → `/account`, mãos → `/collections/all`.
Rodapé `#f7f6f6` (continua o fundo da foto) com `%UNSUBSCRIBELINK%`.

## pedido-confirmado.html

Pós-compra "Pedido confirmado!". Design original: `d:/Downloads/Pós-compra - Pedido Confirmado certo.png`
(600×2012, 1x), cópia em `assets/pedido-confirmado/_design.png` e upscale em `_design-2x.png`.
Os recortes saem do 2x pelo `assets/pedido-confirmado/_recortes.py` (se vier export 2x do Figma, é só
substituir o `_design-2x.png` e rodar de novo).

| Arquivo em `assets/pedido-confirmado/` (prefixo `pep-pc-`, já no Files) | Linhas do 1x | Uso |
|---|---|---|
| `pep-pc-hero-ceu.jpg` | 0–425 | céu **sem texto** (`remove_text.py`), `background` do `<td>` com VML, `bgcolor #00569f` |
| `pep-pc-logo.png` | 85–121 | logo PEP branco com alfa (79×36) |
| `pep-pc-confirmado.png` | 208–276 | "confirmado!" cursivo, `#daf9ac` com alfa (355×68) |
| `pep-pc-hero-latas.jpg` | 425–929 | mãos brindando com as três latas |
| `pep-pc-agora.png` | 1128–1179 | "agora?" cursivo laranja com alfa (156×51). No design o "?" encosta no "t" de "acontece"; aqui fica logo abaixo |
| `pep-pc-selo-20g.jpg` | 1470–1550 | faixa de largura cheia com o selo "20g de proteína" (ele invade a coluna da lata) |
| `pep-pc-selos.jpg` | 1550–1750, x 0–256 | selos "66 kcal" e "Zero açúcar". Coluna da esquerda, com o "Obrigado por..." em HTML embaixo |
| `pep-pc-mao-lata.jpg` | 1550–2012, x 256–600 | mão com a lata (coluna da direita) |
| `pep-bv-mao.png` | — | mãozinha do botão, reaproveitada do boas-vindas (cópia local só pro preview) |

É HTML: "Pedido", parágrafo do hero, botão (VML no Outlook), "O que acontece", o parágrafo `#535050`
e o "Obrigado por escolher..." (verde, 18.5px; no mobile as duas colunas ficam lado a lado em 42.67% /
57.33% e esse texto cai para 13px).

- **CTA "Acompanhar meu pedido" → `https://pepprotein.com.br/account`** (redireciona para a conta de
  cliente da Shopify). Não existe variável de rastreio/status do pedido na plataforma.
- Placeholder: `%UNSUBSCRIBELINK%`.
## bem-vindo.html

"Bem vindo(a)! Você acabou de entrar no universo de quem lê rótulo" (boas-vindas institucional, sem
cupom). Design original: `d:/Downloads/email-completo (8).jpg` (600×2774, 1x), cópia em
`assets/bem-vindo/_design.jpg` e upscale em `_design-2x.png`. Recortes pelo `assets/bem-vindo/_recortes.py`.
CTAs → `https://pepprotein.com.br/collections/all`.

| Arquivo em `assets/bem-vindo/` (prefixo `pep-bem-`, já no Files) | Recorte do 1x (x, y) | Uso |
|---|---|---|
| `pep-bem-latas-topo.jpg` | 0–600, 214–468 | as três latas embaixo do título |
| `pep-bem-o-que-e.jpg` | 170–430, 872–992 | "O que é a PEP???" com contorno (fonte display) |
| `pep-bem-mao-v2.jpg` | 0–312, 1074–1517 | mão com a lata **e os três traços verdes** inteiros. Chamadas em HTML à direita (espaçadores 24/45/40) |
| `pep-bem-pulso-v2.jpg` | 0–100, 1517–1600 | ponta do pulso: `background` da seção PROTEIN/ENERGY/PEACE, some no mobile (`.pulso`) e no Outlook |
| `pep-bem-ico-protein/energy/peace.jpg` | 355–490, 1517 / 1682 / 1847 (135×135) | um círculo por linha, com o texto ao lado em `valign="middle"`. A linha entre eles é um `<td>` verde de 9×30px (HTML). Assim o alinhamento aguenta o texto quebrando diferente no mobile. `pep-bem-mao.jpg`, `pep-bem-pulso.jpg` e `pep-bem-icones.jpg` (coluna única, com o topo do 1º círculo cortado) são da 1ª versão e ficaram sem uso no Files |
| `pep-bem-latas.jpg` | 0–600, 2330–2774 | latas no degrau cinza. O rodapé continua o cinza (`#dcdfe5`) |

Logo = `pep-u24-logo.png`, mãozinha = `pep-bv-mao.png` (cópias locais só para o preview).
É HTML: título, subtítulos, os dois cards verdes (1º `border-radius:100px`, 2º 64px, cantos retos no
Outlook) e o botão "Experimentar PEP" (VML). Quebras do design com `<br class="br">` (somem no mobile).
Placeholder: `%UNSUBSCRIBELINK%`.