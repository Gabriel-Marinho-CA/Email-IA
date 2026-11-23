# E-mails Nüma — o que a gente aprendeu

> **Formato antigo (out/2026).** Estes templates são HTML colado no bloco "HTML" do Flash, que hoje
> vira um bloco só (`mj-raw`). Templates novos são **MJML** importado pelo favorito "Importar MJML"
> (ver `../FLASHCRM-EMAIL-E-FLUXOS-PARA-DEV.md` e `../CLAUDE.md`). O descadastro atual é
> `{{link_optout}}`; o `%UNSUBSCRIBELINK%` daqui é do formato antigo. As lições de Handlebars e de
> e-mail abaixo continuam valendo.

Notas de quem já tropeçou. Leia antes de mexer nos templates.

---

## 1. O pipeline

O HTML que você escreve **não** é o HTML que sai. Ele passa por duas etapas antes de virar e-mail:

```
seu HTML  →  Handlebars (troca as variáveis)  →  MJML (build)  →  e-mail enviado
```

Cada etapa tem suas próprias regras, e as duas já quebraram o build por motivos não óbvios.
Os detalhes estão nas seções 2 e 3.

---

## 2. Handlebars — o subset que a plataforma entende

Não é o Handlebars completo. É um subset, e a documentação da plataforma não diz qual.
Isto aqui foi levantado enviando e-mails de teste com cada sintaxe:

| | Sintaxe | Observação |
|---|---|---|
| ✅ | `{{variavel}}` | |
| ✅ | `{{#if x}}...{{else}}...{{/if}}` | o `else` funciona **aqui** |
| ✅ | `{{#each produtos}}{{this.campo}}{{/each}}` | sempre com o prefixo `this.` |
| ❌ | `{{else}}` dentro de `{{#each}}` | **vaza como texto visível no e-mail** |
| ❌ | alias `as \|item\|` | sai literal |
| ❌ | `@index`, `@root` | saem literais |
| ❌ | índice direto (`produtos.0.nome`) | sai literal |
| ❌ | section Mustache (`{{#produtos}}`) | sai literal |
| ❌ | Liquid (`{% for %}`) | não é Liquid |

### A pegadinha do nome da coleção

A interface lista **`{{produtos_carrinho}}`** como "Lista de Produtos". Ela **não é uma lista** —
é uma string pronta: `"Produto A, Produto B, Produto C"`. Um `{{#each}}` nela nunca roda, e
falha em silêncio: sem erro, sem aviso, só um card vazio.

A coleção que realmente itera se chama **`produtos`**, e **não aparece na interface**:

```handlebars
{{#each produtos}}
  {{this.nome}} · {{this.preco}}
{{/each}}
```

Campos confirmados por item: `nome`, `descricao`, `quantidade`, `preco`, `preco_original`,
`imagem`, `url`.

> Moral: quando um `{{#each}}` vier vazio, teste se a variável é mesmo uma lista antes de
> mexer na sintaxe. As duas falhas são idênticas na tela.

---

## 3. MJML — duas armadilhas

**Webfont no `<head>` quebra o build.** Um `<link href="fonts.googleapis.com...">` vira uma tag
`mj-font` malformada e derruba tudo com `mj-attributes cannot be used inside mj-font`. Nunca use
`<link>` nem `@import` de fonte. Não é perda real: Gmail, Outlook e Yahoo ignoram webfont de
qualquer jeito — só o Apple Mail carregava. A stack de fallback (`.f`) resolve.

**Comentário HTML com tag Handlebars dentro também quebra.** O compilador lê as tags dentro de
`<!-- -->` e tenta interpretá-las: um `{{#if}}` numa nota explicativa abre um bloco que nunca
fecha. Anote o template com `{{!-- comentário Handlebars --}}`.

E um detalhe do próprio comentário Handlebars: se você escrever `--}}` no meio do texto, ele
fecha ali e o resto da nota aparece no e-mail. Já aconteceu.

> **Atualização (set/2026):** melhor ainda é não comentar. O `{{!-- --}}` aparece como texto
> quando o HTML é aberto no navegador ou colado num editor. Anotações vão no README.

---

## 4. HTML de e-mail — o que vale para este projeto

**Layout é tabela.** Nada de flex, grid ou `position`. Container de 600px, `role="presentation"`
em toda tabela de layout.

**SVG não existe.** Gmail bloqueia. Todo ícone e ilustração vira PNG.

**O que o HTML não faz, vira imagem.** Rotação, blur e texto em curva não existem em e-mail. No
template de carrinho, três blocos foram exportados do Figma como PNG único: o marquee do topo, o
hero com o selo girado e a faixa de selos inclinada.

**Mas só isso.** Todo o resto é texto real — headline, card, preços, lista de diferenciais,
rodapé. Melhor para acessibilidade, para dark mode e para não cair em spam por excesso de imagem.

**Espaçamento vem de linha espaçadora, não de margin.** `margin` é ignorada em vários clientes.

**Divisor de 1px não leva `padding` no mesmo `<td>` do fundo colorido** — o padding entra dentro
do fundo e o "1px" vira uma barra de 17px. Use uma linha espaçadora antes e outra depois.

