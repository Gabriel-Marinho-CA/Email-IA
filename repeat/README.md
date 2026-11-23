# E-mails Repeat

## Marca

**Regra de links (16/10/2026, pedido do usuário):** card/botão de produto aponta direto para
`https://repeatonline.com.br/products/<handle>`. O cupom automático (`/discount/CODIGO?redirect=...`)
fica só no CTA principal e no hero.

| Item | Valor |
|---|---|
| Loja Shopify | admin `repeatfoods` = domínio permanente **`y1yycy-wg.myshopify.com`** (é o que o CLI/OAuth aceita; `repeatfoods.myshopify.com` é alias e o `store auth` com ele falha) |
| Site | `https://repeatonline.com.br` |
| CDN | `https://cdn.shopify.com/s/files/1/0780/2290/1980/files/` |
| Auth do CLI | `shopify store auth --store y1yycy-wg.myshopify.com --scopes read_files,write_files,read_discounts,write_discounts,read_products,read_price_rules,write_price_rules` (feito em 16/10/2026) |
| Rodapé | Kalena Importação Exportação e Comércio Ltda · CNPJ 10.293.200/0001-33 · Av. Angélica, 2503, cj. 101 · São Paulo/SP · 01227-200 · WhatsApp (11) 94794-7874 · Instagram `@repeatfoods` |
| Brandbook | `D:\Downloads\LO1_BRANDBOOK_REPEAT_2025.6.pdf` |

**Cores** (brandbook): laranja `#d4471a` (principal), laranja escuro `#a64208`, creme `#f2e2dc`,
vinho `#571713`. **Tom:** moderna, espontânea, acolhedora, confiante; "Repeat, prazer que cabe na rotina."

**Fontes:** HWT Artz (títulos, caixa alta) e Arboria (texto). Nenhuma é email-safe:
- Título em HWT Artz só dentro de imagem. `assets/_marca/fontes/` tem os subsets extraídos do PDF
  (A–Z, 0–9, `% ! . & $ # @ ?`, Ç e Õ). **Não tem Ê, Ã, É nem vírgula**: escreva a headline sem eles.
- Em texto HTML: títulos com `'HWT Artz', 'Helvetica Neue Condensed', 'HelveticaNeue-CondensedBold',
  'Roboto Condensed', 'Arial Narrow', 'Helvetica Neue', Arial, sans-serif` em caixa alta; corpo com
  `'Avenir Next', Avenir, 'Helvetica Neue', Helvetica, Arial, sans-serif` (Avenir é a mais próxima da Arboria no Apple).

**`assets/_marca/`** (compartilhado entre templates): `logo-mask.png` (alfa do logo, 3302×917, extraído
do vetor do PDF), `vagem-`, `graos-`, `estrela-`, `meialua-mask.png` (formas da página 07 do brandbook),
`produtos/` (packshots da loja; os de edamame e alga são PNG com fundo transparente) e `marca.py`
(cores, `forma()`, `texto()` em HWT Artz, `leque()` de pacotes, `estrela_selo()`, `logo()`), que os
`_recortes.py` de cada template importam.

## WhatsApp (API oficial) nas automações — 19/10/2026

Templates da Meta criados no Flash (Templates → Criar → WhatsApp API), categoria Marketing, pt_BR,
**todos APPROVED** em 19/10/2026. `{{primeiro_nome}}` = `{{1}}`; botões são URL fixa com o cupom.

