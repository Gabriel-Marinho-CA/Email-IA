"""Gera os 3 e-mails do Pré Black 30% OFF (mesmo layout; só muda o bloco da Caixa Surpresa).

    python lata-fit/assets/pre-black-30off/_montar.py

-1: Caixa Surpresa "De R$ 139 por R$ 97,30 com cupom" (Figma 16001:8889)
-2: Caixa Surpresa "De R$ 210 por R$ 139,00 com cupom" (Figma 16005:2)
-3: sem a Caixa Surpresa (Figma 16005:192)

Os .mjml gerados são o que vai para o Flash. Ajuste aqui e rode de novo, para os três ficarem iguais.
"""
import os

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
CDN = 'https://cdn.shopify.com/s/files/1/0829/8731/9551/files/lf-p30-'
SITE = 'https://www.latamfit.com.br'
FF = "'Helvetica Neue', Helvetica, Arial, sans-serif"
MARROM, VERMELHO, ROSA, AMARELO, CREME, BRANCO = '#5a2a1e', '#c8365a', '#f4a8c4', '#f6e77e', '#f8f3e7', '#fefdfd'
TODOS = SITE + '/collections/all'
CAIXA = SITE + '/products/caixa-surpresa'
COCADA = SITE + '/products/cocada-com-chocolate-zero-acucar-300g-12-uni-de-25g-cada-latam-fit'
GOIABINHA = SITE + '/products/goiabinha-zero-acucar-264g-12-uni-de-22g-cada-latam-fit'
WAFER = SITE + '/products/wafer-cookie-cream-proteina-coberto-com-chocolate-300g-12-uni-de-25g-cada-latam-protein'
IG = 'https://www.instagram.com/latam.fit/'
P0 = 'padding-top="0px" padding-right="0px" padding-bottom="0px" padding-left="0px"'

