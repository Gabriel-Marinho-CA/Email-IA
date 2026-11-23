# E-mails marketing no Flash CRM

O Flash CRM dispara os e-mails das automações dos clientes (carrinho abandonado, boas-vindas,
pós-compra, recompra, cashback) e das campanhas. O layout vem do Figma; a gente transforma em
**MJML**, sobe as imagens na Shopify do cliente e importa no Flash. O Claude Code faz a parte braçal
com a skill `email-flash-crm`, anexada nesta página.

**Por que MJML:** o editor de e-mail do Flash é feito em MJML. Importado do jeito certo, cada parte do
e-mail (texto, imagem, botão) vira um bloco normal do editor, que qualquer pessoa edita clicando.
HTML colado no bloco "HTML" vira um bloco só, que só dá para editar mexendo no código.

---

## 1. Criar o template no Flash

Pré-requisito: canal de e-mail da loja configurado e **domínio verificado** (DNS/SPF/DKIM). Sem
isso o Flash não deixa criar template de e-mail.

**Uma vez por navegador: criar o favorito "Importar MJML".** O Flash tem o importador de MJML, mas
sem botão; o favorito abre ele. No Chrome: mostre a barra de favoritos (`Ctrl + Shift + B`), clique
com o botão direito nela → **Adicionar página…** → Nome `Importar MJML` → na URL, cole:

```
javascript:(()=>{for(const f of document.querySelectorAll('iframe')){let d;try{d=f.contentDocument}catch(e){continue}if(!d)continue;const v=[...d.querySelectorAll('*')].find(e=>e.__gjsv);if(v){const em=v.__gjsv.em;const ed=(em.getEditor&&em.getEditor())||em.Editor;ed.runCommand('mjml-import');return}}alert('Abra um template de e-mail no editor do Flash primeiro.')})()
```

Ele não lê senha, cookie nem token: só abre uma janela que o próprio editor do Flash já tem.

**1. No menu lateral, clique em Templates.**

![Menu lateral do Flash CRM com Templates selecionado](../prints-do-flash/passo-1-menu-templates.png)

**2. Clique em "+ Criar Template" e escolha Email.**

![Botão Criar Template com as opções SMS, Email e WhatsApp API](../prints-do-flash/passo-2-criar-template-email.png)

**3. Com o editor aberto, clique no favorito "Importar MJML".** Abre a janela "Import MJML".

**4. Apague o que estiver na janela, cole o arquivo `.mjml` inteiro e clique em Import.** O import
**substitui** o template todo.

**5.** Confira em Desktop / Mobile (o editor esconde o espaçamento das seções; use **Visualizar**),
dê um nome e clique em **Criar Template**. Envie um **teste** (Gmail, Outlook e celular).

**6.** Em **Automações** (ou na campanha), escolha o template no passo **Email**, preencha o
**assunto** e o **pré-header** (eles não vão no arquivo) e confira se o fluxo está **Ativo** (é o erro
mais comum).

E-mail de carrinho/pedido com lista de produtos: depois do import, arraste o bloco nativo
**Produtos do Carrinho** / **Produtos do Pedido** para o lugar dele.

---

## 2. Variáveis

| Grupo (onde funciona) | Variáveis |
|---|---|
| Cliente (qualquer fluxo e campanha) | `{{primeiro_nome}}` `{{nome_cliente}}` (nome completo) `{{sobrenome}}` `{{email}}` `{{telefone}}` |
| Pedido | `{{numero_pedido}}` `{{valor_pedido}}` `{{status_pedido}}` `{{url_rastreio}}` `{{codigo_rastreio}}` `{{transportadora}}` `{{status_entrega}}` |
| Pagamento | `{{pix_copia_cola}}` `{{boleto_url}}` `{{boleto_linha_digitavel}}` `{{url_pagamento}}` |
| Cashback | `{{valor_cashback}}` `{{cupom}}` `{{data_vencimento}}` `{{data_ativacao}}` `{{compra_minima}}` `{{desconto_max}}` |
| Carrinho abandonado | `{{carrinho_url}}` `{{carrinho_produto_nome}}` `{{carrinho_produto_imagem}}` `{{carrinho_total}}` `{{carrinho_frete}}` `{{carrinho_qtd_itens}}` |
| Descadastro (todos) | `{{link_optout}}`: **obrigatório no rodapé** |