| Template | Texto (resumo) | Botão | Fluxo |
|---|---|---|---|
| `repeat_carrinho_5off` | carrinho + cupom 5%CARRINHO + `{{carrinho_url}}` no corpo | — | 2055, depois do e-mail |
| `repeat_segunda_compra_10off` | 10% na 2ª compra, SEGUNDA10 | Usar meus 10% → `/discount/SEGUNDA10` | 2056 |
| `repeat_aniversario_antes_10off` | presente adiantado, NIVER10 | Quero meu presente → `/discount/NIVER10` | 2057 (1º e-mail) |
| `repeat_aniversario_dia_15off` | feliz aniversário, NIVER15, só hoje | Usar meus 15% → `/discount/NIVER15` | 2057 (2º e-mail) |
| `repeat_reativacao_40d_5off` | bateu saudade, VOLTA5 | Usar meus 5% → `/discount/VOLTA5` | 2058 |
| `repeat_reativacao_60d_10off` | subimos seu desconto, VOLTA10 | Usar meus 10% → `/discount/VOLTA10` | 2058 |
| `repeat_reativacao_90d_15off` | maior desconto, VOLTA15 | Usar meus 15% → `/discount/VOLTA15` | 2058 |
| `flashcrm_bounceback_wpp` (modelo do Flash, já aprovado) | obrigado + cashback `{{cupom}}` válido até `{{data_vencimento}}` | — | 2059 |

- Cada WhatsApp entra **logo depois do e-mail** correspondente, na mesma etapa do fluxo (como nos
  modelos do Flash). Smart Sending ativo nas etapas.
- Etapa no fluxo: `tipo_acao: send_whatsapp`, `config: {meta_template_name, meta_template_language:
  "pt_BR", meta_category: "MARKETING", content_preview, template_params: {"1": "{{primeiro_nome}}", ...}}`.
- Inserido salvando o fluxo existente pela mutação do editor com `flow: {id, ...}` e as ações com o
  `id` do banco (as novas sem `id`, ligadas por `temp_id`), igual ao `generateFluxoPayload` do Flash.
  IDs das etapas novas: 12896 (2055), 12897 (2056), 12898/12899 (2057), 12900/12901/12902 (2058), 12903 (2059).
- O fluxo 2055 teve a condição alterada no editor do Flash para "sem pedido nos últimos **2** dias"
  (edição feita fora desta sessão); foi mantida.

## Formato: MJML (não HTML)

Os templates da Repeat seguem o `FLASHCRM-EMAIL-E-FLUXOS-PARA-DEV.md` da raiz: o arquivo entregue é
**`.mjml`**, importado no Flash pelo favorito "Importar MJML", e cada tag vira bloco nativo editável.
O `.html` ao lado é só o MJML compilado, para preview e e-mail de teste.

```powershell
npx -y mjml@4.15.3 repeat/cashback.mjml -o repeat/cashback.html
```

No Flash: Templates → Criar Template → E-mail → favorito **Importar MJML** → colar o `.mjml` → Import →
nomear → Criar Template. Assunto e pré-header vão no passo do fluxo.

---

## Carrinho abandonado (`carrinho-abandonado.mjml`)

Sem layout do Figma: design criado do brandbook, no estilo das aplicações em fundo creme com meia-lua
laranja. Prefixo `rep-ca-`. Imagens geradas por `assets/carrinho-abandonado/_recortes.py`.

| Arquivo | Exibição | O que é |
|---|---|---|
| `rep-ca-logo.png` | 130×36 | logo laranja com alfa (topo creme) |
| `rep-ca-hero.jpg` | 600×500 | "ESQUECEU ALGO?" em HWT Artz + estrela laranja "5% OFF" + 2 algas e 3 edamames sobre meia-lua laranja |
| `rep-ca-icone-vagem/graos/estrela.png` | 56×56 | formas da marca em creme com alfa, na faixa "FEITO PRA REPETIR" |
| `rep-cb-logo.png` (do cashback) | 100×28 | logo branco do rodapé |

- Cupom **`5%CARRINHO`**, que já existia na loja (criado em 13/10/2026: 5% no pedido inteiro, um uso
  por cliente, combina com tudo). Fixo no texto, "digite no checkout".
- Todos os CTAs (hero, "FINALIZAR MEU PEDIDO", "VOLTAR PRO CARRINHO", imagem do produto) → `{{carrinho_url}}`.
- Card "NO SEU CARRINHO" com blocos nativos e variáveis: `{{carrinho_produto_imagem}}`,
  `{{carrinho_produto_nome}}`, `{{carrinho_qtd_itens}}`, `{{carrinho_total}}`. A seção tem
  `fc-if--carrinho_produto_imagem` (some se o carrinho vier sem imagem). Mostra só o 1º produto; para
  listar todos, trocar pelo bloco nativo "Produtos do Carrinho" do Flash (arrastar depois do import,
  como o doc recomenda).