ESTILO = """      @media only screen and (max-width:480px) {
        .p30-logo { padding-top:14px !important; }
        .p30-logo table, .p30-logo td { width:80px !important; }
        .p30-logo img { width:80px !important; height:24px !important; }
        .p30-frete { padding-top:6px !important; padding-bottom:14px !important; }
        .p30-frete div { font-size:10px !important; line-height:13px !important; letter-spacing:0.4px !important; }
        .p30-pre { padding-top:34px !important; }
        .p30-pre div { font-size:13px !important; line-height:18px !important; letter-spacing:1px !important; }
        .p30-l { width:40px !important; height:2px !important; line-height:2px !important; }
        .p30-pt { margin:0 10px !important; }
        .p30-big { padding-top:10px !important; }
        .p30-big div { font-size:62px !important; line-height:66px !important; letter-spacing:-1px !important; }
        .p30-site div { font-size:28px !important; line-height:30px !important; letter-spacing:-0.3px !important; }
        .p30-par { padding-top:12px !important; padding-left:13px !important; padding-right:13px !important; }
        .p30-par div { font-size:12.5px !important; line-height:16px !important; }
        .p30-par div div { max-width:316px !important; }
        .p30-c1w { padding-top:16px !important; }
        .p30-c1 { padding:7px 10px !important; }
        .p30-c1a { font-size:10px !important; line-height:12px !important; letter-spacing:0.6px !important; }
        .p30-c1b { padding-top:2px !important; font-size:28px !important; line-height:30px !important; }
        .p30-c1c { padding-top:2px !important; font-size:10px !important; line-height:12px !important; letter-spacing:0.3px !important; }
        .p30-btn1 { padding-top:16px !important; padding-bottom:4px !important; }
        .p30-btn1 table { width:196px !important; }
        .p30-btn1 a { width:176px !important; font-size:12px !important; line-height:16px !important; letter-spacing:0.5px !important; padding:11px 10px !important; }
        .p30-h2 { padding-top:34px !important; padding-left:10px !important; padding-right:10px !important; }
        .p30-h2 div { font-size:19px !important; line-height:22px !important; }
        .p30-c2w { padding-top:14px !important; }
        .p30-c2 { padding:14px 16px !important; }
        .p30-c2a { font-size:10px !important; line-height:12px !important; letter-spacing:0.5px !important; }
        .p30-c2b { padding-top:2px !important; font-size:26px !important; line-height:27px !important; }
        .p30-pill { padding:9px 16px !important; font-size:12px !important; line-height:16px !important; letter-spacing:0.6px !important; border-radius:17px !important; }
        .p30-val { padding-top:10px !important; }
        .p30-val div { font-size:11px !important; line-height:14px !important; letter-spacing:0.4px !important; }
        .p30-btn2 { padding-top:14px !important; padding-bottom:29px !important; }
        .p30-btn2 table { width:212px !important; }
        .p30-btn2 a { width:192px !important; font-size:12px !important; line-height:16px !important; letter-spacing:0.5px !important; padding:11px 10px !important; }
        .p30-of { padding-top:23px !important; padding-left:10px !important; padding-right:10px !important; }
        .p30-of div { font-size:10px !important; line-height:13px !important; letter-spacing:0.6px !important; }
        .p30-cx { padding-top:5px !important; }
        .p30-cx div { font-size:36px !important; line-height:40px !important; letter-spacing:-0.3px !important; }
        .p30-tkw { padding-top:10px !important; }
        .p30-tk-t { height:10px !important; }
        .p30-tk-bt { height:9px !important; }
        .p30-tk-e { width:5px !important; }
        .p30-tk-tl { border-radius:9px 0 0 0 !important; }
        .p30-tk-tr { border-radius:0 9px 0 0 !important; }
        .p30-tk-bl { border-radius:0 0 0 9px !important; }
        .p30-tk-br { border-radius:0 0 9px 0 !important; }
        .p30-tk-a { height:17px !important; }
        .p30-tk-b { height:18px !important; }
        .p30-tk-nl { width:4px !important; height:9px !important; border-radius:0 6px 6px 0 !important; }
        .p30-tk-nr { width:4px !important; height:9px !important; border-radius:6px 0 0 6px !important; }
        .p30-tk-npt { height:11px !important; }
        .p30-tk-npb { height:10px !important; }
        .p30-tk-nt { width:5px !important; height:3px !important; border-radius:0 0 3px 3px !important; }
        .p30-tk-nb { width:5px !important; height:3px !important; border-radius:3px 3px 0 0 !important; }
        .p30-tk-aw { width:48px !important; }
        .p30-tk-m { padding:0 6px 0 12px !important; }
        .p30-tk-de { font-size:11.5px !important; line-height:15px !important; padding:0 8px 2px 0 !important; }
        .p30-tk-pr { padding:0 3px 4px 0 !important; }
        .p30-tk-por { font-size:12px !important; line-height:12px !important; }
        .p30-tk-rs { font-size:16px !important; line-height:18px !important; }
        .p30-tk-num { font-size:34px !important; line-height:34px !important; letter-spacing:-0.5px !important; }
        .p30-tk-cents { font-size:24px !important; }
        .p30-tk-cc { font-size:10px !important; line-height:11px !important; letter-spacing:0.5px !important; }
        .p30-par2 { padding-top:14px !important; padding-left:16px !important; padding-right:16px !important; }
        .p30-par2 div { font-size:13px !important; line-height:17px !important; }
        .p30-par2 div div { max-width:%%PARW_M%%px !important; }
        .p30-btn3 { padding-top:15px !important; padding-bottom:34px !important; }
        .p30-btn3 table { width:250px !important; }
        .p30-btn3 a { width:230px !important; font-size:12px !important; line-height:16px !important; letter-spacing:0.5px !important; padding:11px 10px !important; }
        .p30-qt { padding-top:30px !important; }
        .p30-qt div { font-size:29px !important; line-height:32px !important; letter-spacing:-0.3px !important; }
        .p30-gw { padding-top:17px !important; }
        .p30-gsp { height:12px !important; }
        .p30-ct { padding:8px 5% 17px !important; font-size:11.5px !important; line-height:14px !important; border-radius:0 0 19px 19px !important; }
        .p30-btn4 { padding-top:24px !important; padding-bottom:30px !important; }
        .p30-btn4 table { width:220px !important; }
        .p30-btn4 a { width:200px !important; font-size:13px !important; line-height:16px !important; letter-spacing:0.6px !important; padding:12px 10px !important; }
        .p30-et { padding-top:26px !important; }
        .p30-et div { font-size:24px !important; line-height:28px !important; letter-spacing:0 !important; }
        .p30-iw { padding:24px 0 26px !important; }
        .p30-ic { width:24.25% !important; font-size:10px !important; line-height:11px !important; letter-spacing:0.3px !important; }
        .p30-ip { width:0.6% !important; }
        .p30-ici { width:40px !important; height:40px !important; margin:0 auto 6px !important; }
        .p30-strip { padding-top:10px !important; padding-bottom:10px !important; padding-left:6px !important; padding-right:6px !important; }
        .p30-strip div { font-size:10px !important; line-height:13px !important; }
        .p30-flogo { padding-top:26px !important; }
        .p30-flogo table, .p30-flogo td { width:127px !important; }
        .p30-flogo img { width:127px !important; height:38px !important; }
        .p30-igw { padding-top:12px !important; }
        .p30-igi { padding-right:10px !important; }
        .p30-ig { width:32px !important; height:32px !important; }
        .p30-ig1 { font-size:13px !important; line-height:17px !important; }
        .p30-ig2 { padding-top:5px !important; font-size:11px !important; line-height:14px !important; }
        .p30-legal { padding-top:20px !important; padding-bottom:24px !important; }
        .p30-legal div { font-size:10px !important; line-height:15px !important; }
      }
      @media only screen and (max-width:359px) {
        .p30-l { width:30px !important; }
        .p30-h2 div { font-size:17px !important; line-height:20px !important; }
        .p30-c2b { font-size:22px !important; line-height:24px !important; }
        .p30-pill { padding:8px 12px !important; font-size:11px !important; line-height:15px !important; }
        .p30-tk { width:74% !important; }
        .p30-ct { font-size:10.5px !important; line-height:13px !important; padding-bottom:16px !important; }
        .p30-ic { font-size:9px !important; line-height:10px !important; }
        .p30-ig1 { font-size:12px !important; }
      }"""