**Botão precisa de VML** para o Outlook desktop, junto do `<a>` normal para os outros clientes.

**Responsivo** com uma `@media (max-width:600px)` e `!important` em tudo — o container vai a 100%,
as imagens ficam fluidas, a headline encolhe, o botão vira bloco e os links do rodapé empilham.

**Crop de imagem sem editor:** o CDN do Shopify aceita `&width=132&height=132&crop=bottom` na URL.
Foi assim que o thumb de 66px saiu de uma foto de 1086×1448 com dois produtos empilhados.
Sempre exporte o dobro do tamanho de exibição, por causa de tela retina.

**Gradiente que atravessa seções tem que fechar na emenda.** Cada seção é um `<td>` separado, então
o degradê é picotado: a cor onde um termina precisa ser exatamente a cor onde o próximo começa. E o
degradê tem que ser vertical. O `recompra.html` usava um `radial-gradient(... at 50% 100%)` na
seção de produtos: como a cor da borda de baixo variava na horizontal (escura no meio, clara nas
pontas) e a seção seguinte começava chapada, a emenda virava uma listra visível de ponta a ponta.
Virou `linear-gradient(180deg, #faf6fd → #e6ddf2)`, que entrega em `#e6ddf2` — a cor com que a
seção de benefícios abre. Lembrando que Outlook ignora gradiente: o `bgcolor` de fallback tem que
ser um tom do meio da rampa, não a cor de uma das pontas.

**PNG exportado do Figma vem com o fundo da seção junto.** Se o elemento não tinha fundo próprio, o
Figma preenche com o fundo do frame e salva opaco. Em cima de uma cor chapada ninguém nota; em cima
de um degradê, aparece uma caixa retangular em volta. Foi o caso das pílulas do `recompra.html` —
os cantos arredondados vinham preenchidos de `#faf6fd`. Ou reexporte com fundo transparente, ou
apague o fundo com um flood fill a partir dos quatro cantos (só o lado de fora é atingido, o
miolo claro da pílula fica intacto).

---

## 5. Como testar antes de mandar

Não confie na leitura. Compile e olhe. O ciclo completo é rápido:

```bash
npm install handlebars          # dentro de uma pasta temporária, não na raiz do projeto
node render.js                  # compila o template com dados de exemplo
```

```js
const H = require('handlebars');
const tpl = H.compile(fs.readFileSync('carrinho-abnadonado.html', 'utf8'));
fs.writeFileSync('out.html', tpl(dados));
```

Compilar de verdade pega o que ler não pega: bloco não fechado, `{{` sobrando no HTML final,
`else` vazando como texto.

**Sempre teste com dados imperfeitos:** um produto sem `preco_original`, um sem `imagem`, um com
nome longo, e o carrinho com mais de um item. Foi assim que os `{{#if}}` de fallback se provaram.

Para ver o resultado:

```bash
chrome --headless=new --window-size=900,2200 --screenshot=out.png out.html
```

O headless tem uma **largura mínima de janela** — pedir `--window-size=375` não ativa a media
query. Para testar mobile, coloque a página num `<iframe style="width:375px">` dentro de uma
janela larga.

⚠️ `npm install` sobe a árvore procurando um `package.json`. Rode dentro de uma pasta temporária
com `package.json` próprio, ou ele instala na sua pasta de usuário.

---

## 6. Arquivos

| Arquivo | O que é |
|---|---|
| `carrinho-abnadonado.html` | template de carrinho abandonado (Figma → e-mail) |
| `recompra.html` | template de recompra — usa `{{nome_cliente}}` na saudação |
| `compra-aprovada.html` | template de pagamento aprovado / confirmação de pedido |
| `lembrete-30-dias.html` / `lembrete-60-dias.html` | lembretes de recompra |
| `variaveis-disponiveis.md` | todas as variáveis da plataforma, por categoria |
| `assets/` | PNGs exportados do Figma — já estão no CDN, servem de backup |

Cada template tem sua pasta dentro de `assets/` (ex.: `assets/recompra/`), porque os nomes de
arquivo se repetem entre templates (todo e-mail tem seu `hero`, seu `logo-rodape`).

**A pasta separa, mas o CDN não.** A biblioteca de arquivos do Shopify é um namespace plano: subir
um segundo `marquee-topo.png` não substitui nem convive — o Shopify renomeia sozinho para
`marquee-topo_86764102-d368-....png` e a URL do template quebra. Foi o que aconteceu no
`recompra.html`. Por isso os arquivos de `assets/compra-aprovada/` já vêm prefixados com
`aprovado-`: sobe a pasta inteira sem renomear nada e as URLs do HTML batem de primeira.

As imagens em produção vêm do CDN do Shopify. Caminho relativo (`assets/foto.png`) **não funciona
em e-mail** — a URL precisa ser absoluta.

### Placeholders sem variável correspondente

