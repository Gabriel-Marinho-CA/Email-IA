# Joie Suplementos

| | |
|---|---|
| Site | `https://www.joiesuplementos.com.br` (não é Shopify: URLs `/produtos/.../c` e `/.../p`) |
| Imagens dos e-mails | Files da `turbo-starter.myshopify.com` (loja da Turbo, indicada pelo usuário em 06/11/2026). Base do CDN: `https://cdn.shopify.com/s/files/1/0968/7354/6003/files/` (conferida). CLI autorizada em 06/11 com `read_products,write_products,read_files,write_files,read_publications,write_publications,read_discounts` |
| Prefixo | `joie-<sigla do template>-` |
| Cores | e-mail 01: verde `#a5de00` (sRGB; no PSD é `#b6dd12` em Adobe RGB), texto do card `#131313`. E-mail 02: verde `#bfe132`, card dos brindes `#0b3823` (faixa do topo `#07301b`), texto do card `#131412`. E-mail 03 (17/11): cabeçalho dos cards `#a5ee2e`, faixa e card `#a9dc2a`/`#a9dd2a`, botão degradê `#a5ee2e` → `#70ad0c` (borda `#c4e68d`). Preto `#000000` |
| Fontes do layout | Trade Gothic Bold (títulos, caixa alta) e Poppins Thin/ExtraLight/Bold (texto). No e-mail: Arial/Helvetica; títulos em Trade Gothic viram imagem |
| Rodapé legal | JOIE SUPLEMENTOS LTDA · CNPJ 26.907.772/0001-03 · Rua Itapura, 1053 · Vila Gomes Cardim · São Paulo/SP · 03310-000 (Receita Federal via BrasilAPI em 06/11/2026; **confirmar com o cliente**) |
| WhatsApp | `5511921459490` (o site tem um link "Quero garantir meus descontos da Black Joie - 2026!") |

**Perfil de cor do PSD muda de e-mail para e-mail:** o designer manda PSD + PNG. No e-mail 01 as camadas vinham em
Adobe RGB e o PNG em sRGB (precisou converter: `#b6dd12` → `#a5de00`). No e-mail 02 o PSD é **Apple RGB**, mas o PNG
exportado tem os mesmos valores das camadas (não converteu): pixel do PSD entra direto. Antes de recortar, compare
um pixel de uma camada com o mesmo pixel do PNG. Ler o PSD: `psd-tools` **>= 1.10** (o 1.9.34 instalado nesta
máquina dá "Invalid version 8"). Instalado à parte, sem mexer no numpy/opencv:
`pip install psd-tools --no-deps --target <pasta>` e `PYTHONPATH=<pasta>` (o `_recortes.py` do e-mail 02 lê a pasta da
variável `PSDLIB`). O composite do psd-tools não roda com o numpy 1.21: use o raster de cada camada
(`layer.topil()`, `smart_object.data`) e componha na ordem do PSD (a iteração vai de baixo para cima; no e-mail 02 o
retângulo preto fica **embaixo** da foto).

**Arquivos do e-mail 01 fora do disco:** em 12/11/2026 a pasta só tinha este README e o material do e-mail 02;
`black-friday-aquecimento.mjml` e `assets/black-friday-aquecimento/` sumiram. As imagens `joie-bfa-` continuam no CDN.

## black-friday-aquecimento.mjml

Black Friday, semana 01, aquecimento (teaser, **sem botão e sem cupom**, igual ao layout). Layout:
`assets/Solicitação Email Marketing - 01 - Black Friday - Semana 01 - Aquecimento.png` (600×1995) + PSD e
recortes do designer na pasta de mesmo nome. Cópia em `assets/black-friday-aquecimento/_design.png`;
`_design-2x.png` = Real-ESRGAN.

| Arquivo (prefixo `joie-bfa-`) | 1x | Origem / uso |
|---|---|---|
| `logo.png` | x 212-388, y 79-162 | logo "Black Friday" (do 2x, bordas limpas), fundo preto |
| `titulo.png` | x 80-520, y 196-310 | "Tem coisa boa chegando por aqui." (Trade Gothic, duas linhas de tamanhos diferentes justificadas: não sai em texto de e-mail) |
| `fundo-texto.jpg` | y 345-500 | `background-url` da seção do 1º parágrafo (início do brilho verde), das camadas do PSD |
| `produtos.jpg` | y 500-976 | foto dos produtos (smart object em 1856px) + topo arredondado do card verde |
| `fundo-card.jpg` | y 976-1354 | `background-url` da seção do card (brilho nas margens; o miolo é coberto pela coluna verde) |
| `olhos-1.png`, `olhos-2.png` | x 168-432, y 1222-1354 / 1354-1486 | círculo branco redesenhado + emoji 👀 do Noto (o mesmo glifo do PSD), cortado na borda do card; PNG com alfa (modo escuro) |
| `black-joie.png` | x 110-490, y 1655-1835 | "A Black da Joie vem aí." (contorno verde, girado), do 2x com bordas limpas |