def texto(cls, conteudo, tam, lh, cor=MARROM, peso='400', ls=None, pt=0, pr=0, pb=0, pl=0):
    ls = f' letter-spacing="{ls}"' if ls is not None else ''
    return (f'<mj-text css-class="{cls}" align="center" font-family="{FF}" font-size="{tam}px" font-weight="{peso}" '
            f'line-height="{lh}px"{ls} color="{cor}" padding-top="{pt}px" padding-right="{pr}px" padding-bottom="{pb}px" '
            f'padding-left="{pl}px">{conteudo}</mj-text>')


def botao(cls, rotulo, href, fundo, cor, largura, tam=16, lh=22, inner=19, ls='0.8px', pt=0, pb=0):
    return (f'<mj-button css-class="{cls}" href="{href}" background-color="{fundo}" color="{cor}" font-family="{FF}" '
            f'font-size="{tam}px" font-weight="700" line-height="{lh}px" letter-spacing="{ls}" border-radius="40px" '
            f'inner-padding="{inner}px 10px" width="{largura}px" align="center" padding-top="{pt}px" padding-right="0px" '
            f'padding-bottom="{pb}px" padding-left="0px">{rotulo}</mj-button>')


def raw(cls, padding, html):
    return f'<mj-raw><tr><td style="padding:{padding};" class="fc-html-block {cls}">{html}</td></tr></mj-raw>'