- Saudação `fc-if--primeiro_nome` / `fc-ifnot--primeiro_nome`. Rodapé com `{{link_optout}}`.
- Faixa "FEITO PRA REPETIR": até 13g de proteína (edamame), crocante sem fritura (edamame assado,
  alga "não é frito" na embalagem), cabe na rotina.
- Assunto sugerido: `Esqueceu algo? Seus snacks estão te esperando` · Pré-header:
  `Finalize o pedido com 5% OFF usando o cupom 5%CARRINHO.`

**No Flash (conta Repeat, empresa 467) — criado em 16/10/2026, inativo:**
- Template **4140** "Repeat - Carrinho 1 - 5% OFF" (MJML importado via `editor.setComponents`, salvo e
  reaberto: volta com as 12 seções, variáveis e `fc-if`; o Flash só acrescenta o `mj-head` de branding).
- Fluxo **2055** "Repeat - Carrinho abandonado (e-mail 5% OFF)", só e-mail (sem WhatsApp, a pedido):
  gatilho Carrinho Abandonado Criado → espera 1 h → "Sem pedido no último dia?" (pedidos = 0 nos
  últimos 1 dia) → Sim: e-mail (template 4140, assunto e pré-header acima) / Não: "Fluxo encerrado".
  `respeitar_opt_out: true`, `permitir_reentrada: false` (o cupom é de um uso por cliente).
- O fluxo de modelo "Carrinho abandonado" (1884) continua lá, inativo: não ligar os dois.

**Pendências**
- O cupom não é aplicado sozinho: `{{carrinho_url}}` é URL completa e não dá para encaixar no
  `/discount/5%25CARRINHO?redirect=...` (link testado, funciona com caminho relativo). Vale testar
  `https://repeatonline.com.br/discount/5%25CARRINHO?redirect={{carrinho_url_caminho}}` num envio de
  teste: se o `carrinho_url_caminho` vier como caminho (`/cart/...`), o botão passa a aplicar o cupom.
- Formato de `{{carrinho_total}}` e da imagem do produto não conferidos em envio real.

---

## Primeira para segunda compra (`segunda-compra.mjml`)

Sem layout do Figma: design criado do brandbook. Hero em fundo vinho com o mesmo pacote duas vezes
(a "repetição") sobre a meia-lua laranja. Prefixo `rep-sc-`. Imagens geradas por
`assets/segunda-compra/_recortes.py`.

| Arquivo | Exibição | O que é |
|---|---|---|
| `rep-sc-hero.jpg` | 600×505 | "GOSTOU? REPETE!" em HWT Artz (creme/laranja) + estrela laranja "10% OFF" + 2 pacotes de edamame sal marinho sobre a meia-lua |
| `rep-sc-crispy.jpg`, `rep-sc-brownie.jpg`, `rep-sc-ervilha.jpg` | 140×140 | cards de cross-sell (foto da loja) |
| `rep-cb-logo.png`, `rep-cb-manifesto.jpg` (do cashback) | 130×36 / 100×28 e 600×200 | logo branco no topo vinho e no rodapé; faixa "PRAZER QUE CABE NA SUA ROTINA." |

- Gatilho: fluxo de pedido, após a 1ª compra.
- Cupom **`SEGUNDA10`** (criado em 16/10/2026: 10% no pedido inteiro, um uso por cliente, combina só
  com frete). Fixo no texto.
- CTAs aplicam o cupom sozinhos: `https://repeatonline.com.br/discount/SEGUNDA10?redirect=%2Fcollections%2Fall`;
  os cards vão direto para a página do produto (`https://repeatonline.com.br/products/<handle>`).
- Cross-sell "NA SEGUNDA, VARIA O SABOR": Crispy de Chocolate com quinoa, Bombom de Brownie zero
  açúcar e Ervilha Crocante wasabi (sem preço).