Texto real: parágrafos (Arial 18/24, `max-width` 324 e 356 para quebrar como o layout), texto do card (36/45,
`<br>` nas quebras), "NOS VEMOS EM BREVE. 💚" (pilha condensada, 33px) e rodapé legal (não existe no layout:
foi acrescentado embaixo da faixa verde, com `{{link_optout}}`).

Estrutura: card verde = seção com `padding` lateral **6,5%** (não px) e `mj-column` verde com
`border-radius 0 0 20px 20px`, para a largura do card acompanhar a do topo que está na imagem em qualquer tela.
O círculo dos olhos é cortado em duas imagens na borda do card (uma dentro da coluna verde, outra na seção
preta). Mobile = desktop em escala (classes `j-*`, degraus 480 e 359). Conferido: desktop alinhado com o layout
(0-3px), celular em 320/360/375/390 e sem `<style>` (nada estoura; o texto só quebra mais).

Links: logo, foto dos produtos e "A Black da Joie vem aí." → `https://www.joiesuplementos.com.br/`.

Assunto sugerido: "Tem coisa boa chegando por aqui 👀" · Pré-header: "A Black Friday da Joie vem aí. Vale a pena
ficar de olho."

Pendências:
- Imagens: as 8 no Files da `turbo-starter` (06/11/2026, todas READY e 200). Não importado no Flash.
- Sem CTA no layout. Ideias (perguntar): botão para a home ou para o WhatsApp da lista da Black.
- Razão social/CNPJ/endereço vieram da Receita: confirmar com o cliente.

## black-friday-brindes.mjml

Black Friday, semana 02, brindes por faixa de valor. Layout:
`assets/Email 02 - Black Friday - 02 - Black Friday - Semana 02 - Brindes/` (PNG 600×2360 + PSD + 3 fatias do designer,
que não são usadas: têm o texto na imagem). Cópia em `assets/black-friday-brindes/_design.png`; `_design-2x.png` =
Real-ESRGAN; `_limpo.png` = camadas do PSD sem texto (glow + retângulo preto + foto) e `_limpo-2x.png` o upscale dela.
Recortes em `assets/black-friday-brindes/_recortes.py`.

| Arquivo (prefixo `joie-bfb-`) | 1x | Origem / uso |
|---|---|---|
| `logo.png` | x 208-392, y 88-174 | logo "Black Friday", do 2x do layout. Não reaproveitei o `joie-bfa-logo.png`: é verde `#a5de00`, e este layout usa `#bfe132` |
| `titulo.png` | x 120-480, y 210-360 | "A Black da Joie começou!" (Trade Gothic), do 2x do layout |
| `fundo-texto.jpg` | y 392-490 | `background-url` da seção do 1º parágrafo (`100% auto`, `center bottom`), de `_limpo-2x` |
| `produtos.jpg` | y 490-934 | foto dos produtos (a camada do PSD é 1x; o smart object em 1856px é outra geração da imagem e não bate) |
| `fundo-card.jpg` | y 934-1145 | `background-url` da seção do card verde (`100% auto`, `center top`): plataforma e brilho nas laterais |
| `faixa.jpg` | y 1838-1958 | faixa girada "Até 10x sem juros • +3% OFF no Pix • Frete grátis", do 2x do layout |
| `melatonina.png`, `hepro.png`, `propolis.png`, `kit-serum.png` | quadro 140×146 por card | smart objects do PSD (1080px, fundo transparente), na posição do layout |

Texto real: 1º parágrafo (20/25, `max-width` 366), card verde (36/45, `<br>`), os 4 cards de brinde (tabela no bloco
HTML, 2 colunas que não empilham, células em %), 2º parágrafo (19/24, `max-width` 360), "Quanto maior o carrinho,
melhor o presente." (36/45), botão "ESCOLHER MEUS PRODUTOS" (400×83) e "Brindes enquanto durarem os estoques.". Rodapé
legal acrescentado no preto do fim, com `{{link_optout}}`. Mobile = desktop em escala (classes `j-*`, degraus 480 e
359). Conferido: desktop alinhado com o layout (0-2px), celular em 320/360/375/390.

Links: logo → home; foto dos produtos, faixa e botão → `https://www.joiesuplementos.com.br/produtos/c` (mesmo link do
banner "Melatonina BRINDE - Black 2026" da home em 12/11/2026).

Assunto sugerido: "A Black da Joie começou! 🎁" · Pré-header: "Nesta semana, suas compras desbloqueiam brindes especiais."

Pendências:
- Imagens: as 10 no Files da `turbo-starter` (12/11/2026, todas READY e 200). Não importado no Flash.
- Texto do layout corrigido (confirmar): "Ganhe Ganhe Própolis" → "Ganhe Própolis"; "ACIMA DE 259,90" → "ACIMA DE R$259,90".
- Própolis e Kit Serum estão os dois em "ACIMA DE R$299" (igual ao layout): confirmar se a 4ª faixa é outro valor.
- Link do botão: confirmar se existe página da Black (hoje vai para todos os produtos).
- Razão social/CNPJ/endereço vieram da Receita: confirmar com o cliente.

## black-17-11.mjml