CUPOM1 = raw('p30-c1w', '24px 0 0', (
    f'<table role="presentation" align="center" width="371" cellpadding="0" cellspacing="0" border="0" style="width:65.32%; '
    f'max-width:371px; margin:0 auto; border:2px dashed {AMARELO}; border-radius:24px; border-collapse:separate;"><tr>'
    f'<td class="p30-c1" align="center" style="padding:12px 16px; font-family:{FF}; color:{MARROM}; text-align:center;">'
    f'<div class="p30-c1a" style="font-size:14px; font-weight:700; line-height:18px; letter-spacing:1px;">USE O CUPOM</div>'
    f'<div class="p30-c1b" style="padding-top:4px; font-size:46px; font-weight:700; line-height:48px; color:{VERMELHO};">PREBLACK</div>'
    f'<div class="p30-c1c" style="padding-top:4px; font-size:12px; font-weight:700; line-height:16px; letter-spacing:0.5px;">VÁLIDO ATÉ 15/11</div>'
    f'</td></tr></table>'))

CUPOM2 = raw('p30-c2w', '24px 0 0', (
    f'<table role="presentation" align="center" width="504" cellpadding="0" cellspacing="0" border="0" style="width:88.73%; '
    f'max-width:504px; margin:0 auto; background-color:#fffaf0; border:2px dashed {VERMELHO}; border-radius:24px; '
    f'border-collapse:separate;"><tr><td class="p30-c2" style="padding:24px 32px;">'
    f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;"><tr>'
    f'<td valign="bottom" align="left" style="font-family:{FF}; color:{MARROM}; text-align:left;">'
    f'<div class="p30-c2a" style="font-size:12px; font-weight:700; line-height:16px; letter-spacing:0.7px;">USE O CUPOM</div>'
    f'<div class="p30-c2b" style="padding-top:4px; font-size:42px; font-weight:700; line-height:44px; color:{VERMELHO};">PREBLACK</div></td>'
    f'<td valign="bottom" align="right" style="text-align:right;"><table role="presentation" align="right" cellpadding="0" '
    f'cellspacing="0" border="0" style="border-collapse:separate;"><tr><td class="p30-pill" style="padding:15px 32px; '
    f'background-color:{VERMELHO}; border-radius:28px; font-family:{FF}; font-size:20px; font-weight:700; line-height:26px; '
    f'letter-spacing:1.2px; color:#ffffff; white-space:nowrap;">30% OFF</td></tr></table></td>'
    f'</tr></table></td></tr></table>'))