- Saudação `fc-if--primeiro_nome` / `fc-ifnot--primeiro_nome`. Rodapé com `{{link_optout}}`.
- Assunto sugerido: `Gostou? Na segunda tem 10% OFF` · Pré-header:
  `Use o cupom SEGUNDA10 na sua próxima compra. O botão já aplica o desconto.`

**No Flash (empresa 467) — criado em 16/10/2026, inativo:**
- Template **4141** "Repeat - Segunda compra - 10% OFF".
- Fluxo **2056** "Repeat - Primeira para segunda compra (10% OFF)", só e-mail: gatilho Cliente fez um
  pedido com filtro de cliente "Número de pedidos = 1, desde sempre" (formato copiado do modelo
  "Pós-compra bounceback") → espera 5 dias → "Ainda só 1 pedido?" → Sim: e-mail (template 4141) /
  Não: "Fluxo encerrado (já recomprou)". Entrada "apenas uma vez", sem envio para quem não tem opt-in.
- O modelo "Pós-compra bounceback" (1887) usa o mesmo gatilho de 1ª compra: não ligar os dois.

**Pendências**
- `SEGUNDA10` vale para qualquer cliente (um uso por cliente), inclusive quem nunca comprou. Restringir
  a quem tem 1 pedido exige segmento de clientes na Shopify (escopo de clientes no CLI).
- O texto não fala em prazo; se o fluxo tiver espera (ex.: enviar após a entrega), dá para ajustar a
  abertura.

---

## Aniversário (`aniversario-antes.mjml` + `aniversario-dia.mjml`)

Par de e-mails do mês de aniversário. Sem layout do Figma: design criado do brandbook com a mesma
cara de festa nos dois (confete com as formas da marca + caixa de presente com os pacotes saindo).
Prefixo `rep-an-`. Imagens geradas por `assets/aniversario/_recortes.py` (tem `texto_acentuado()`,
que desenha o acento agudo à mão, porque a HWT Artz não tem Ó).

| Arquivo | Exibição | O que é |
|---|---|---|
| `rep-an-hero-antes.jpg` | 600×520 | fundo laranja, "PRESENTE ADIANTADO!", estrela creme "10% OFF", caixa branca com fita vinho, chão creme |
| `rep-an-hero-dia.jpg` | 600×520 | fundo vinho, "FELIZ NIVER!", estrela laranja "15% OFF" + etiqueta "SÓ HOJE", caixa laranja com fita creme |
| `rep-cb-logo.png`, `rep-cb-edamame/alga/coco.jpg` (do cashback) | | logo branco (topo e rodapé) e cards de produto |

| | Antes do aniversário | No dia (se não comprou) |
|---|---|---|
| Template | `aniversario-antes.mjml` | `aniversario-dia.mjml` |
| Cupom | `NIVER10` (10%) | `NIVER15` (15%) |
| Topo | laranja | vinho (mais urgente) |
| Saudação | "Oi, {{primeiro_nome}}!" / "Oi!" | "Parabéns, {{primeiro_nome}}!" / "Parabéns!" |
| CTA | QUERO MEU PRESENTE | USAR MEUS 15% HOJE |

- Cupons criados na Shopify em 16/10/2026: pedido inteiro, um uso por cliente, combinam só com frete,
  sem data de fim. Fixos no texto.
- CTAs → `https://repeatonline.com.br/discount/NIVER10?redirect=...` (ou NIVER15), que aplicam o
  cupom sozinhos.
- Seção "PRA COMEMORAR": 3 cards (edamame, alga, cracker de coco) em fundo creme, com link direto
  para a página do produto.
- Sem variável de data (`idade_aniversario` não confirmada). Rodapé com `{{link_optout}}`.
- Assunto/pré-header: antes `Seu presente de aniversário chegou adiantado 🎁` ·
  `10% OFF em tudo da Repeat com o cupom NIVER10.`; dia `Feliz niver! Hoje tem 15% OFF pra você` ·
  `Presente do dia: use NIVER15. Vale só hoje.`