Black Friday, e-mail 03 (envio 17/11): "Todo o site com 30% OFF" + brindes por valor do carrinho. Layout:
`assets/black-17-11/FULL-Joie-Email03-BlackFriday.png` (600×1861; as fatias `01/02/03-...png` são o mesmo PNG cortado,
com o texto). Sem PSD desta vez. O `Figma.docx` tem o link do Figma (`wIeCQWdXd9sT0xPn7ywt9h`), mas a conta do MCP não tem
acesso ao arquivo ("you don't have edit access"): tudo saiu do PNG. Cópia em `assets/black-17-11/_design.png`;
`_design-2x.png` = Real-ESRGAN. Recortes em `assets/black-17-11/_recortes.py`.

**ESRGAN clareia os escuros** (+2 a +8 níveis nos fundos quase pretos) e deixa contorno escuro em volta de letra clara. O
`_recortes.py` corrige somando ao 2x a diferença `1x − (2x reduzido)` ampliada: a média de cada 2×2 volta a ser o pixel do 1x
e o detalhe do upscale fica. Texto e formas que viram HTML saem dos fundos por interpolação harmônica (Laplace) sobre
retângulos inteiros (o fundo é liso), sem polinômio.

| Arquivo (prefixo `joie-b17-`) | 1x | Origem / uso |
|---|---|---|
| `topo.jpg` | y 0-300 | logo, "TODO O SITE COM 30% OFF" (Trade Gothic) e divisor, sobre a cortina |
| `fundo-brindes.jpg` | y 300-616 | `background-url` (`100% 100%`) da seção do parágrafo + cards, sem o texto e sem os cards |
| `robo.jpg`, `relogio.jpg` | x 112-287 / 312-487, y 446-571 | corpo translúcido de cada card com o brinde (inclui a borda lateral) |
| `base-1.jpg`, `base-2.jpg` | mesmos x, y 572-611 | 1x, sem a legenda: `background` do `<td>` de "Ganham ..." (com `bgcolor` `#01290c` para o Outlook), cantos de baixo inclusos |
| `produtos.jpg` | y 616-890 | CreaGEN, HEPRO, Morning Shot, Colágeno no pedestal |
| `fundo-botao.jpg` | y 890-1041 | fundo (cortina) do 1º botão, sem o botão |
| `aproveita.jpg` | y 1072-1267 | topo do card com "E VOCÊ TAMBÉM APROVEITA" (Trade Gothic) e o brilho em volta |
| `fundo-card.jpg` | y 1268-1472 | brilho nas margens do corpo do card; o miolo é coberto pela `mj-column` |
| `fundo-final.jpg` | y 1473-1860 | fundo do parágrafo final, 2º botão, "Brindes enquanto..." e rodapé legal |

Texto real: parágrafo do topo (17,5/24, `max-width` 322), cabeçalho dos cards (14/16) e legendas (11/14) numa tabela no
bloco HTML (2 cards que não empilham; no celular os cards alargam de 29,3% para 35,25% para a legenda caber em uma linha),
faixa "ATÉ 10X SEM JUROS • +3% OFF NO PIX • FRETE GRÁTIS" (9px, `letter-spacing` 2px, fundo `#a9dc2a`), os 3 bullets (pilha
condensada, 34/57, bolinha = `span` inline-block verde), parágrafo final (22/30, `max-width` 370), os 2 botões
"APROVEITAR 30% OFF" (`mj-button` 299×63, raio 16) e "Brindes enquanto durarem os estoques." (16, itálico). Rodapé legal
acrescentado no fim, em cima do brilho, com `{{link_optout}}`.

Fundos com texto em cima usam `background-size="100% 100%"`: no desktop a seção tem a altura da imagem (sem distorção) e no
celular o fundo estica só na vertical, então a cortina continua alinhada com as imagens de cima e de baixo. O degradê do
botão é um `linear-gradient` no `mj-style` (fora da media query) por cima do `background-color` `#8acd1d`: cliente que não
aceita degradê mostra o verde chapado. Mobile = desktop em escala (classes `j-*`, degraus 480 e 359). Conferido: desktop
alinhado com o layout (0-1px em todos os blocos), celular em 320/360/375/390.

Links: todas as imagens clicáveis e os 2 botões → `https://www.joiesuplementos.com.br/produtos/c` (mesmo link do banner
"Smartwach | Black Joie 2026" da home em 17/11/2026).

Assunto sugerido: "Começou: todo o site com 30% OFF 💚" · Pré-header: "E o seu carrinho ainda pode desbloquear um robô
aspirador ou um smartwatch."

Pendências:
- Imagens: as 11 no Files da `turbo-starter` (17/11/2026, todas READY e 200). Não importado no Flash.
- O layout não tem cupom: confirmar que os 30% saem automáticos no site (senão, falta o código no e-mail).
- Link dos botões: confirmar se existe página da Black (hoje vai para todos os produtos).
- No Outlook do Windows: cantos dos cards retos, legenda dos cards em cor chapada (sem a imagem de fundo) e bullets sem a
  bolinha verde. Gmail/Apple Mail mostram tudo.
- Razão social/CNPJ/endereço vieram da Receita: confirmar com o cliente.
