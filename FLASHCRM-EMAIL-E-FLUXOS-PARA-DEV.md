# FlashCRM — como importar e-mails (MJML) e fluxos (JSON) — documento para Dev

> **Arquivo único e autossuficiente.** Tudo que é preciso está aqui dentro: como o Flash funciona por
> baixo, o formato dos dados, o código completo dos favoritos (legível e pronto para colar), exemplos
> reais e o que foi e não foi testado.
>
> **Levantado em 14/10/2026** na conta de cliente Fui ao Mar (empresa_id 97), acessada pelo painel de
> parceiro da Turbo Partners. Nada disso é API oficial do Flash: é engenharia reversa do front-end.
> Uma atualização do Flash pode quebrar qualquer parte.

---

## Sumário

1. Contexto e objetivo
2. Como criar um favorito no navegador ("Adicionar página")
3. **E-mail** — o que o Flash usa por trás (GrapesJS + MJML)
4. E-mail — o importador escondido e o favorito "Importar MJML"
5. E-mail — regras de MJML no Flash (blocos, armadilhas, condicionais, produtos, variáveis)
6. E-mail — exemplo real completo
7. **Fluxos** — o que o Flash usa por trás (Next.js + React Query + Supabase RPC)
8. Fluxos — formato JSON de um fluxo
9. Fluxos — favoritos "Exportar fluxo" e "Importar fluxo" (código completo)
10. Fluxos — exemplo real completo
11. O que foi testado, o que não foi, riscos
12. Observações encontradas na conta durante a investigação
13. O que seria ideal o Flash oferecer oficialmente

---

## 1. Contexto e objetivo

Na implantação de CRM no FlashCRM a gente monta, por cliente, dezenas de templates de e-mail e
vários fluxos (carrinho, pós-compra, cashback, winback…). Fazer tudo à mão no editor é lento e
propenso a erro. O objetivo era:

- **E-mail:** gerar o e-mail em código (por IA ou à mão) e colar no Flash de forma que ele **entre
  quebrado nos blocos nativos do construtor** (Texto, Imagem, Botão…), e não como um bloco HTML único.
- **Fluxo:** conseguir **exportar** um fluxo pronto e **importar** em outra conta/loja, montando uma
  biblioteca de fluxos padrão.

O Flash não tem botão para nenhuma das duas coisas. Mas as funções existem no front-end, e dá para
chamá-las com um **favorito de navegador (bookmarklet)**.

---

## 2. Como criar um favorito no navegador ("Adicionar página")

Um bookmarklet é um favorito cuja URL começa com `javascript:`. Ao clicar, o navegador executa aquele
código **na página aberta naquele momento**, com o mesmo acesso que a própria página tem. Não instala
nada, não pede senha, não guarda login.

No Chrome:

1. Mostre a barra de favoritos: `Cmd + Shift + B` (Mac) / `Ctrl + Shift + B` (Windows).
2. Botão direito na barra → **Adicionar página…**
3. **Nome:** o nome do favorito (ex.: `Importar MJML`).
4. **URL:** apague o que tiver e cole o código inteiro (começa com `javascript:`).
5. **Salvar.**

Alternativa sem favorito: abrir o console (`Cmd + Option + J`), colar o código **sem** o prefixo
`javascript:` e Enter. Na primeira vez o Chrome exige digitar `allow pasting`.

> Segurança: os favoritos deste documento **não leem token, cookie nem senha**. Eles reutilizam
> objetos que o próprio Flash já criou na página (o editor de e-mail e a função de salvar fluxo),
> então só fazem o que o usuário logado já poderia fazer clicando.

---

## 3. E-mail — o que o Flash usa por trás

**O editor de e-mail do FlashCRM é GrapesJS com o plugin MJML.** (Até ~ago/2026 era Unlayer; mudou.)

- **GrapesJS** — framework open-source de construtor visual (drag-and-drop). Classes `gjs-*` / `eb-gjs`
  no DOM. O canvas é um `<iframe>`.