def ticket(de, numero):
    borda = '1px solid #e8dec5'
    W8 = 'width="8" '
    AW = 'width="80" '
    fundo = f'background-color:{CREME};'
    zero = 'font-size:0; line-height:0;'

    def canto(cls, lados, raio, h, extra=''):
        b = ' '.join(f'border-{l}:{borda};' for l in lados)
        return f'<td class="{cls}" {extra}style="height:{h}px; {fundo} {b} border-radius:{raio}; {zero}">&nbsp;</td>'

    def lado(direita):
        lb = 'right' if direita else 'left'
        nota = (f'<div class="p30-tk-n{"r" if direita else "l"}" style="width:7px; height:15px; background-color:{BRANCO}; '
                f'border:{borda}; border-{lb}:0; border-radius:{"9px 0 0 9px" if direita else "0 9px 9px 0"};"></div>')
        return (f'<td class="p30-tk-e" width="8" valign="top" style="width:8px; padding:0; {fundo} {zero}">'
                f'<div class="p30-tk-a" style="height:28px; border-{lb}:{borda};"></div>{nota}'
                f'<div class="p30-tk-b" style="height:31px; border-{lb}:{borda};"></div></td>')

    def picote(cima, h):
        lado_b = 'top' if cima else 'bottom'
        raio = '0 0 5px 5px' if cima else '5px 5px 0 0'
        return (f'<td class="p30-tk-np {"p30-tk-npt" if cima else "p30-tk-npb"}" width="10" valign="{lado_b}" '
                f'style="width:2.8%; height:{h + 1}px; padding:0; {fundo} {zero}"><div class="p30-tk-{"nt" if cima else "nb"}" '
                f'style="width:8px; height:4px; margin:0 auto; background-color:{BRANCO}; border:{borda}; border-{lado_b}:0; '
                f'border-radius:{raio};"></div></td>')

    def faixa(cima, h):
        lado_b = 'top' if cima else 'bottom'
        t = 't' if cima else 'bt'
        cantos = ('14px 0 0 0', '0 14px 0 0') if cima else ('0 0 0 14px', '0 0 14px 0')
        c1 = 'p30-tk-tl' if cima else 'p30-tk-bl'
        c2 = 'p30-tk-tr' if cima else 'p30-tk-br'
        return ('<tr>' + canto(f'p30-tk-e p30-tk-{t} {c1}', [lado_b, 'left'], cantos[0], h, extra=W8)
                + canto(f'p30-tk-{t} p30-tk-aw', [lado_b], '0', h, extra=AW) + picote(cima, h)
                + canto(f'p30-tk-{t}', [lado_b], '0', h)
                + canto(f'p30-tk-e p30-tk-{t} {c2}', [lado_b, 'right'], cantos[1], h, extra=W8) + '</tr>')

    conteudo = (
        f'<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
        f'<td class="p30-tk-de" valign="middle" style="padding:0 16px 4px 0; font-family:{FF}; font-size:18px; line-height:24px; '
        f'color:{MARROM}; white-space:nowrap;">De <span style="text-decoration:line-through;">{de}</span></td>'
        f'<td valign="middle" style="padding:0;"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>'
        f'<td class="p30-tk-pr" valign="bottom" style="padding:0 5px 7px 0; font-family:{FF}; white-space:nowrap;">'
        f'<div class="p30-tk-por" style="font-size:19px; line-height:20px; color:{MARROM};">por</div>'
        f'<div class="p30-tk-rs" style="font-size:26px; line-height:28px; color:{VERMELHO};">R$</div></td>'
        f'<td class="p30-tk-num" valign="bottom" style="padding:0; font-family:{FF}; font-size:56px; font-weight:700; '
        f'line-height:56px; letter-spacing:-1px; color:{VERMELHO}; white-space:nowrap;">{numero}</td></tr>'
        f'<tr><td style="padding:0;"></td><td class="p30-tk-cc" align="center" style="padding:0; font-family:{FF}; '
        f'font-size:12px; line-height:14px; letter-spacing:0.9px; color:{MARROM}; text-align:center; white-space:nowrap;">'
        f'COM CUPOM</td></tr></table></td></tr></table>')
    return raw('p30-tkw', '16px 0 0', (
        f'<table role="presentation" class="p30-tk" align="center" width="357" cellpadding="0" cellspacing="0" border="0" '
        f'style="width:62.85%; max-width:357px; margin:0 auto; border-collapse:separate;">'
        f'{faixa(True, 18)}'
        f'<tr>{lado(False)}<td class="p30-tk-m" colspan="3" valign="middle" style="padding:0 24px 0 32px; {fundo}">{conteudo}</td>{lado(True)}</tr>'
        f'{faixa(False, 15)}'
        f'</table>'))


def card(img, alt, href, cor, nome):
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%; '
            f'border-collapse:separate;"><tr><td style="padding:0; font-size:0; line-height:0;"><a href="{href}" target="_blank">'
            f'<img src="{CDN}{img}" width="270" alt="{alt}" style="display:block; width:100%; max-width:270px; height:auto; '
            f'border:0; outline:none;"></a></td></tr><tr><td class="p30-ct" align="center" style="padding:15px 8% 29px; '
            f'background-color:{cor}; border-radius:0 0 32px 32px; font-family:{FF}; font-size:18px; font-weight:700; '
            f'line-height:22px; color:{MARROM}; text-align:center;"><a href="{href}" target="_blank" style="color:{MARROM}; '
            f'text-decoration:none;">{nome}</a></td></tr></table>')