**No Flash (empresa 467) — criado em 16/10/2026, inativo:**
- Templates **4142** "Repeat - Aniversario antes - 10% OFF" e **4143** "Repeat - Aniversario no dia - 15% OFF".
- Fluxo **2057** "Repeat - Aniversário (10% antes, 15% no dia)", só e-mail: gatilho Aniversário do
  Cliente, 7 dias antes (`trigger_config: {aniversario_mode: "antes", aniversario_dias: 7,
  offset_dias: 7}`; "depois" grava `offset_dias` negativo, "no dia" grava 0; máximo 30 dias) →
  e-mail NIVER10 (4142) → espera 7 dias → "Não comprou nos últimos 7 dias?" → Sim: e-mail NIVER15
  (4143) / Não: "Fluxo encerrado (comprou antes do dia)". Frequência "Com intervalo mínimo entre
  entradas: 300 dias" (`permitir_reentrada: true, intervalo_reentrada_dias: 300`) = uma vez por ano.
- Só dispara para quem tem data de nascimento cadastrada no Flash.
- O modelo "Aniversário" (1883) continua inativo: não ligar os dois.

**Pendências**
- **Ano que vem:** os cupons são de um uso por cliente, então no 2º aniversário o `NIVER10`/`NIVER15`
  já usado não funciona. Antes de out/2027: criar códigos novos (ex.: `NIVER10-27`) e trocar nos
  templates, ou passar para cupom por cliente do Flash.
- A Shopify não limita o `NIVER15` ao dia do aniversário de cada cliente: o texto diz "só hoje",
  mas o código vale sempre (um uso por cliente). Alternativa: cupom por cliente gerado pelo Flash
  ("Criar cashback") com validade de 1 dia, trocando `NIVER15` por `{{cupom}}`.
- O gatilho de aniversário do Flash (dias antes / no dia) e o filtro "não comprou desde o 1º e-mail"
  são configurados no fluxo.

---

## Reativação (`reativacao-40.mjml`, `reativacao-60.mjml`, `reativacao-90.mjml`)

Série para quem comprou uma vez e sumiu. Sem layout do Figma: design do brandbook, prefixo `rep-re-`,
imagens geradas por `assets/reativacao/_recortes.py`. Mesma composição nos três, com a cor do hero
escalando junto com o desconto: laranja (40) → laranja escuro (60) → vinho (90). Os `.mjml` são a
fonte: edite direto neles.

| Arquivo | Exibição | O que é |
|---|---|---|
| `rep-re-hero-40/60/90.jpg` | 600×540 | meia-lua no topo com o logo (como na embalagem), headline em HWT Artz ("BATEU SAUDADE?", "VOLTA VAI!", "NOSSO MAIOR DESCONTO"), estrela com 5%/10%/15% OFF e fileira de 5 pacotes subindo de trás de uma curva branca que emenda com a seção seguinte |
| `rep-re-crispy.jpg`, `rep-re-brownie.jpg`, `rep-re-ervilha.jpg` | 160×160 | cards de produto |
| `rep-cb-edamame/alga/coco.jpg`, `rep-cb-manifesto.jpg`, `rep-cb-logo.png` | — | reaproveitados do cashback |

| Dias | Cupom | CTA | Produtos |
|---|---|---|---|
| 40 | `VOLTA5` (5%) | QUERO MATAR A SAUDADE | Edamame, Alga, Cracker de Coco |
| 60 | `VOLTA10` (10%) | USAR MEUS 10% OFF | Crispy de Chocolate, Bombom de Brownie, Ervilha Crocante |
| 90 | `VOLTA15` (15%) | GARANTIR MEUS 15% OFF | Edamame, Crispy de Chocolate, Cracker de Coco |

- Cupons criados na Shopify em 16/10/2026: pedido inteiro, um uso por cliente, combinam só com frete.
- Os CTAs e o hero levam a `https://repeatonline.com.br/discount/VOLTAx?redirect=%2Fcollections%2Fall`
  (o cupom entra sozinho; testado, grava o cookie `discount_code`); os cards vão direto para a página
  do produto. O texto também diz pra digitar o código no checkout.