- **MJML** — linguagem de marcação open-source para e-mail (https://documentation.mjml.io). Cada
  componente do GrapesJS é uma tag MJML: `mjml`, `mj-body`, `mj-section`, `mj-column`, `mj-text`,
  `mj-image`, `mj-button`, `mj-divider`, `mj-spacer`, `mj-social`, `mj-social-element`, `mj-navbar`,
  `mj-raw`, `mj-hero`, `mj-wrapper`, `mj-group`, `mj-head`, `mj-style`, `mj-font`. Além de tipos do
  Flash: `merge-tag`, `data-variable`, `data-collection`, `data-condition`. A detecção é por tagName.
- No envio, o MJML é compilado para o HTML de tabelas compatível com Gmail/Outlook/celular.

**Por que isso importa:** colar HTML comum no bloco "HTML" vira **um bloco único** (`mj-raw`), só
editável no código. Importar **MJML** faz cada tag virar o bloco nativo correspondente — editável no
painel como se tivesse sido montado à mão.

### Como chegar no editor pelo JavaScript

Os elementos dentro do iframe do canvas têm a propriedade `__gjsv` (a view do GrapesJS). A partir dela:

```js
const iframe = [...document.querySelectorAll('iframe')].find(f => f.contentDocument?.querySelector('*'));
const el = [...iframe.contentDocument.querySelectorAll('*')].find(e => e.__gjsv);
const em = el.__gjsv.em;                 // EditorModel
const editor = em.getEditor();           // API pública do GrapesJS
```

API disponível: `getProjectData`, `loadProjectData`, `setComponents`, `addComponents`, `getHtml`,
`runCommand`, `Blocks`, `Components`, `getWrapper()`…

**Comandos registrados** (via `editor.Commands`): `mjml-import` (abre o modal "Import MJML" com
CodeMirror e botão Import — **substitui o template inteiro**), `mjml-code`, `mjml-code-to-html`,
`export-template`, `core:open-code`. **Nenhum deles tem botão na interface.**

**Blocos da paleta** são strings MJML sem hooks de drop — arrastar um bloco é o mesmo que fazer parse
do MJML dele. IDs: `eb-section, eb-text, eb-image, eb-button, eb-social, eb-menu, eb-divider,
eb-spacer, eb-html, eb-pronta-topbar, eb-pronta-header_logo, eb-pronta-hero_foto, eb-pronta-saudacao,
eb-pronta-cartao_cupom, eb-pronta-cartao_cashback, eb-pronta-beneficios, eb-pronta-passos,
eb-pronta-depoimento, eb-pronta-resumo_67_33, eb-pronta-categorias, eb-data-resumo-carrinho,
eb-data-condicional, eb-data-produtos-carrinho, eb-data-produtos-pedido, eb-produto`.
Para ver o MJML de qualquer um: `editor.Blocks.get('eb-pronta-saudacao').get('content')`.

Rotas do editor: `/templates/novo?tipo=email` (novo), `/templates/ia` (gerador por IA, não avaliado),
`/templates/branding`, `/templates/blocos-globais`. Botão de salvar: "Criar Template" (novo) /
"Salvar" (existente).

---

## 4. E-mail — o favorito "Importar MJML"

### Código legível

```js
(() => {
  for (const f of document.querySelectorAll('iframe')) {
    let d;
    try { d = f.contentDocument; } catch (e) { continue; }
    if (!d) continue;
    const v = [...d.querySelectorAll('*')].find(e => e.__gjsv);
    if (v) {
      const em = v.__gjsv.em;
      const ed = (em.getEditor && em.getEditor()) || em.Editor;
      ed.runCommand('mjml-import');   // abre o modal nativo "Import MJML"
      return;
    }
  }
  alert('Abra um template de e-mail no editor do Flash primeiro.');
})();
```

### Pronto para colar na URL do favorito

```
javascript:(()=>{for(const f of document.querySelectorAll('iframe')){let d;try{d=f.contentDocument}catch(e){continue}if(!d)continue;const v=[...d.querySelectorAll('*')].find(e=>e.__gjsv);if(v){const em=v.__gjsv.em;const ed=(em.getEditor&&em.getEditor())||em.Editor;ed.runCommand('mjml-import');return}}alert('Abra um template de e-mail no editor do Flash primeiro.')})()
```

### Uso

1. **Templates → Criar Template → E-mail** (ou `/templates/novo?tipo=email`).
2. Clicar no favorito → abre o modal **Import MJML**.
3. Apagar o conteúdo do modal, colar o MJML, clicar **Import**.
4. Conferir; arrastar o bloco dinâmico de produtos se for e-mail de carrinho/pedido (ver 5.5).
5. Nomear e **Criar Template**.
6. No passo do fluxo: escolher o template + preencher **assunto** e **pré-header** (não vão no MJML) →
   Aplicar → Salvar → recarregar e conferir.

### Alternativa programática (sem modal)

```js
editor.setComponents(mjmlString);   // mesmo efeito do Import: substitui tudo
editor.getHtml();                   // HTML compilado, para conferir
```

---

## 5. E-mail — regras de MJML no Flash

### 5.1 Bloco da paleta → MJML que ele gera

| Bloco | MJML |
|---|---|
| Seção | `<mj-section padding="0"><mj-column></mj-column></mj-section>` |
| Texto | `<mj-text padding="10px 25px" font-size="14px" color="#1A1A1A" line-height="1.5">…</mj-text>` |
| Imagem | `<mj-image src="" alt="" padding="10px 25px" fluid-on-mobile="true">` |
| Botão | `<mj-button background-color="#000000" color="#FFFFFF" border-radius="6px" font-size="14px" padding="10px 25px" href="#">Clique aqui</mj-button>` |
| Divisor | `<mj-divider border-color="#e5e7eb" border-width="1px" padding="10px 25px">` |
| Espaço | `<mj-spacer height="32px">` |
| Social | `<mj-social>` + `<mj-social-element>` |
| Menu | `<mj-section css-class="eb-menu">` + `<mj-text>` por item |
| HTML | `<mj-raw><tr><td style="padding:0;" class="fc-html-block">…</td></tr></mj-raw>` |

As **Seções prontas** são combinações desses mesmos componentes.

### 5.2 Estrutura

1. Todo conteúdo dentro de `mj-section` → `mj-column`.
2. Duas colunas = duas `mj-column width="50%"` na mesma seção (até 4).
3. `mj-text` aceita HTML inline (`<strong>`, `<em>`, `<a>`, `<br>`, `<span style>`).
4. Largura 600px. Só fontes email-safe (Arial, Helvetica, Georgia, Times New Roman, Verdana, Tahoma,
   Trebuchet MS, Courier New).
5. CTA principal: `mj-button width="100%"`.

### 5.3 Armadilhas

- **Padding por lado, não em atalho.** O importador adiciona `padding-top/right/bottom/left` com
  valores padrão. O HTML final sai certo (o atalho vence na compilação), mas o painel lateral mostra
  os padrões. Escreva sempre `padding-top="…" padding-right="…" padding-bottom="…" padding-left="…"`.
- **O canvas do editor não mostra o padding de seção** (CSS do canvas zera o padding do `td` — vale
  inclusive para as seções prontas do Flash). O HTML compilado/enviado tem o padding. Para ver o real,
  usar "Visualizar" ou `editor.getHtml()`.
- **Import substitui tudo.** Não existe "importar e somar".
- **`mj-raw` é dívida:** vira um bloco só, editável só no código.

### 5.4 Conteúdo condicional

| `css-class` na `mj-section` | A seção aparece quando |
|---|---|
| `fc-if--VARIAVEL` | a variável tem valor |
| `fc-ifnot--VARIAVEL` | a variável está vazia |
| `fc-nostack` | (outra função) colunas não empilham no celular |

```xml
<mj-section css-class="fc-if--primeiro_nome">…Olá, {{primeiro_nome}}…</mj-section>
<mj-section css-class="fc-ifnot--primeiro_nome">…Olá!…</mj-section>
```

O editor reconhece: mostra a seção `fc-ifnot--` com o rótulo "Só quando Primeiro nome está vazio".
No canvas as duas aparecem; no envio só uma (**inferido** — o bloco pronto "Saudação" do Flash usa
exatamente isso; envio real não testado).

Condicional Handlebars (bloco "Condicional"):

```xml
<mj-raw>{{#if is_vip}}</mj-raw>
<mj-section>…</mj-section>
<mj-raw>{{/if}}</mj-raw>
```

### 5.5 Blocos dinâmicos de produto

São MJML comum marcado por comentários:

| Bloco | Marcador | Onde funciona |
|---|---|---|
| Produtos do Carrinho | `<!-- eb:produtos-carrinho … -->` … `<!-- /eb:produtos-carrinho -->` | só fluxo de carrinho |
| Produtos do Pedido | `<!-- eb:produtos-pedido … -->` | só fluxos de pedido |
| Produto (estático) | `<!-- eb:produto-estatico … -->` | qualquer lugar |
| Resumo do carrinho | `{{{produtos_carrinho_html}}}` | só fluxo de carrinho |

```xml
<mj-wrapper>
  <mj-raw><!-- eb:produtos-carrinho layout=grade card-layout=vertical colunas=1 botao=1 botao-destino=carrinho_url texto-botao=Voltar%20ao%20meu%20carrinho --></mj-raw>
  <mj-section css-class="eb-evt-card" padding="0">
    <mj-column css-class="eb-evt-col" padding="16px">
      <mj-image css-class="eb-field-imagem" src="" alt="Produto"></mj-image>
      <mj-text css-class="eb-field-nome" font-weight="700">Nome do produto</mj-text>
      <mj-text css-class="eb-field-quantidade">Qtd: 2</mj-text>
      <mj-text css-class="eb-field-preco" font-weight="800">R$ 149,90</mj-text>
      <mj-button css-class="eb-field-botao" href="{{carrinho_url}}">Voltar ao meu carrinho</mj-button>
    </mj-column>
  </mj-section>
  <mj-raw><!-- /eb:produtos-carrinho --></mj-raw>
</mj-wrapper>
```

**Recomendação:** importar sem o bloco dinâmico e arrastar o bloco nativo depois (garante a config
que o painel espera). Fora do fluxo certo, o bloco some do e-mail enviado sem aviso.

### 5.6 Variáveis (registro do próprio Flash)

> `{{nome_cliente}}` agora é o **nome completo**. Para "Olá, Maria" use `{{primeiro_nome}}`.

Cond. = pode ser usada em `fc-if--`/`fc-ifnot--`.

| Grupo / contexto | Variável | Cond. |
|---|---|---|
| Cliente (campanha e qualquer fluxo) | `primeiro_nome`, `nome_cliente`, `sobrenome`, `email`, `telefone` | ✅ todas |
| Pedido (`fluxo:pedido`) | `numero_pedido`, `status_pedido`, `url_rastreio`, `codigo_rastreio`, `transportadora`, `status_entrega` | ✅ |
| | `valor_pedido` | — |
| Pagamento (`fluxo:pedido`) | `pix_copia_cola`, `boleto_url`, `boleto_linha_digitavel`, `url_pagamento` | ✅ |
| Cashback (`fluxo:cashback`) | `valor_cashback`, `cupom`, `data_vencimento`, `data_ativacao`, `desconto_max` | ✅ |
| | `compra_minima` | — |
| Carrinho (`fluxo:carrinho`) | `carrinho_url`, `carrinho_produto_nome`, `carrinho_produto_imagem`, `carrinho_url_caminho`, `produtos_carrinho` | ✅ |
| | `carrinho_total`, `carrinho_qtd_itens`, `carrinho_frete` | — |
| Links (todos) | `link_optout`, `unsubscribe_url` (um dos dois obrigatório no rodapé) | — |
| Gatilho aniversário | `idade_aniversario` (não reconferida no editor novo) | |
| Gatilho RFM | `segmento_rfm`, `segmento_rfm_anterior` (não reconferidas) | |

Fora do contexto, a variável sai vazia.

### 5.7 Outras regras

- **Assunto e pré-header não vão no MJML** — ficam no passo do fluxo/campanha.
- Imagens: evitar `.webp` (Outlook desktop); testar a URL alternativa (`.jpg`/`.png` variam por loja);
  `alt` em toda `mj-image`; amostrar o hex do fundo da foto/logo para a seção.
- CTA sempre `mj-button`, nunca imagem. Texto real, nunca dentro da arte.
- Rodapé com `{{link_optout}}`, razão social, CNPJ e endereço.

---

## 6. E-mail — exemplo real completo

"Carrinho 1 – NS" da Fui ao Mar. **Testado:** importado em template novo → 7 `mj-section`, 7
`mj-column`, 13 `mj-text`, 1 `mj-button`, 1 `mj-image`, 1 `mj-divider`, zero erros de compilação,
HTML final de 25 KB com logo, `{{primeiro_nome}}`, `{{carrinho_url}}`, `{{link_optout}}` e as classes
`fc-if--`/`fc-ifnot--` presentes. Não foi salvo.

Assunto (no passo do fluxo): `Ficou algo no seu carrinho` · Pré-header: `As latas que você separou continuam disponíveis.`

```xml
<mjml>
  <mj-body background-color="#EEF2F7" width="600px">

    <!-- CABEÇALHO -->
    <mj-section background-color="#FFFFFF" padding-top="28px" padding-right="32px" padding-bottom="0px" padding-left="32px">
      <mj-column>
        <mj-image src="https://acdn-us.mitiendanube.com/stores/001/464/658/themes/common/logo-401111844-1715103331-b4ac86419d9ab99d6d6aaa28a9a3232c1715103331.png" alt="Fui ao Mar" width="190px" href="https://www.fuiaomar.com.br/" padding-top="0px" padding-right="0px" padding-bottom="22px" padding-left="0px"></mj-image>
        <mj-divider border-color="#DDE3EC" border-width="1px" padding-top="0px" padding-right="0px" padding-bottom="0px" padding-left="0px"></mj-divider>
      </mj-column>
    </mj-section>

    <!-- TÍTULO -->
    <mj-section background-color="#FFFFFF" padding-top="34px" padding-right="32px" padding-bottom="0px" padding-left="32px">
      <mj-column>
        <mj-text font-family="Arial, Helvetica, sans-serif" font-size="11px" line-height="16px" letter-spacing="2.6px" color="#8A93A6" padding-top="0px" padding-right="0px" padding-bottom="14px" padding-left="0px">CARRINHO</mj-text>
        <mj-text font-family="Georgia, 'Times New Roman', serif" font-size="30px" line-height="36px" color="#111D43" padding-top="0px" padding-right="0px" padding-bottom="18px" padding-left="0px">Ficou algo no seu carrinho.</mj-text>
      </mj-column>
    </mj-section>

    <!-- ABERTURA: com nome -->
    <mj-section css-class="fc-if--primeiro_nome" background-color="#FFFFFF" padding-top="0px" padding-right="32px" padding-bottom="0px" padding-left="32px">
      <mj-column>
        <mj-text font-family="Arial, Helvetica, sans-serif" font-size="16px" line-height="25px" color="#5A6478" padding-top="0px" padding-right="0px" padding-bottom="14px" padding-left="0px">Olá, {{primeiro_nome}}. As latas que você separou continuam disponíveis.</mj-text>
      </mj-column>
    </mj-section>

    <!-- ABERTURA: sem nome -->
    <mj-section css-class="fc-ifnot--primeiro_nome" background-color="#FFFFFF" padding-top="0px" padding-right="32px" padding-bottom="0px" padding-left="32px">
      <mj-column>
        <mj-text font-family="Arial, Helvetica, sans-serif" font-size="16px" line-height="25px" color="#5A6478" padding-top="0px" padding-right="0px" padding-bottom="14px" padding-left="0px">As latas que você separou continuam disponíveis.</mj-text>
      </mj-column>
    </mj-section>

    <!-- TEXTO + BOTÃO -->
    <mj-section background-color="#FFFFFF" padding-top="0px" padding-right="32px" padding-bottom="34px" padding-left="32px">
      <mj-column>
        <mj-text font-family="Arial, Helvetica, sans-serif" font-size="16px" line-height="25px" color="#5A6478" padding-top="0px" padding-right="0px" padding-bottom="26px" padding-left="0px">Se ficou dúvida sobre qual escolher ou como servir, responda este e-mail — quem responde conhece cada casa da lista.</mj-text>
        <mj-button href="{{carrinho_url}}" background-color="#111D43" color="#FFFFFF" font-family="Arial, Helvetica, sans-serif" font-size="15px" font-weight="bold" border-radius="3px" inner-padding="17px 24px" width="100%" padding-top="0px" padding-right="0px" padding-bottom="0px" padding-left="0px">Voltar ao carrinho</mj-button>
      </mj-column>
    </mj-section>

    <!-- ↓↓ ARRASTE AQUI O BLOCO "PRODUTOS DO CARRINHO" ↓↓ -->

    <!-- RECEITAS DO BLOG -->
    <mj-section background-color="#F6F9FC" border-top="1px solid #DDE3EC" padding-top="28px" padding-right="32px" padding-bottom="30px" padding-left="32px">
      <mj-column>
        <mj-text font-family="Arial, Helvetica, sans-serif" font-size="11px" line-height="16px" letter-spacing="2.6px" color="#8A93A6" padding-top="0px" padding-right="0px" padding-bottom="14px" padding-left="0px">NO BLOG</mj-text>
        <mj-text font-family="Arial, Helvetica, sans-serif" font-size="15px" line-height="24px" color="#5A6478" padding-top="0px" padding-right="0px" padding-bottom="16px" padding-left="0px">A lata resolve o jantar, mas não precisa resolver sozinha. No blog tem receita testada para cada uma delas.</mj-text>
        <mj-text font-family="Arial, Helvetica, sans-serif" font-size="15px" line-height="30px" color="#111D43" padding-top="0px" padding-right="0px" padding-bottom="0px" padding-left="0px">
          <a href="https://blog.fuiaomar.com.br/sardinhas-ao-forno/" style="color:#111D43;text-decoration:none;border-bottom:1px solid #DDE3EC;">Sardinhas ao forno</a><br>
          <a href="https://blog.fuiaomar.com.br/quiche-de-atum-com-salada/" style="color:#111D43;text-decoration:none;border-bottom:1px solid #DDE3EC;">Quiche de atum com salada</a><br>
          <a href="https://blog.fuiaomar.com.br/torta-fria-de-sardinha/" style="color:#111D43;text-decoration:none;border-bottom:1px solid #DDE3EC;">Torta fria de sardinha</a><br>
          <a href="https://blog.fuiaomar.com.br/calzone-de-brocolis-e-sardinha-lucas/" style="color:#111D43;text-decoration:none;border-bottom:1px solid #DDE3EC;">Calzone de brócolis e sardinha</a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- RODAPÉ -->
    <mj-section background-color="#EEF2F7" padding-top="30px" padding-right="32px" padding-bottom="34px" padding-left="32px">
      <mj-column>
        <mj-text align="center" font-family="Arial, Helvetica, sans-serif" font-size="11px" line-height="17px" letter-spacing="2.6px" color="#111D43" padding-top="0px" padding-right="0px" padding-bottom="16px" padding-left="0px">NAVEGUE POR NOVOS SABORES</mj-text>
        <mj-text align="center" font-family="Arial, Helvetica, sans-serif" font-size="12px" line-height="19px" color="#8A93A6" padding-top="0px" padding-right="0px" padding-bottom="10px" padding-left="0px">Fui Ao Mar Comercio de Produtos Alimenticios, Importacao e Exportacao LTDA<br>CNPJ 35.997.372/0001-19 · Alameda Santos, 1165 — Sala 103<br>Cerqueira César · São Paulo/SP · 01419-002</mj-text>
        <mj-text align="center" font-family="Arial, Helvetica, sans-serif" font-size="12px" line-height="19px" color="#8A93A6" padding-top="0px" padding-right="0px" padding-bottom="10px" padding-left="0px"><a href="mailto:contato@fuiaomar.com.br" style="color:#8A93A6;text-decoration:underline;">contato@fuiaomar.com.br</a> · WhatsApp (11) 98860-2948</mj-text>
        <mj-text align="center" font-family="Arial, Helvetica, sans-serif" font-size="12px" line-height="19px" color="#8A93A6" padding-top="0px" padding-right="0px" padding-bottom="10px" padding-left="0px">Você recebeu este e-mail porque comprou ou se cadastrou na Fui ao Mar.</mj-text>
        <mj-text align="center" font-family="Arial, Helvetica, sans-serif" font-size="12px" line-height="19px" color="#8A93A6" padding-top="0px" padding-right="0px" padding-bottom="0px" padding-left="0px"><a href="{{link_optout}}" style="color:#8A93A6;text-decoration:underline;">Não quero mais receber</a></mj-text>
      </mj-column>
    </mj-section>

  </mj-body>
</mjml>
```

---

## 7. Fluxos — o que o Flash usa por trás

- Front-end **Next.js** (bundler **Turbopack**, chunks em `/_next/static/chunks/*.js`).
- Estado de servidor em **TanStack React Query** (`QueryClient` acessível pela árvore React).
- Backend **Supabase**: o front chama funções Postgres via `supabase.rpc(...)`.
- O desenho do fluxo é **React Flow** (canvas com minimapa). O desenho é derivado dos dados; não há
  "posição" salva por nó.

### Hooks do front (módulo de automações)

`useAutomationFlow`, `useAutomationFlows`, `useAutomationFlowsWithAttribution`, `useCancelDrenagem`,
`useDrainFlow`, `useDuplicateAutomationFlow`, `useGatilhoPagamentoDisponivel`, `useReactivateFlow`,
`useSaveAutomationFlow`, `useToggleFlowActive`.

### RPCs relevantes

| RPC | Parâmetros | Uso |
|---|---|---|
| `buscar_fluxo_completo` | `p_fluxo_id`, `p_empresa_id` | Lê o fluxo + todas as ações. Retorna `{success, fluxo, acoes}` |
| `salvar_fluxo_automacao` | `p_fluxo`, `p_acoes` | Cria/salva o fluxo inteiro de uma vez. Retorna `{success, fluxo, acoes, id_map, primeira_acao_id}` |
| `get_fluxos_com_atribuicao` | `p_empresa_id`, `p_data_inicio`, `p_data_fim`, `p_status_filter` | Lista com métricas |
| `drenar_fluxo` | — | "Drenar" |
| `front_onboarding_instanciar_modelos` | — | Cria os modelos de onboarding na conta |
| `front_gatilho_pagamento_disponivel` | — | Verifica gatilho de pagamento |

Tabela: `fluxos_automacao` (lida com `.from("fluxos_automacao").select("*").eq("empresa_id", …)`).

Query keys do React Query: `["automation-flow", <id>]` (fluxo completo), `["automation-flows", <empresa>]`,
`["automation-flows-attribution", <empresa>, "30d"]`, `["creditos", <empresa>]` etc.

### Como o "Duplicar" nativo funciona (é a base do import)

```js
// useDuplicateAutomationFlow — trecho do bundle, desminificado
const { fluxo, acoes } = await supabase.rpc('buscar_fluxo_completo', { p_fluxo_id: id, p_empresa_id: empresa.id });
const p_fluxo = {
  empresa_id: empresa.id, nome: `${fluxo.nome} (Copia)`, descricao: fluxo.descricao,
  trigger_tipo: fluxo.trigger_tipo, trigger_config: fluxo.trigger_config, ativo: false,
  permitir_reentrada: fluxo.permitir_reentrada, intervalo_reentrada_dias: fluxo.intervalo_reentrada_dias,
  respeitar_opt_out: fluxo.respeitar_opt_out, smart_sending_override: fluxo.smart_sending_override
};
const map = new Map(acoes.map(a => [a.id, `temp-${a.id}`]));
const ref = x => x == null ? null : map.get(x) ?? null;
const p_acoes = acoes.map(a => ({
  temp_id: map.get(a.id), ordem: a.ordem, nome: a.nome, tipo_acao: a.tipo_acao, config: a.config,
  proxima_acao: ref(a.proxima_acao), proxima_acao_true: ref(a.proxima_acao_true), proxima_acao_false: ref(a.proxima_acao_false)
}));
await supabase.rpc('salvar_fluxo_automacao', { p_fluxo, p_acoes });
```

E o `useSaveAutomationFlow` (usado pelo editor):

```js
mutationFn: async ({ flow, actions }) => {
  const { data, error } = await supabase.rpc('salvar_fluxo_automacao', {
    p_fluxo: { ...flow, empresa_id: empresa.id },   // empresa da sessão atual
    p_acoes: actions || []
  });
  if (error) throw error;
  if (!data?.success) throw Error(data?.error || 'Erro ao salvar fluxo');
  return data;
}
```

### Modelos de automação

`/automacoes/modelos` (Nova Automação → A partir de modelo): Boas-vindas, Carrinho abandonado,
Aniversário, Pós-compra bounceback, Reativação (Winback), Confirmação de pedido, Confirmação de envio,
Pedido de avaliação. Os dados vêm do servidor (não estão no bundle); fluxos criados de modelo
gravam `modelo_origem_chave`. Não dá para adicionar modelos próprios à galeria.

---

## 8. Fluxos — formato JSON

### Fluxo (`p_fluxo`)

| Campo | Tipo | Observação |
|---|---|---|
| `nome` | string | |
| `descricao` | string/null | |
| `trigger_tipo` | string | ex.: `carrinho_abandonado` |
| `trigger_config` | objeto | filtros do gatilho — ver abaixo |
| `ativo` | bool | **sempre `false` no import** |
| `permitir_reentrada` | bool | |
| `intervalo_reentrada_dias` | int/null | |
| `respeitar_opt_out` | bool | |
| `smart_sending_override` | ?/null | |
| `empresa_id` | int | **preenchido pelo front com a empresa da sessão** — não mandar |

Campos só de leitura que aparecem no `buscar_fluxo_completo`: `id`, `status`, `ativado_em`,
`created_at`, `updated_at`, `arquivado_em`, `total_entradas`, `total_cancelados`, `total_concluidos`,
`total_em_andamento`, `modelo_origem_chave`.

`trigger_config` observado:

```json
{
  "filtro": { "groups": [ { "group_number": 1, "conditions": [
    { "field": "evento.loja", "operator": "in", "valueList": ["262"], "negate": false,
      "days": null, "endDate": null, "startDate": null, "valueMax": null, "valueMin": null,
      "valueText": null, "valueUuid": null, "group_number": 1, "timeOperator": null } ] } ] },
  "direcao": null, "subtipo": null, "status_to": "", "offset_dias": null, "segmento_to": null,
  "status_from": null, "segmento_from": null, "aniversario_dias": null, "aniversario_mode": null,
  "status_entrega_to": null
}
```

### Ações (`p_acoes`)

| Campo | Observação |
|---|---|
| `temp_id` | string qualquer, única no fluxo (o Flash usa `temp-<id>`, os favoritos usam `t<id>`) |
| `ordem` | inteiro |
| `nome` | rótulo do nó |
| `tipo_acao` | ver tabela |
| `config` | depende do tipo |
| `proxima_acao` | `temp_id` da próxima (null = fim) |
| `proxima_acao_true` / `proxima_acao_false` | só em `condition`: ramo Sim / Não |

| `tipo_acao` | `config` observado |
|---|---|
| `delay` | `{ "unidade": "minutos" \| "horas" \| "dias", "quantidade": 30 }` |
| `condition` | `{ "field": null, "value": "", "operator": "=", "condicao_v2": { "logic": "AND", "groups": [ { "logic": "AND", "conditions": [ { "field": "frequency", "operator": "=", "valueMin": 0, "days": 1, "timeOperator": "in_the_last" } ] } ] } }` |
| `send_email` | `{ "assunto": "…", "pre_header": "…", "template_id": 1998 }` |
| `send_whatsapp` | `{ "meta_template_name": "fam_carrinho_wpp", "meta_template_language": "pt_BR" }` |

Não observados ainda (existem no produto, formato não levantado): SMS, cashback/cupom, tags,
webhook, gatilhos de pedido/aniversário/RFM.

### Formato de pacote usado pelos favoritos (`flashcrm-fluxo-v1`)

```text
{
  "formato": "flashcrm-fluxo-v1",
  "origem": { "empresa_id": 97, "fluxo_id": 938, "exportado_em": "ISO-8601" },
  "fluxo": { "...campos de p_fluxo, sem id/empresa_id/ativo..." },
  "acoes": [ { "...campos de p_acoes..." } ]
}
```

---

## 9. Fluxos — favoritos "Exportar fluxo" e "Importar fluxo"

### Como funcionam

- **Exportar** (rodar com um fluxo salvo aberto em `/automacoes/<id>`): acha o `QueryClient` subindo
  a árvore de fibers do React (`__reactFiber*` → `memoizedProps.client`), lê
  `getQueryData(["automation-flow", id])` — o fluxo que a tela já carregou — e monta o pacote
  trocando ids reais por `temp_id`. Mostra uma caixa com **Copiar** / **Baixar .json**. Só leitura.
- **Importar** (rodar em `/automacoes/em-branco`): acha, nos hooks dos fibers, o `MutationObserver`
  cujo `mutationFn` contém `"Erro ao salvar fluxo"` (= `useSaveAutomationFlow`) e chama
  `observer.mutate({ flow, actions })`. Ou seja, salva **pela mesma função do editor**, com a empresa
  da sessão. Força `ativo:false`, acrescenta " (importado)" ao nome e remove `id`/`empresa_id`.
  Se o pacote veio de outra empresa (compara `origem.empresa_id` com a empresa atual, lida da query
  key `["creditos", N]`), **remove `template_id`** dos e-mails e lista o que revisar.
- Primeira abordagem tentada (ler o token do Supabase do `localStorage` e chamar a REST direto) foi
  **descartada por segurança** — os favoritos não tocam em credenciais.

### Exportar — código legível

```js
// Favorito "Exportar fluxo" — rode com um fluxo SALVO aberto (/automacoes/NUMERO).
// Lê o fluxo que o próprio Flash já carregou na tela e copia um JSON portátil.
// Não grava nada.
(async () => {
  const id = +location.pathname.split('/').pop();
  let qc;
  for (const el of document.querySelectorAll('*')) {
    const k = Object.keys(el).find(k => k.startsWith('__reactFiber'));
    if (!k) continue;
    let f = el[k];
    while (f && !qc) {
      const p = f.memoizedProps;
      if (p && p.client && p.client.getQueryCache) qc = p.client;
      f = f.return;
    }
    if (qc) break;
  }
  const d = qc && id && qc.getQueryData(['automation-flow', id]);
  if (!d) { alert('Abra um fluxo salvo (Automações → Editar) e espere o desenho carregar.'); return; }
  const ids = new Map(d.acoes.map(a => [a.id, 't' + a.id]));
  const ref = x => (x == null ? null : ids.get(x) ?? null);
  const pkg = {
    formato: 'flashcrm-fluxo-v1',
    origem: { empresa_id: d.empresa_id, fluxo_id: d.id, exportado_em: new Date().toISOString() },
    fluxo: {
      nome: d.nome,
      descricao: d.descricao,
      trigger_tipo: d.trigger_tipo,
      trigger_config: d.trigger_config,
      permitir_reentrada: d.permitir_reentrada,
      intervalo_reentrada_dias: d.intervalo_reentrada_dias,
      respeitar_opt_out: d.respeitar_opt_out,
      smart_sending_override: d.smart_sending_override
    },
    acoes: d.acoes.map(a => ({
      temp_id: ids.get(a.id),
      ordem: a.ordem,
      nome: a.nome,
      tipo_acao: a.tipo_acao,
      config: a.config,
      proxima_acao: ref(a.proxima_acao),
      proxima_acao_true: ref(a.proxima_acao_true),
      proxima_acao_false: ref(a.proxima_acao_false)
    }))
  };
  const s = JSON.stringify(pkg, null, 2);
  window.__fluxoExportado = s;

  const box = document.createElement('div');
  box.style.cssText = 'position:fixed;inset:0;z-index:2147483647;background:rgba(10,10,20,.55);display:flex;align-items:center;justify-content:center;font-family:system-ui,sans-serif';
  box.innerHTML = '<div style="background:#fff;border-radius:12px;padding:20px;width:min(720px,92vw);box-shadow:0 20px 60px rgba(0,0,0,.3)">' +
    '<div style="font-size:17px;font-weight:700;margin-bottom:6px">Exportar fluxo</div>' +
    '<div id="fc-exp-info" style="font-size:13px;color:#555;margin-bottom:10px"></div>' +
    '<textarea id="fc-exp-txt" readonly style="width:100%;height:320px;font:12px ui-monospace,Menlo,monospace;border:1px solid #ccc;border-radius:8px;padding:10px;box-sizing:border-box"></textarea>' +
    '<div style="display:flex;gap:8px;justify-content:flex-end;margin-top:12px">' +
    '<button id="fc-exp-close" style="padding:9px 16px;border:1px solid #ccc;border-radius:8px;background:#fff;cursor:pointer">Fechar</button>' +
    '<button id="fc-exp-dl" style="padding:9px 16px;border:1px solid #ccc;border-radius:8px;background:#fff;cursor:pointer">Baixar .json</button>' +
    '<button id="fc-exp-copy" style="padding:9px 16px;border:0;border-radius:8px;background:#d4f26a;font-weight:700;cursor:pointer">Copiar</button>' +
    '</div></div>';
  document.body.appendChild(box);
  const $ = id => box.querySelector('#' + id);
  $('fc-exp-info').textContent = '"' + d.nome + '" — ' + pkg.acoes.length + ' etapas. Copie ou baixe, e use no "Importar fluxo".';
  $('fc-exp-txt').value = s;
  $('fc-exp-close').onclick = () => box.remove();
  $('fc-exp-copy').onclick = async () => {
    const t = $('fc-exp-txt');
    t.select();
    try { await navigator.clipboard.writeText(s); } catch (e) { document.execCommand('copy'); }
    $('fc-exp-copy').textContent = 'Copiado';
  };
  $('fc-exp-dl').onclick = () => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([s], { type: 'application/json' }));
    a.download = d.nome.replace(/[^\w\- ]+/g, '').trim().replace(/\s+/g, '-') + '.json';
    a.click();
  };
})();
```

### Exportar — pronto para colar na URL do favorito

```
javascript:(async()%3D%3E%7Bconst%20e%3D%2Blocation.pathname.split(%22%2F%22).pop()%3Blet%20o%3Bfor(const%20e%20of%20document.querySelectorAll(%22*%22))%7Bconst%20t%3DObject.keys(e).find((e%3D%3Ee.startsWith(%22__reactFiber%22)))%3Bif(!t)continue%3Blet%20r%3De%5Bt%5D%3Bfor(%3Br%26%26!o%3B)%7Bconst%20e%3Dr.memoizedProps%3Be%26%26e.client%26%26e.client.getQueryCache%26%26(o%3De.client)%2Cr%3Dr.return%7Dif(o)break%7Dconst%20t%3Do%26%26e%26%26o.getQueryData(%5B%22automation-flow%22%2Ce%5D)%3Bif(!t)return%20void%20alert(%22Abra%20um%20fluxo%20salvo%20(Automa%5Cxe7%5Cxf5es%20%5Cu2192%20Editar)%20e%20espere%20o%20desenho%20carregar.%22)%3Bconst%20r%3Dnew%20Map(t.acoes.map((e%3D%3E%5Be.id%2C%22t%22%2Be.id%5D)))%2Ci%3De%3D%3Enull%3D%3De%3Fnull%3Ar.get(e)%3F%3Fnull%2Ca%3D%7Bformato%3A%22flashcrm-fluxo-v1%22%2Corigem%3A%7Bempresa_id%3At.empresa_id%2Cfluxo_id%3At.id%2Cexportado_em%3A(new%20Date).toISOString()%7D%2Cfluxo%3A%7Bnome%3At.nome%2Cdescricao%3At.descricao%2Ctrigger_tipo%3At.trigger_tipo%2Ctrigger_config%3At.trigger_config%2Cpermitir_reentrada%3At.permitir_reentrada%2Cintervalo_reentrada_dias%3At.intervalo_reentrada_dias%2Crespeitar_opt_out%3At.respeitar_opt_out%2Csmart_sending_override%3At.smart_sending_override%7D%2Cacoes%3At.acoes.map((e%3D%3E(%7Btemp_id%3Ar.get(e.id)%2Cordem%3Ae.ordem%2Cnome%3Ae.nome%2Ctipo_acao%3Ae.tipo_acao%2Cconfig%3Ae.config%2Cproxima_acao%3Ai(e.proxima_acao)%2Cproxima_acao_true%3Ai(e.proxima_acao_true)%2Cproxima_acao_false%3Ai(e.proxima_acao_false)%7D)))%7D%2Cn%3DJSON.stringify(a%2Cnull%2C2)%3Bwindow.__fluxoExportado%3Dn%3Bconst%20c%3Ddocument.createElement(%22div%22)%3Bc.style.cssText%3D%22position%3Afixed%3Binset%3A0%3Bz-index%3A2147483647%3Bbackground%3Argba(10%2C10%2C20%2C.55)%3Bdisplay%3Aflex%3Balign-items%3Acenter%3Bjustify-content%3Acenter%3Bfont-family%3Asystem-ui%2Csans-serif%22%2Cc.innerHTML%3D'%3Cdiv%20style%3D%22background%3A%23fff%3Bborder-radius%3A12px%3Bpadding%3A20px%3Bwidth%3Amin(720px%2C92vw)%3Bbox-shadow%3A0%2020px%2060px%20rgba(0%2C0%2C0%2C.3)%22%3E%3Cdiv%20style%3D%22font-size%3A17px%3Bfont-weight%3A700%3Bmargin-bottom%3A6px%22%3EExportar%20fluxo%3C%2Fdiv%3E%3Cdiv%20id%3D%22fc-exp-info%22%20style%3D%22font-size%3A13px%3Bcolor%3A%23555%3Bmargin-bottom%3A10px%22%3E%3C%2Fdiv%3E%3Ctextarea%20id%3D%22fc-exp-txt%22%20readonly%20style%3D%22width%3A100%25%3Bheight%3A320px%3Bfont%3A12px%20ui-monospace%2CMenlo%2Cmonospace%3Bborder%3A1px%20solid%20%23ccc%3Bborder-radius%3A8px%3Bpadding%3A10px%3Bbox-sizing%3Aborder-box%22%3E%3C%2Ftextarea%3E%3Cdiv%20style%3D%22display%3Aflex%3Bgap%3A8px%3Bjustify-content%3Aflex-end%3Bmargin-top%3A12px%22%3E%3Cbutton%20id%3D%22fc-exp-close%22%20style%3D%22padding%3A9px%2016px%3Bborder%3A1px%20solid%20%23ccc%3Bborder-radius%3A8px%3Bbackground%3A%23fff%3Bcursor%3Apointer%22%3EFechar%3C%2Fbutton%3E%3Cbutton%20id%3D%22fc-exp-dl%22%20style%3D%22padding%3A9px%2016px%3Bborder%3A1px%20solid%20%23ccc%3Bborder-radius%3A8px%3Bbackground%3A%23fff%3Bcursor%3Apointer%22%3EBaixar%20.json%3C%2Fbutton%3E%3Cbutton%20id%3D%22fc-exp-copy%22%20style%3D%22padding%3A9px%2016px%3Bborder%3A0%3Bborder-radius%3A8px%3Bbackground%3A%23d4f26a%3Bfont-weight%3A700%3Bcursor%3Apointer%22%3ECopiar%3C%2Fbutton%3E%3C%2Fdiv%3E%3C%2Fdiv%3E'%2Cdocument.body.appendChild(c)%3Bconst%20d%3De%3D%3Ec.querySelector(%22%23%22%2Be)%3Bd(%22fc-exp-info%22).textContent%3D'%22'%2Bt.nome%2B'%22%20%5Cu2014%20'%2Ba.acoes.length%2B'%20etapas.%20Copie%20ou%20baixe%2C%20e%20use%20no%20%22Importar%20fluxo%22.'%2Cd(%22fc-exp-txt%22).value%3Dn%2Cd(%22fc-exp-close%22).onclick%3D()%3D%3Ec.remove()%2Cd(%22fc-exp-copy%22).onclick%3Dasync()%3D%3E%7Bd(%22fc-exp-txt%22).select()%3Btry%7Bawait%20navigator.clipboard.writeText(n)%7Dcatch(e)%7Bdocument.execCommand(%22copy%22)%7Dd(%22fc-exp-copy%22).textContent%3D%22Copiado%22%7D%2Cd(%22fc-exp-dl%22).onclick%3D()%3D%3E%7Bconst%20e%3Ddocument.createElement(%22a%22)%3Be.href%3DURL.createObjectURL(new%20Blob(%5Bn%5D%2C%7Btype%3A%22application%2Fjson%22%7D))%2Ce.download%3Dt.nome.replace(%2F%5B%5E%5Cw%5C-%20%5D%2B%2Fg%2C%22%22).trim().replace(%2F%5Cs%2B%2Fg%2C%22-%22)%2B%22.json%22%2Ce.click()%7D%7D)()%3B
```

### Importar — código legível

```js
// Favorito "Importar fluxo" — rode em Automações → Nova Automação → Em branco.
// Abre uma caixa para colar o JSON exportado e salva usando a mesma função
// de salvar do editor do Flash. O fluxo sempre nasce DESLIGADO.
(() => {
  const fibers = function* () {
    for (const el of document.querySelectorAll('*')) {
      const k = Object.keys(el).find(k => k.startsWith('__reactFiber'));
      if (k) yield el[k];
    }
  };
  let obs, qc;
  for (let f of fibers()) {
    while (f && !(obs && qc)) {
      const p = f.memoizedProps;
      if (!qc && p && p.client && p.client.getQueryCache) qc = p.client;
      let h = f.memoizedState, g = 0;
      while (!obs && h && g++ < 80) {
        const c = h.memoizedState;
        if (c && c.options && typeof c.options.mutationFn === 'function' &&
            c.options.mutationFn.toString().includes('Erro ao salvar fluxo')) obs = c;
        h = h.next;
      }
      f = f.return;
    }
    if (obs && qc) break;
  }
  if (!obs) { alert('Abra Automações → Nova Automação → Em branco e clique no favorito de novo.'); return; }

  // empresa aberta agora (para saber se o JSON veio de outra conta)
  let empresaAtual = null;
  if (qc) for (const q of qc.getQueryCache().getAll()) {
    const k = q.queryKey;
    if (k[0] === 'creditos' && typeof k[1] === 'number') { empresaAtual = k[1]; break; }
  }

  const box = document.createElement('div');
  box.style.cssText = 'position:fixed;inset:0;z-index:2147483647;background:rgba(10,10,20,.55);display:flex;align-items:center;justify-content:center;font-family:system-ui,sans-serif';
  box.innerHTML = '<div style="background:#fff;border-radius:12px;padding:20px;width:min(720px,92vw);box-shadow:0 20px 60px rgba(0,0,0,.3)">' +
    '<div style="font-size:17px;font-weight:700;margin-bottom:6px">Importar fluxo</div>' +
    '<div style="font-size:13px;color:#555;margin-bottom:10px">Cole o JSON exportado. O fluxo será criado <b>desligado</b>.</div>' +
    '<textarea id="fc-imp-txt" style="width:100%;height:320px;font:12px ui-monospace,Menlo,monospace;border:1px solid #ccc;border-radius:8px;padding:10px;box-sizing:border-box"></textarea>' +
    '<div id="fc-imp-msg" style="font-size:13px;margin:10px 0;white-space:pre-wrap"></div>' +
    '<div style="display:flex;gap:8px;justify-content:flex-end">' +
    '<button id="fc-imp-cancel" style="padding:9px 16px;border:1px solid #ccc;border-radius:8px;background:#fff;cursor:pointer">Cancelar</button>' +
    '<button id="fc-imp-ok" style="padding:9px 16px;border:0;border-radius:8px;background:#d4f26a;font-weight:700;cursor:pointer">Importar</button>' +
    '</div></div>';
  document.body.appendChild(box);
  const $ = id => box.querySelector('#' + id);
  const msg = (t, cor) => { $('fc-imp-msg').style.color = cor || '#333'; $('fc-imp-msg').textContent = t; };
  $('fc-imp-cancel').onclick = () => box.remove();
  $('fc-imp-txt').focus();

  $('fc-imp-ok').onclick = async () => {
    let p;
    try { p = JSON.parse($('fc-imp-txt').value); } catch (e) { msg('JSON inválido: ' + e.message, '#b00020'); return; }
    if (!p || !p.fluxo || !Array.isArray(p.acoes) || !p.fluxo.trigger_tipo) {
      msg('Formato inesperado: o JSON precisa ter "fluxo" (com trigger_tipo) e "acoes".', '#b00020'); return;
    }
    const outraConta = p.origem && empresaAtual != null && p.origem.empresa_id !== empresaAtual;
    const revisar = [];
    const acoes = p.acoes.map(a => {
      const config = { ...(a.config || {}) };
      if ('template_id' in config && outraConta) {
        delete config.template_id;
        revisar.push('• "' + a.nome + '": escolher o template (veio de outra conta)');
      }
      if (config.meta_template_name) revisar.push('• "' + a.nome + '": conferir se o WhatsApp "' + config.meta_template_name + '" existe e está aprovado aqui');
      return { ...a, config };
    });
    const filtroTxt = JSON.stringify(p.fluxo.trigger_config || {});
    if (outraConta && /evento\.loja|valueUuid":"|segmento/.test(filtroTxt)) revisar.push('• Gatilho: conferir filtro de loja/segmento (IDs são da conta de origem)');

    const flow = { ...p.fluxo, ativo: false, nome: (p.fluxo.nome || 'Fluxo') + ' (importado)' };
    delete flow.id; delete flow.empresa_id;

    $('fc-imp-ok').disabled = true;
    msg('Salvando…');
    try {
      const r = await obs.mutate({ flow, actions: acoes });
      const novoId = r && (r.fluxo_id || r.id || (r.fluxo && r.fluxo.id));
      msg('Fluxo criado DESLIGADO: "' + flow.nome + '" (' + acoes.length + ' etapas).' +
        (revisar.length ? '\n\nRevise antes de ligar:\n' + revisar.join('\n') : ''), '#0a7a3d');
      $('fc-imp-ok').textContent = 'Abrir fluxo';
      $('fc-imp-ok').disabled = false;
      $('fc-imp-ok').onclick = () => { location.href = novoId ? '/automacoes/' + novoId : '/automacoes'; };
      window.__fluxoImportado = r;
    } catch (e) {
      $('fc-imp-ok').disabled = false;
      msg('O Flash recusou: ' + (e && e.message ? e.message : e), '#b00020');
    }
  };
})();
```

### Importar — pronto para colar na URL do favorito

```
javascript:(()%3D%3E%7Blet%20e%2Co%3Bfor(let%20t%20of%20function*()%7Bfor(const%20e%20of%20document.querySelectorAll(%22*%22))%7Bconst%20o%3DObject.keys(e).find((e%3D%3Ee.startsWith(%22__reactFiber%22)))%3Bo%26%26(yield%20e%5Bo%5D)%7D%7D())%7Bfor(%3Bt%26%26(!e%7C%7C!o)%3B)%7Bconst%20i%3Dt.memoizedProps%3B!o%26%26i%26%26i.client%26%26i.client.getQueryCache%26%26(o%3Di.client)%3Blet%20n%3Dt.memoizedState%2Cr%3D0%3Bfor(%3B!e%26%26n%26%26r%2B%2B%3C80%3B)%7Bconst%20o%3Dn.memoizedState%3Bo%26%26o.options%26%26%22function%22%3D%3Dtypeof%20o.options.mutationFn%26%26o.options.mutationFn.toString().includes(%22Erro%20ao%20salvar%20fluxo%22)%26%26(e%3Do)%2Cn%3Dn.next%7Dt%3Dt.return%7Dif(e%26%26o)break%7Dif(!e)return%20void%20alert(%22Abra%20Automa%5Cxe7%5Cxf5es%20%5Cu2192%20Nova%20Automa%5Cxe7%5Cxe3o%20%5Cu2192%20Em%20branco%20e%20clique%20no%20favorito%20de%20novo.%22)%3Blet%20t%3Dnull%3Bif(o)for(const%20e%20of%20o.getQueryCache().getAll())%7Bconst%20o%3De.queryKey%3Bif(%22creditos%22%3D%3D%3Do%5B0%5D%26%26%22number%22%3D%3Dtypeof%20o%5B1%5D)%7Bt%3Do%5B1%5D%3Bbreak%7D%7Dconst%20i%3Ddocument.createElement(%22div%22)%3Bi.style.cssText%3D%22position%3Afixed%3Binset%3A0%3Bz-index%3A2147483647%3Bbackground%3Argba(10%2C10%2C20%2C.55)%3Bdisplay%3Aflex%3Balign-items%3Acenter%3Bjustify-content%3Acenter%3Bfont-family%3Asystem-ui%2Csans-serif%22%2Ci.innerHTML%3D'%3Cdiv%20style%3D%22background%3A%23fff%3Bborder-radius%3A12px%3Bpadding%3A20px%3Bwidth%3Amin(720px%2C92vw)%3Bbox-shadow%3A0%2020px%2060px%20rgba(0%2C0%2C0%2C.3)%22%3E%3Cdiv%20style%3D%22font-size%3A17px%3Bfont-weight%3A700%3Bmargin-bottom%3A6px%22%3EImportar%20fluxo%3C%2Fdiv%3E%3Cdiv%20style%3D%22font-size%3A13px%3Bcolor%3A%23555%3Bmargin-bottom%3A10px%22%3ECole%20o%20JSON%20exportado.%20O%20fluxo%20ser%5Cxe1%20criado%20%3Cb%3Edesligado%3C%2Fb%3E.%3C%2Fdiv%3E%3Ctextarea%20id%3D%22fc-imp-txt%22%20style%3D%22width%3A100%25%3Bheight%3A320px%3Bfont%3A12px%20ui-monospace%2CMenlo%2Cmonospace%3Bborder%3A1px%20solid%20%23ccc%3Bborder-radius%3A8px%3Bpadding%3A10px%3Bbox-sizing%3Aborder-box%22%3E%3C%2Ftextarea%3E%3Cdiv%20id%3D%22fc-imp-msg%22%20style%3D%22font-size%3A13px%3Bmargin%3A10px%200%3Bwhite-space%3Apre-wrap%22%3E%3C%2Fdiv%3E%3Cdiv%20style%3D%22display%3Aflex%3Bgap%3A8px%3Bjustify-content%3Aflex-end%22%3E%3Cbutton%20id%3D%22fc-imp-cancel%22%20style%3D%22padding%3A9px%2016px%3Bborder%3A1px%20solid%20%23ccc%3Bborder-radius%3A8px%3Bbackground%3A%23fff%3Bcursor%3Apointer%22%3ECancelar%3C%2Fbutton%3E%3Cbutton%20id%3D%22fc-imp-ok%22%20style%3D%22padding%3A9px%2016px%3Bborder%3A0%3Bborder-radius%3A8px%3Bbackground%3A%23d4f26a%3Bfont-weight%3A700%3Bcursor%3Apointer%22%3EImportar%3C%2Fbutton%3E%3C%2Fdiv%3E%3C%2Fdiv%3E'%2Cdocument.body.appendChild(i)%3Bconst%20n%3De%3D%3Ei.querySelector(%22%23%22%2Be)%2Cr%3D(e%2Co)%3D%3E%7Bn(%22fc-imp-msg%22).style.color%3Do%7C%7C%22%23333%22%2Cn(%22fc-imp-msg%22).textContent%3De%7D%3Bn(%22fc-imp-cancel%22).onclick%3D()%3D%3Ei.remove()%2Cn(%22fc-imp-txt%22).focus()%2Cn(%22fc-imp-ok%22).onclick%3Dasync()%3D%3E%7Blet%20o%3Btry%7Bo%3DJSON.parse(n(%22fc-imp-txt%22).value)%7Dcatch(e)%7Breturn%20void%20r(%22JSON%20inv%5Cxe1lido%3A%20%22%2Be.message%2C%22%23b00020%22)%7Dif(!(o%26%26o.fluxo%26%26Array.isArray(o.acoes)%26%26o.fluxo.trigger_tipo))return%20void%20r('Formato%20inesperado%3A%20o%20JSON%20precisa%20ter%20%22fluxo%22%20(com%20trigger_tipo)%20e%20%22acoes%22.'%2C%22%23b00020%22)%3Bconst%20i%3Do.origem%26%26null!%3Dt%26%26o.origem.empresa_id!%3D%3Dt%2Ca%3D%5B%5D%2Cs%3Do.acoes.map((e%3D%3E%7Bconst%20o%3D%7B...e.config%7C%7C%7B%7D%7D%3Breturn%22template_id%22in%20o%26%26i%26%26(delete%20o.template_id%2Ca.push('%5Cu2022%20%22'%2Be.nome%2B'%22%3A%20escolher%20o%20template%20(veio%20de%20outra%20conta)'))%2Co.meta_template_name%26%26a.push('%5Cu2022%20%22'%2Be.nome%2B'%22%3A%20conferir%20se%20o%20WhatsApp%20%22'%2Bo.meta_template_name%2B'%22%20existe%20e%20est%5Cxe1%20aprovado%20aqui')%2C%7B...e%2Cconfig%3Ao%7D%7D))%2Cc%3DJSON.stringify(o.fluxo.trigger_config%7C%7C%7B%7D)%3Bi%26%26%2Fevento%5C.loja%7CvalueUuid%22%3A%22%7Csegmento%2F.test(c)%26%26a.push(%22%5Cu2022%20Gatilho%3A%20conferir%20filtro%20de%20loja%2Fsegmento%20(IDs%20s%5Cxe3o%20da%20conta%20de%20origem)%22)%3Bconst%20d%3D%7B...o.fluxo%2Cativo%3A!1%2Cnome%3A(o.fluxo.nome%7C%7C%22Fluxo%22)%2B%22%20(importado)%22%7D%3Bdelete%20d.id%2Cdelete%20d.empresa_id%2Cn(%22fc-imp-ok%22).disabled%3D!0%2Cr(%22Salvando%5Cu2026%22)%3Btry%7Bconst%20o%3Dawait%20e.mutate(%7Bflow%3Ad%2Cactions%3As%7D)%2Ct%3Do%26%26(o.fluxo_id%7C%7Co.id%7C%7Co.fluxo%26%26o.fluxo.id)%3Br('Fluxo%20criado%20DESLIGADO%3A%20%22'%2Bd.nome%2B'%22%20('%2Bs.length%2B%22%20etapas).%22%2B(a.length%3F%22%5Cn%5CnRevise%20antes%20de%20ligar%3A%5Cn%22%2Ba.join(%22%5Cn%22)%3A%22%22)%2C%22%230a7a3d%22)%2Cn(%22fc-imp-ok%22).textContent%3D%22Abrir%20fluxo%22%2Cn(%22fc-imp-ok%22).disabled%3D!1%2Cn(%22fc-imp-ok%22).onclick%3D()%3D%3E%7Blocation.href%3Dt%3F%22%2Fautomacoes%2F%22%2Bt%3A%22%2Fautomacoes%22%7D%2Cwindow.__fluxoImportado%3Do%7Dcatch(e)%7Bn(%22fc-imp-ok%22).disabled%3D!1%2Cr(%22O%20Flash%20recusou%3A%20%22%2B(e%26%26e.message%3Fe.message%3Ae)%2C%22%23b00020%22)%7D%7D%7D)()%3B
```

### Uso

**Exportar:** conta de origem → Automações → ⋯ → **Editar** → esperar o desenho → favorito
**Exportar fluxo** → Copiar ou Baixar .json.

**Importar:** conta de destino → Automações → **Nova Automação → Em branco** → favorito **Importar
fluxo** → colar → **Importar** → ler a lista de revisão → **Abrir fluxo**. Nasce **Inativo**.

### O que religar depois do import

| Item | Mesma conta | Outra conta |
|---|---|---|
| `template_id` (e-mail) | mantido | **removido** — escolher no editor |
| `meta_template_name` (WhatsApp) | mantido | mantido pelo nome — precisa existir/aprovado na WABA da conta |
| `evento.loja` no gatilho | ok | **trocar** — id de loja é da conta de origem |
| segmentos/listas (`valueUuid`, `segmento_*`) | ok | **trocar** |
| `respeitar_opt_out` | copiado | copiado — conferir |

Depois: Salvar → recarregar → conferir → só então ativar.

---

## 10. Fluxos — exemplo real completo

`SF - AUT-01 - Carrinho Abandonado` da Fui ao Mar (fluxo 938), exportado pelo favorito:

```json
{
  "formato": "flashcrm-fluxo-v1",
  "origem": { "empresa_id": 97, "fluxo_id": 938, "exportado_em": "2026-10-14T21:44:00.374Z" },
  "fluxo": {
    "nome": "SF - AUT-01 - Carrinho Abandonado",
    "descricao": null,
    "trigger_tipo": "carrinho_abandonado",
    "trigger_config": {
      "filtro": {
        "groups": [
          {
            "conditions": [
              { "days": null, "field": "evento.loja", "negate": false, "endDate": null, "operator": "in", "valueMax": null, "valueMin": null, "startDate": null, "valueList": ["262"], "valueText": null, "valueUuid": null, "group_number": 1, "timeOperator": null }
            ],
            "group_number": 1
          }
        ]
      },
      "direcao": null, "subtipo": null, "status_to": "", "offset_dias": null, "segmento_to": null, "status_from": null, "segmento_from": null, "aniversario_dias": null, "aniversario_mode": null, "status_entrega_to": null
    },
    "permitir_reentrada": false,
    "intervalo_reentrada_dias": null,
    "respeitar_opt_out": false,
    "smart_sending_override": null
  },
  "acoes": [
    { "temp_id": "t5600", "ordem": 1, "nome": "Espera 30 minutos", "tipo_acao": "delay", "config": { "unidade": "minutos", "quantidade": 30 }, "proxima_acao": "t5601", "proxima_acao_true": null, "proxima_acao_false": null },
    { "temp_id": "t5601", "ordem": 2, "nome": "Sem pedido no último dia?", "tipo_acao": "condition", "config": { "field": null, "value": "", "operator": "=", "condicao_v2": { "logic": "AND", "groups": [ { "logic": "AND", "conditions": [ { "days": 1, "field": "frequency", "operator": "=", "valueMin": 0, "timeOperator": "in_the_last" } ] } ] } }, "proxima_acao": null, "proxima_acao_true": "t5602", "proxima_acao_false": "t5603" },
    { "temp_id": "t5602", "ordem": 3, "nome": "Carrinho Email 1", "tipo_acao": "send_email", "config": { "assunto": "Ficou algo no seu carrinho", "pre_header": "As latas que você separou continuam disponíveis.", "template_id": 1998 }, "proxima_acao": "t5604", "proxima_acao_true": null, "proxima_acao_false": null },
    { "temp_id": "t5603", "ordem": 4, "nome": "Fluxo encerrado (cliente comprou)", "tipo_acao": "delay", "config": { "unidade": "minutos", "quantidade": 1 }, "proxima_acao": null, "proxima_acao_true": null, "proxima_acao_false": null },
    { "temp_id": "t5604", "ordem": 5, "nome": "Carrinho WhatsApp", "tipo_acao": "send_whatsapp", "config": { "meta_template_name": "fam_carrinho_wpp", "meta_template_language": "pt_BR" }, "proxima_acao": "t5605", "proxima_acao_true": null, "proxima_acao_false": null },
    { "temp_id": "t5605", "ordem": 6, "nome": "Espera 20 horas", "tipo_acao": "delay", "config": { "unidade": "horas", "quantidade": 20 }, "proxima_acao": "t5606", "proxima_acao_true": null, "proxima_acao_false": null },
    { "temp_id": "t5606", "ordem": 7, "nome": "Ainda sem pedido?", "tipo_acao": "condition", "config": { "field": null, "value": "", "operator": "=", "condicao_v2": { "logic": "AND", "groups": [ { "logic": "AND", "conditions": [ { "days": 1, "field": "frequency", "operator": "=", "valueMin": 0, "timeOperator": "in_the_last" } ] } ] } }, "proxima_acao": null, "proxima_acao_true": "t5608", "proxima_acao_false": "t5607" },
    { "temp_id": "t5607", "ordem": 8, "nome": "Fluxo encerrado (comprou após 20h)", "tipo_acao": "delay", "config": { "unidade": "minutos", "quantidade": 1 }, "proxima_acao": null, "proxima_acao_true": null, "proxima_acao_false": null },
    { "temp_id": "t5608", "ordem": 9, "nome": "Carrinho Email 2", "tipo_acao": "send_email", "config": { "assunto": "Ainda dá tempo", "pre_header": "Que tal finalizar seu pedido? Seus produtos favoritos estão esperando por você! 🐟", "template_id": 1999 }, "proxima_acao": null, "proxima_acao_true": null, "proxima_acao_false": null }
  ]
}
```

Lido como desenho: Gatilho carrinho abandonado (loja 262) → Espera 30 min → **Sem pedido no último
dia?** → Sim: E-mail 1 → WhatsApp → Espera 20 h → **Ainda sem pedido?** → Sim: E-mail 2 / Não: fim ·
Não (do primeiro): fim. Os "fins" são `delay` de 1 minuto sem próxima ação (padrão usado para dar nome
ao encerramento).

---

## 11. Testes, lacunas e riscos

### Testado (14/10/2026, conta Fui ao Mar)

| Teste | Resultado |
|---|---|
| Importar MJML em template novo | ✅ blocos nativos, 0 erros, HTML 25 KB. **Não salvo.** |
| Exportar fluxo 938 | ✅ pacote de 5.280 caracteres, 9 ações, ramos corretos |
| Importar MJML, salvar e reabrir (16/10/2026, conta Repeat) | ✅ template 4140: voltou com as 12 `mj-section`, variáveis, `fc-if--`/`fc-ifnot--` e paddings por lado; o Flash acrescenta um `mj-head` (`mj-font` + `mj-attributes`) de branding |
| Criar fluxo novo pela mutação de salvar (16/10/2026, conta Repeat) | ✅ fluxo 2055 em `/automacoes/em-branco`, 4 ações (delay → condition → send_email com `pre_header` → delay), inativo, abre certo no editor |
| Importar o pacote na mesma conta | ✅ criou fluxo **2002** "TESTE IMPORT - apagar (importado)", **Inativo**, 9 ações, ramos Sim/Não, templates e assuntos idênticos (`id_map` `t5600…t5608 → 12210…12218`). **Esse fluxo de teste continua na conta — apagar/arquivar.** |

### Não testado

- Salvar um template importado e reabrir (persistência).
- Import de MJML contendo bloco dinâmico (recomendação: arrastar depois).
- Se `fc-if--`/`fc-ifnot--` é aplicado no envio real (inferido pelo uso nos blocos do próprio Flash).
- **Import de fluxo entre contas diferentes.** A lógica de limpeza está pronta, mas não rodou.
- Fluxos com SMS, cashback, cupom, tags, gatilhos de pedido/aniversário/RFM.
- Cópia para a área de transferência pelo favorito com clique real (no teste automatizado o navegador
  bloqueou por falta de gesto do usuário; por isso existe o botão Copiar + `execCommand` + Baixar .json).

### Riscos

- **Não oficial.** Depende de: `__gjsv` no canvas, comando `mjml-import`, `__reactFiber*`, query key
  `["automation-flow", id]`, texto `"Erro ao salvar fluxo"` dentro do `mutationFn`, query key
  `["creditos", N]`. Qualquer refactor do Flash pode quebrar. Sintoma: o favorito mostra o alerta de
  "abra a tela certa" mesmo na tela certa.
- **Referências cruzadas entre empresas.** Se um `template_id` de outra empresa for enviado ao
  `salvar_fluxo_automacao`, não sabemos se o backend valida a posse. Por isso o import remove
  `template_id` quando detecta outra empresa. Vale o dev do Flash confirmar a validação no RPC.
- **Fluxo importado nasce desligado**, mas qualquer um pode ligar sem revisar. Regra interna: só ligar
  depois da revisão de copy.

---

## 12. Observações encontradas na conta durante a investigação

1. Os fluxos **SF - AUT-01 (Carrinho)** e **SF - AUT-04 (Winback)** estão **Ativos**, com 22 e 101
   entradas, e marcados "Pausada — template indisponível" (WhatsApp `fam_carrinho_wpp` indisponível).
   Conferir quem ligou e se os e-mails anteriores ao WhatsApp chegaram a sair.
2. O fluxo de carrinho está com **`respeitar_opt_out: false`** — quem pediu descadastro pode continuar
   recebendo. Recomendado ligar.
3. O canvas do editor de e-mail zera o padding das seções (visual apenas; o HTML enviado está certo).

---

## 13. O que seria ideal o Flash oferecer oficialmente

- Botão **Importar MJML** / **Exportar MJML** no editor de e-mail (o comando já existe).
- **Exportar / Importar fluxo** em JSON no menu ⋯ do fluxo, com mapeamento de templates, lojas e
  segmentos na conta de destino.
- **Biblioteca de modelos por parceiro** (agência cadastra seus fluxos/templates padrão e aplica nas
  contas dos clientes).
- Validação no `salvar_fluxo_automacao` de que `template_id`, segmentos e lojas pertencem à empresa.
- `respeitar_opt_out` ligado por padrão em fluxos de marketing.

---

*Turbo Partners — Documentação FlashCRM · 14/10/2026*