GRADE = raw('p30-gw', '28px 0 0', (
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;"><tr>'
    f'<td width="270" valign="top" style="width:48.21%;">{card("card-1.png", "Cocada com Chocolate Zero Açúcar com 30% OFF", COCADA, "#f1ddc8", "Cocada com Chocolate<br>Zero Açúcar")}</td>'
    '<td width="20" style="width:3.58%; font-size:0; line-height:0;">&nbsp;</td>'
    f'<td width="270" valign="top" style="width:48.21%;">{card("card-2.png", "Goiabinha Zero Açúcar com 30% OFF", GOIABINHA, "#f7cfde", "Goiabinha<br>Zero Açúcar")}</td>'
    '</tr><tr><td colspan="3" class="p30-gsp" style="height:20px; font-size:0; line-height:0;">&nbsp;</td></tr><tr>'
    f'<td width="270" valign="top" style="width:48.21%;">{card("card-3.png", "Cocada com Chocolate Zero Açúcar com 30% OFF", COCADA, "#f5e7a3", "Cocada com Chocolate<br>Zero Açúcar")}</td>'
    '<td width="20" style="width:3.58%; font-size:0; line-height:0;">&nbsp;</td>'
    f'<td width="270" valign="top" style="width:48.21%;">{card("card-4.png", "Wafer Cookies &amp; Cream com proteína com 30% OFF", WAFER, "#c4e2f9", "Wafer Cookies &amp; Cream<br>com proteína")}</td>'
    '</tr></table>'))

ICONES = [('icone-1.png', SITE + '/collections/frontpage', 'OPÇÕES SEM<br>LACTOSE'),
          ('icone-2.png', SITE + '/collections/sem-gluten', 'OPÇÕES SEM<br>GLÚTEN'),
          ('icone-3.png', SITE + '/collections/com-proteina', 'OPÇÕES COM<br>PROTEÍNA'),
          ('icone-4.png', SITE + '/collections/vegano', 'OPÇÕES<br>VEGANAS')]
PAD = '<td class="p30-ip" width="16" style="width:2.86%; font-size:0; line-height:0;">&nbsp;</td>'
LINHA_ICONES = raw('p30-iw', '40px 0 40px', (
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;"><tr>' + PAD +
    PAD.join(f'<td class="p30-ic" width="120" valign="top" align="center" style="width:21.43%; font-family:{FF}; font-size:13px; '
             f'font-weight:700; line-height:14px; letter-spacing:0.5px; color:{MARROM}; text-align:center;"><a href="{h}" '
             f'target="_blank" style="color:{MARROM}; text-decoration:none;"><img class="p30-ici" src="{CDN}{i}" width="64" '
             f'height="64" alt="" style="display:block; width:64px; height:64px; margin:0 auto 10px; border:0; outline:none;">'
             f'{r}</a></td>' for i, h, r in ICONES) + PAD + '</tr></table>'))

INSTAGRAM = raw('p30-igw', '16px 0 0', (
    f'<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:0 auto;"><tr>'
    f'<td class="p30-igi" valign="middle" style="padding:0 16px 0 0;"><a href="{IG}" target="_blank"><img class="p30-ig" '
    f'src="{CDN}instagram.png" width="48" height="48" alt="Instagram" style="display:block; width:48px; height:48px; border:0; '
    f'outline:none;"></a></td><td valign="middle" align="center" style="font-family:{FF}; text-align:center;">'
    f'<div class="p30-ig1" style="font-size:18px; font-weight:700; line-height:24px; color:{CREME};"><a href="{IG}" '
    f'target="_blank" style="color:{CREME}; text-decoration:none;">Siga @latam.fit no Instagram</a></div>'
    f'<div class="p30-ig2" style="padding-top:11px; font-size:14px; line-height:18px; color:#bca79b;">Cupom PREBLACK válido até 15/11</div>'
    f'</td></tr></table>'))


def secao(fundo, filhos, raio=None, pl=0, pr=0):
    r = f' border-radius="{raio}"' if raio else ''
    corpo = '\n'.join('          ' + f for f in filhos)
    return (f'      <mj-section background-color="{fundo}"{r} padding-top="0px" padding-right="{pr}px" padding-bottom="0px" '
            f'padding-left="{pl}px">\n        <mj-column>\n{corpo}\n        </mj-column>\n      </mj-section>')