- Saudação `fc-if--primeiro_nome` / `fc-ifnot--primeiro_nome`. Rodapé vinho igual ao dos outros, com `{{link_optout}}`.
- Assuntos: `Bateu saudade? Tem 5% OFF te esperando` · `Subimos seu desconto pra 10%` ·
  `Nosso maior desconto pra você: 15% OFF`. Pré-headers: `Volte com o cupom VOLTA5 em todos os produtos.` ·
  `Use VOLTA10 em todos os produtos. O botão já aplica o cupom.` · `Cupom VOLTA15 em todos os produtos. Aproveita!`

**No Flash (empresa 467) — criado em 16/10/2026, inativo:**
- Templates **4144** (40 dias, VOLTA5), **4145** (60 dias, VOLTA10), **4146** (90 dias, VOLTA15).
  O 60 e o 90 foram montados no navegador a partir do 40 e conferidos por SHA-256 contra os `.mjml`.
- Fluxo **2058** "Repeat - Reativação 40/60/90 dias (5%, 10%, 15%)", só e-mail, 12 etapas: gatilho
  Cliente fez um pedido com filtro "Número de pedidos = 1" (comprou uma vez) → espera 40 dias →
  "Ainda só 1 pedido?" → Sim: e-mail VOLTA5 → espera 20 dias → "Ainda só 1 pedido?" → Sim: e-mail
  VOLTA10 → espera 30 dias → "Ainda só 1 pedido?" → Sim: e-mail VOLTA15. Cada "Não" encerra.
  Entrada apenas uma vez.
- **20/10/2026, a pedido do usuário: virou "dias sem comprar".** Gatilho Cliente fez um pedido **sem
  filtro**, entrada **"Sempre"** (`permitir_reentrada: true`, `intervalo_reentrada_dias: null`): toda
  compra de qualquer cliente começa uma contagem. As três condições agora são "Dias desde a última
  compra ≥ 40 / 60 / 90" (`{field: "recencia", operator: ">=", valueMin: N}`, mesmo formato do modelo
  Winback 1888), cada "Não" encerra. Quem compra no meio do caminho sai na próxima condição da contagem
  antiga e começa uma nova. 15 etapas (condição 40 = 13019, encerrado 40 = 13020).
- Os cupons VOLTA5/10/15 são de um uso por cliente: quem já usou e some de novo recebe o e-mail com um
  código que não funciona mais. Solução, se precisar: cupom por cliente via "Criar cashback".
- O modelo "Reativação (Winback)" (1888) continua inativo: não ligar os dois.

**Pendências**
- Mesmo gatilho do fluxo de 2ª compra (2056): o cliente recebe `SEGUNDA10` (10%) no 5º dia e, se não
  voltar, `VOLTA5` (5%) no 40º. Ou seja, a oferta cai antes de subir. Decidir se mantém, se o 40
  dias vira 10% ou se o fluxo de 2ª compra encerra quem já recebeu.
- Produtos sem preço. `fc-if` não testado em envio real.
- "Nosso maior desconto" vale dentro da régua de reativação. Se outra campanha der mais que 15%, rever o texto.

---

## Cashback (`cashback.mjml`)

**Guardado, vai mudar. Não está no Flash.** O usuário quer o cashback como "5% de cashback em cada
compra (acumulativo)": o cupom deixa de ser o `CASHBACK5` fixo e passa a vir da etapa "Criar
cashback" do fluxo (`criar_cashback`: `cashback_percentual`, `dias_inicio`, `dias_vencimento`,
`desconto_max_percentual`, como no modelo "Pós-compra bounceback"), com `{{cupom}}`,
`{{valor_cashback}}` e `{{data_vencimento}}` no e-mail. Revisar texto e hero ("5% OFF" vira "5% DE VOLTA").
- `CASHBACK5` na Shopify **desativado em 16/10/2026** (status EXPIRED) a pedido do usuário.