- "Olá, Maria": use `{{primeiro_nome}}`. `{{nome_cliente}}` é o nome completo.
- Fora do fluxo certo a variável sai vazia (ex.: `{{carrinho_url}}` num e-mail de cashback).
- **Seção que só aparece se tiver o dado:** no arquivo, a seção leva a classe `fc-if--primeiro_nome`
  (aparece se tem nome) ou `fc-ifnot--primeiro_nome` (aparece se não tem). O editor mostra o rótulo
  "Só quando…". É assim que sai "Oi, Maria!" para quem tem nome e "Oi!" para quem não tem.
- Rodapé: razão social, CNPJ, endereço e o link de descadastro.

---

## 3. O que quebra o template

- **Comentários no arquivo** (`<!-- -->`): com `{{ }}` dentro quebram o build; sem, viram lixo no editor.
- **Webfont.** Só fontes que todo e-mail tem: Helvetica/Arial (Georgia, Verdana etc. também).
- **URLs relativas.** Imagem e link sempre com `https://...` completo.
- **Espaçamento em atalho** (`padding="10px 20px"`): o e-mail sai certo, mas o painel mostra valores
  errados. Escreva cada lado (`padding-top`, `padding-right`...).
- **Importar de novo apaga o que foi editado à mão no Flash** (o import substitui tudo).
- Condicional com `{{#if}}` só testa se está vazio, não compara valor (`{{#if cupom}}` funciona,
  "se cupom = X" não).

---

## 4. Imagens: Files da Shopify do cliente

As imagens de cada marca vão no **Files** (Conteúdo → Arquivos) da loja Shopify **daquela marca**, e
a URL do CDN entra no arquivo do e-mail. Ex.: PEP → `pep-protein.myshopify.com`.

- **Prefixe todo arquivo com marca + template** (`pep-bv-hero.jpg` = PEP boas-vindas). O Files é uma
  pasta só: nome repetido vira `nome_<uuid>.png` e a URL do template quebra.
- **Nunca reenvie com o mesmo nome** para atualizar: suba `-v2` e troque no template.
- Use a URL **sem** o `?v=...` do final.
- Padrão das imagens: exportadas em **2x** (largura cheia = 1200px, exibida em 600px), JPG para foto,
  PNG só com transparência, até ~200 KB cada. O e-mail tem **600px** de largura.
- Foto de produto e logo: se a loja já tem o original em alta, use ele em vez de recortar do print.

A skill sobe as imagens pela Shopify CLI. Uma vez por loja, em cada máquina (precisa de acesso de
colaborador na loja):

```
shopify store auth --store <loja>.myshopify.com --scopes read_files,write_files
```

---

## 5. Usando o Claude

**Instalar a skill** (uma vez por máquina):

1. Baixe o `email-flash-crm.zip` anexado e descompacte em `C:\Users\<você>\.claude\skills\`
   (Mac/Linux: `~/.claude/skills/`). Tem que ficar `.claude\skills\email-flash-crm\SKILL.md`.
2. Instale: Python 3 (`pip install pillow numpy opencv-python requests`), Node.js (para o MJML),
   Google Chrome e Shopify CLI (`npm install -g @shopify/cli`).
3. Opcional, para upscale na GPU: o
   [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-windows.zip)
   descompactado em `email-flash-crm\scripts\bin\esrgan\`.

**Pedir um template:** abra o Claude Code na pasta dos e-mails (uma subpasta por marca) e mande:

```
/email-flash-crm pep "d:/Downloads/recompra-90.png"
Recompra de 90 dias, cupom VOLTAR10 fixo, CTA para /collections/all.
```

Ele mede o PNG, recorta as imagens, monta o `.mjml`, compara com o layout lado a lado (desktop e
mobile) até bater, sobe as imagens na Shopify e anota tudo no README da marca. Diga sempre a
**marca**, o **arquivo do layout**, **qual e-mail é**, o **link dos botões**, o **cupom** e, se for
marca nova, a **razão social e o CNPJ** do rodapé.

Ele entrega o `.mjml` (é esse que vai no "Importar MJML") e um `.html` do mesmo e-mail, só para
visualizar. Antes de publicar, confira a comparação que ele gera e o e-mail de teste do Flash: nenhum
`{{` sobrando, imagens carregando, links certos e o "Não quero mais receber" funcionando no rodapé.
