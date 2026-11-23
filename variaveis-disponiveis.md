# Variáveis disponíveis

## Cliente
| Campo | Variável |
|---|---|
| Nome | `{{nome_cliente}}` |
| Sobrenome | `{{sobrenome}}` |
| E-mail | `{{email}}` |
| Telefone | `{{telefone}}` |

## Pedido
| Campo | Variável |
|---|---|
| Número do pedido | `{{numero_pedido}}` |
| Valor do pedido | `{{valor_pedido}}` |

## Cashback
| Campo | Variável |
|---|---|
| Valor do cashback | `{{valor_cashback}}` |
| Código do cupom | `{{cupom}}` |
| Data de vencimento | `{{data_vencimento}}` |
| Data de ativação | `{{data_ativacao}}` |
| Compra mínima | `{{compra_minima}}` |
| Desconto máximo | `{{desconto_max}}` |

## Carrinho abandonado
| Campo | Variável | Tipo |
|---|---|---|
| Total do carrinho | `{{carrinho_total}}` | texto |
| Link de recuperação | `{{carrinho_url}}` | texto |
| Qtd. de itens | `{{carrinho_qtd_itens}}` | número |
| Lista de produtos | `{{produtos_carrinho}}` | **texto pronto** ("Produto A, Produto B, Produto C") |
| Frete | `{{carrinho_frete}}` | texto |
| **Lista iterável de produtos** | **`produtos`** | **lista** — não aparece na interface |

### O loop dos itens
A coleção que itera é **`produtos`**, não `produtos_carrinho`:

```handlebars
{{#each produtos}}
  {{this.nome}} · {{this.preco}}
{{/each}}
```

`produtos_carrinho` é só uma string de resumo; `{{#each}}` nela nunca roda.

## Cross-sell dinâmico (não são variáveis da plataforma)
O `compra-aprovada.html` espera estas flags no payload do envio. Não existem por padrão — quem
liga é o fluxo da automação (ver README §7). Sem nenhuma delas, o e-mail cai no card padrão.

| Flag | Card que aparece |
|---|---|
| `{{comprou_gaba}}` | Creatina |
| `{{comprou_creatina}}` | Fibras |
| — (inclusive quem comprou Fibras) | Gaba |

## O que o motor de template aceita (verificado em teste real)
| | Sintaxe |
|---|---|
| ✅ | `{{variavel}}` |
| ✅ | `{{#if x}}...{{else}}...{{/if}}` |
| ✅ | `{{#each produtos}}{{this.campo}}{{/each}}` |
| ❌ | `{{else}}` dentro de `{{#each}}` — **vaza como texto visível no e-mail** |
| ❌ | alias `as \|item\|` |
| ❌ | `@index`, `@root` |
| ❌ | índice direto (`produtos.0.nome`) |
| ❌ | section estilo Mustache (`{{#produtos}}`) |
| ❌ | sintaxe Liquid (`{% for %}`) |

Também importante: o build passa por **MJML**. Nunca coloque `<link>` ou `@import` de webfont
no `<head>` (vira `mj-font` e quebra), e nunca anote o template com comentário HTML contendo
tags `{{ }}` — use comentário Handlebars.

## Não existem (usadas no template como placeholder manual)
- Descadastro / preferências de e-mail
- Links de Sobre nós, FAQ, Meus pedidos
- Endereço do remetente
- Subtotal do carrinho (só existe o total)
- Subtotal, frete e código de rastreio do **pedido** (só existem `{{numero_pedido}}` e `{{valor_pedido}}`)
- Lista de itens do **pedido** — o `{{#each produtos}}` do `compra-aprovada.html` reaproveita a
  coleção do carrinho abandonado e ainda não foi confirmado em envio real