**Versão nativa do Flash — criada em 16/10/2026, inativa:**
- E-mail atualizado: hero `rep-cb-hero-v2.jpg` (selo "5% DE VOLTA"), texto com
  "R$ {{valor_cashback}}" (a variável vem só com o número, igual ao bloco "Cartão de cashback" do
  Flash), cupom `{{cupom}}`, "válido até {{data_vencimento}}"; botão e hero →
  `/discount/{{cupom}}?redirect=%2Fcollections%2Fall` (aplica o cupom do cliente).
- Template **4147** "Repeat - Cashback 5% (cada compra)".
- Fluxo **2059** "Repeat - Cashback 5% em cada compra", só e-mail: gatilho Cliente fez um pedido,
  sem filtro, entrada "Sempre" (toda compra) → espera 1 dia → **Criar cashback** (`criar_cashback`:
  5%, ativa na hora, vence em 30 dias, desconta até 25%; mesma etapa do "Cashback de agradecimento"
  do modelo 1887) → e-mail (4147). Assunto `Seu cashback de R$ {{valor_cashback}} chegou!` ·
  pré-header `Use o cupom {{cupom}} na próxima compra. Vale até {{data_vencimento}}.`
- "Acumulativo": o usuário acredita que o cashback nativo já cobre. No app e na central de ajuda
  cada cashback aparece como registro separado (cupom próprio); não achei opção de saldo somado.
  Conferir em Cashbacks depois das primeiras compras.
- O modelo "Pós-compra bounceback" (1887) também cria cashback (10%) na 1ª compra: não ligar os dois.

Sem layout do Figma: design criado a partir do brandbook. Prefixo `rep-cb-`. Imagens geradas por
`assets/cashback/_recortes.py` (2x, exibidas em 1x).

| Arquivo | Exibição | O que é |
|---|---|---|
| `rep-cb-logo.png` | 130×36 (topo) e 100×28 (rodapé) | logo branco com alfa |
| `rep-cb-hero.jpg` | 600×550 | "SEU CASHBACK CHEGOU!" em HWT Artz + estrela "5% OFF" + leque com 5 sabores de edamame; base creme `#f2e2dc` que emenda com a seção seguinte |
| `rep-cb-edamame.jpg`, `rep-cb-alga.jpg`, `rep-cb-coco.jpg` | 160×160 | cards de produto (fundo branco) |
| `rep-cb-manifesto.jpg` | 600×200 | "PRAZER QUE CABE NA SUA ROTINA." (sem vírgula: a fonte não tem) |

- Saudação: `fc-if--primeiro_nome` ("Oi, {{primeiro_nome}}!") / `fc-ifnot--primeiro_nome` ("Oi!").
- Passos "01. 02. 03." com `fc-nostack` (20%/80%, não empilham no celular).
- Cupom **`CASHBACK5` fixo no texto**. Regra criada na Shopify em 16/10/2026
  (`gid://shopify/DiscountCodeNode/1539343679708`): 5% no pedido inteiro, todos os clientes, sem
  mínimo, sem data de fim, **sem limite de uso por cliente** (o e-mail sai a cada compra), combina só
  com desconto de frete.
- CTAs → `https://repeatonline.com.br/discount/CASHBACK5?redirect=...` (aplica o cupom sozinho;
  testado: grava o cookie `discount_code=CASHBACK5`). Cards levam direto para a página do produto.
- Rodapé com `{{link_optout}}`.
- Assunto sugerido: `Seu cashback de 5% chegou` · Pré-header: `Use o CASHBACK5 na próxima compra. O botão já aplica o desconto.`

**Pendências**
- Se o fluxo usar a ação "Criar cashback" do Flash (cupom por cliente), trocar `CASHBACK5` por
  `{{cupom}}` no card e nos links, e dá para mostrar `{{valor_cashback}}`/`{{data_vencimento}}`.
- Já existe na loja o `5%CARRINHO` (um uso por cliente, combina com tudo). Confirmar se o
  `CASHBACK5` deve seguir o mesmo padrão.
- Produtos sem preço (preço fixo no e-mail fica velho). `fc-if`/`fc-nostack` não testados em envio real.