Estes ficaram como `%TEXTO%` no template porque a plataforma não expõe variável equivalente —
preencha na mão: `%UNSUBSCRIBELINK%`, `%LINK_PREFERENCIAS%`, `%LINK_SOBRE%`, `%LINK_FAQ%`,
`%LINK_PEDIDOS%`, `%SENDER-INFO-SINGLELINE%`.

Também não existe subtotal do carrinho — só `{{carrinho_total}}` e `{{carrinho_frete}}`. Por isso
a linha "Subtotal" do design do Figma foi removida do card: sem a variável, ela repetiria o total
e ficaria errada sempre que o frete não fosse grátis.

### O que falta no e-mail de pedido aprovado

Para pedido a plataforma só expõe `{{numero_pedido}}` e `{{valor_pedido}}`. Não há subtotal, frete,
código de rastreio nem lista de itens documentada. Consequências no `compra-aprovada.html`:

- **Subtotal e Frete saíram do card** pelo mesmo motivo do carrinho — sem variável, mentiriam.
- **A lista de itens usa `{{#each produtos}}`**, a mesma coleção não documentada do carrinho
  abandonado. Não foi confirmada em pedido aprovado: se o teste real vier com o card sem itens,
  é porque a plataforma não expõe a lista aqui — apague o bloco e deixe só o Total.
- **O CTA aponta para a página de conta do Shopify**
  (`https://shopify.com/76420317229/account`), não para um rastreio. A barra de status é
  ilustrativa: sempre mostra "Pagamento aprovado" ativo, porque não existe variável de status.
- **Os cards de cross-sell já estão com link e preço reais** (`sejanuma.com.br/products/...`):
  Gaba R$ 129,00 · Creatina R$ 159,00 · Prebiotic Superfood R$ 129,90. O preço riscado do design
  saiu dos quatro cards — não existe preço "de", e repetir o mesmo valor riscado seria mentira.

---

## 7. Cross-sell dinâmico (compra-aprovada)

A seção de cross-sell tem **quatro cards** e mostra **um só**, escolhido pelo que o cliente comprou:

| Comprou | Recebe | Link |
|---|---|---|
| Gaba | Creatina · R$ 159,00 | `/products/creatina-em-gummie` |
| Creatina | Fibras · R$ 129,90 | `/products/prebiotic-superfood` |
| Fibras · ou nenhuma flag | Gaba · R$ 129,00 | `/products/gaba-relax` |

São **três cards**, não quatro: o card do Daily Superfood está comentado (`{{!-- ... --}}`) logo
abaixo do último `{{else}}`, caso um dia volte. "Comprou Fibras" e "não veio flag nenhuma" caem no
mesmo ramo — o `{{else}}` final — e os dois mostram Gaba. Por isso só existem dois `{{#if}}`.

A ordem dos `{{#if}}` **é** a prioridade: quem comprou Gaba + Fibras cai no primeiro ramo e vê
Creatina. Para trocar a regra, basta reordenar os blocos.

### O que o template não consegue fazer sozinho

A decisão **não sai do `{{#each produtos}}`**. Dentro do loop só existe `this.campo`, e o subset da
plataforma não tem comparação: não há `{{#if (eq this.nome "Gaba")}}`, não há `@root` para voltar ao
contexto de fora, e `{{else}}` dentro do `each` vaza como texto. `{{#if}}` só testa se o valor é
vazio ou não — nunca *qual* valor é.

Por isso o gatilho são **flags booleanas planas**, avaliadas fora do loop:

```handlebars
{{#if comprou_gaba}}              card Creatina
{{else}}{{#if comprou_creatina}}  card Fibras
{{else}}                          card Gaba  (comprou Fibras, ou nenhuma flag)
{{/if}}{{/if}}
```

`comprou_fibras` nem é lida: quem comprou Fibras cai no `{{else}}` final junto com quem não trouxe
flag nenhuma. Quem preenche `comprou_gaba` / `comprou_creatina` é a **plataforma**, não o
template. Dois caminhos, na ordem de preferência:

1. **Condição no fluxo da automação** — a maioria dos builders tem filtro "pedido contém o produto
   X". Uma branch por produto, cada uma mandando o mesmo template com a flag ligada. Não depende de
   nenhuma variável nova.
2. **Variável customizada no envio** — se a plataforma deixa criar campo próprio no payload, mande
   `comprou_gaba: true`. Mais limpo, mas só funciona se ela expuser isso.

Se nenhuma flag chegar, o e-mail não quebra: cai no card padrão.

### Vale testar antes de aceitar a limitação

O subset foi levantado por tentativa e erro e pode ter mais do que a gente descobriu. Um envio de
teste com estas três linhas responde se dá para tornar tudo automático, sem flag nenhuma:

```handlebars
A: {{#each produtos}}{{#if (eq this.nome "Gaba")}}ACHOU{{/if}}{{/each}}
B: {{#each produtos}}[{{this.nome}}]{{/each}}
C: {{#if produtos_carrinho}}TEM{{/if}}
```

Se **A** imprimir `ACHOU` (e não vazar o `(eq ...)` como texto), o subset tem subexpressão e a regra
pode viver inteira dentro do `{{#each}}` — aí o card de cross-sell entra no loop e some a
necessidade de flag.