def email(caixa, gap):
    cupom_fecha = caixa is None
    s1 = secao(ROSA, [
        texto('p30-pre', (f'<span class="p30-l" style="display:inline-block; width:80px; height:3px; line-height:3px; font-size:1px; '
                          f'background-color:{MARROM}; vertical-align:middle;">&nbsp;</span><span class="p30-pt" '
                          f'style="display:inline-block; margin:0 18px; vertical-align:middle;">PRÉ BLACK LATAM FIT</span>'
                          f'<span class="p30-l" style="display:inline-block; width:80px; height:3px; line-height:3px; font-size:1px; '
                          f'background-color:{MARROM}; vertical-align:middle;">&nbsp;</span>'),
              22, 30, peso='700', ls='1.6px', pt=57, pr=10, pl=10),
        texto('p30-big', '30% OFF', 102, 108, cor='#ffffff', peso='700', ls='-2px', pt=20),
        texto('p30-site', 'no site todo', 46, 46, peso='700', ls='-0.5px'),
        texto('p30-par', '<div style="max-width:455px; margin:0 auto;">Doces zero adição de açúcares, wafers com proteína, '
                         'caixas e combos. Tudo com desconto até 15/11.</div>', 18, 24, pt=20, pr=20, pl=20),
        CUPOM1,
        botao('p30-btn1', 'APROVEITAR 30% OFF', TODOS, AMARELO, MARROM, 320, pt=24, pb=5),
        f'<mj-image src="{CDN}hero.jpg" alt="Goiabinha, Cocada e Wafer Protein Latam Fit com 30% OFF" width="568px" '
        f'href="{TODOS}" {P0}></mj-image>',
    ], raio='32px 32px 0 0')
    s2 = secao(BRANCO, [
        texto('p30-h2', '30% OFF em todos os produtos', 32, 35, peso='700', pt=56, pr=20, pl=20),
        CUPOM2,
        texto('p30-val', 'VÁLIDO ATÉ 15/11', 16, 21, peso='700', ls='0.6px', pt=16),
        botao('p30-btn2', 'COMPRAR COM O CUPOM', TODOS, VERMELHO, '#ffffff', 352, pt=24, pb=48),
    ], raio='0 0 32px 32px' if cupom_fecha else None)
    blocos = [s1, s2]
    if caixa:
        blocos.append(secao(BRANCO, [
            f'<mj-image src="{CDN}caixa.jpg" alt="Caixa Surpresa Latam Fit: pague R$ 139 e leve mais de R$ 210 em produtos" '
            f'width="568px" href="{CAIXA}" {P0}></mj-image>',
            texto('p30-of', 'A OFERTA MAIS VANTAJOSA DO PRÉ BLACK', 15, 21, peso='700', ls='1px', pt=38, pr=20, pl=20),
            texto('p30-cx', 'Caixa Surpresa', 60, 66, peso='700', ls='-0.5px', pt=8),
            ticket(caixa['de'], caixa['numero']),
            texto('p30-par2', f'<div style="max-width:{caixa["parw"]}px; margin:0 auto;">{caixa["par"]}</div>', 18, 24,
                  pt=24, pr=20, pl=20),
            botao('p30-btn3', 'QUERO MINHA CAIXA SURPRESA', CAIXA, VERMELHO, '#ffffff', 408, pt=25, pb=56),
        ], raio='0 0 32px 32px'))
    wrapper = (f'    <mj-wrapper background-color="#f7dade" background-url="{CDN}ondas.jpg" background-size="600px auto" '
               f'background-repeat="repeat" background-position="center top" padding-top="20px" padding-right="16px" '
               f'padding-bottom="{gap}px" padding-left="16px">\n' + '\n'.join(blocos) + '\n    </mj-wrapper>')

    topo = secao(CREME, [
        f'<mj-image css-class="p30-logo" src="{CDN}logo.png" alt="Latam Fit" width="106px" height="32px" align="center" '
        f'href="{SITE}" padding-top="20px" padding-right="0px" padding-bottom="0px" padding-left="0px"></mj-image>',
        texto('p30-frete', 'FRETE GRÁTIS ACIMA DE R$ 99 PARA TODO O BRASIL', 12, 16, peso='700', ls='0.6px', pt=8, pr=10, pb=20, pl=10),
    ])
    queridinhos = secao(BRANCO, [
        texto('p30-qt', f'Os <span style="color:{VERMELHO};">queridinhos</span><br>com 30% OFF', 48, 53, peso='700',
              ls='-0.5px', pt=48),
        GRADE,
        botao('p30-btn4', 'VER OS MAIS VENDIDOS', SITE + '/collections/mais-vendidos', VERMELHO, '#ffffff', 357, tam=18,
              lh=24, inner=20, ls='1px', pt=40, pb=48),
    ], pl=20, pr=20)
    favorito = secao(CREME, [
        texto('p30-et', 'Encontre o seu favorito', 40, 44, peso='700', ls='-0.3px', pt=40),
        LINHA_ICONES,
    ], pl=20, pr=20)
    faixa = secao(VERMELHO, [
        texto('p30-strip', 'Zero adição de açúcares&nbsp; · &nbsp;Direto da fábrica&nbsp; · &nbsp;Frete grátis acima de R$ 99',
              15, 20, cor=BRANCO, pt=16, pr=10, pb=16, pl=10),
    ])
    rodape = secao(MARROM, [
        f'<mj-image css-class="p30-flogo" src="{CDN}logo-rodape.png" alt="Latam Fit" width="211px" height="64px" align="center" '
        f'href="{SITE}" padding-top="40px" padding-right="0px" padding-bottom="0px" padding-left="0px"></mj-image>',
        INSTAGRAM,
        texto('p30-legal', ('Latam Fit · Rua José Elias, 71, sala&nbsp;116 · Uberlândia/MG&nbsp;·&nbsp;38411-217<br>'
                            '<a href="mailto:sac@latamfit.com.br" style="color:#bca79b; text-decoration:underline;">sac@latamfit.com.br</a><br>'
                            'Você recebeu este e-mail porque se cadastrou ou comprou na Latam Fit. '
                            f'<a href="{{{{link_optout}}}}" style="color:{CREME}; text-decoration:underline;">Não quero mais receber</a>'),
              11, 17, cor='#bca79b', pt=32, pr=12, pb=32, pl=12),
    ], pl=20, pr=20)
    def fora(s):
        return '\n'.join(l[2:] for l in s.split('\n'))

    corpo = '\n\n'.join([fora(topo), wrapper] + [fora(s) for s in (queridinhos, favorito, faixa, rodape)])
    estilo = ESTILO.replace('%%PARW_M%%', str(round(caixa['parw'] * 13 / 18)) if caixa else '264')
    return (f'<mjml>\n  <mj-head>\n    <mj-style>\n{estilo}\n    </mj-style>\n  </mj-head>\n'
            f'  <mj-body background-color="{CREME}" width="600px">\n\n{corpo}\n\n  </mj-body>\n</mjml>\n')


VARIANTES = {
    '1': (dict(de='R$ 139', numero='97,30', parw=365,
               par='Receba mais de R$ 210 em produtos e descubra novos sabores Latam Fit.'), 40),
    '2': (dict(de='R$ 210', numero='139<span class="p30-tk-cents" style="font-size:40px;">,00</span>', parw=390,
               par='Receba mais de R$ 210 em produtos e descubra novos sabores Latam Fit pagando apenas R$ 139,00.'), 16),
    '3': (None, 23),
}
for n, (caixa, gap) in VARIANTES.items():
    arq = os.path.join(RAIZ, 'lata-fit', f'pre-black-30off-{n}.mjml')
    with open(arq, 'w', encoding='utf-8', newline='\n') as f:
        f.write(email(caixa, gap))
    print(arq)
