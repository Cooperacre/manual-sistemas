"""Gera o PDF único do manual (capa, sumário, fichas na ordem do menu, governança e anexo).

Uso (na raiz do projeto, com `npm run build` já feito e o dev server fechado):
    python tools/gerar_pdf.py

Cada página do `dist/` vira um PDF pelo Edge sem janela; depois o PyMuPDF junta tudo,
troca os links internos por "(p. N)" clicável e cria os marcadores. O Manual Operacional da
Filial IV (outra pasta, `ANEXO_REPO`) é construído num diretório temporário e entra inteiro
como Anexo A, para o PDF impresso se bastar sem depender de link. Duas saídas em pdf/:
  manual-sistemas-matriz.pdf   fichas com o protocolo de assinatura ao fim de cada uma
  manual-sistemas-leitura.pdf  fichas sem protocolo e, no fim, uma Folha de validação única
"""
import functools
import http.server
import re
import sys
import shutil
import subprocess
import tempfile
import threading
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import pymupdf

RAIZ = Path(__file__).resolve().parent.parent
DIST = RAIZ / "dist"
SAIDA = RAIZ / "pdf"
ANEXO_REPO = RAIZ.parent / "cooperacre4-manual"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORTAS = {"hub": 4399, "anexo": 4398}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]

# (grupo, título, slug) na ordem do menu lateral (astro.config.mjs)
PAGINAS = [
    ("Introdução", "O que é este manual", "intro"),
    ("Introdução", "Glossário", "glossario"),
    ("Catálogo de Sistemas", "Visão geral", "catalogo"),
    ("Catálogo de Sistemas", "Por situação", "catalogo/situacao"),
    ("Catálogo de Sistemas", "Onde está o código", "catalogo/repositorios"),
    ("Sistemas", "Visão geral", "sistemas"),
    ("Sistemas", "Análise Comercial", "catalogo/analisecomercial"),
    ("Sistemas", "Comissão", "catalogo/comissao"),
    ("Sistemas", "Consulta Meta", "catalogo/consultameta"),
    ("Sistemas", "CooperConecta", "catalogo/cooperconecta"),
    ("Sistemas", "CooperFlow", "catalogo/cooperflow"),
    ("Sistemas", "Cooperlog", "catalogo/cooperlog"),
    ("Sistemas", "Net Monitor", "catalogo/netmonitor"),
    ("Planilhas", "Visão geral", "planilhas"),
    ("Planilhas", "Controle de Saída", "catalogo/controle-de-saida"),
    ("Planilhas", "Controle Interno", "planilhas/controle-interno"),
    ("Planilhas", "Estoque Polpa", "catalogo/estoquepolpa"),
    ("Planilhas", "Transferência Estoque Balcão", "planilhas/transferencia-estoque-balcao"),
    ("Automações", "Visão geral", "automacoes"),
    ("Automações", "Meta Pipeline", "catalogo/meta-pipeline"),
    ("Automações", "Conciliador Contábil", "catalogo/contabil"),
    ("Automações", "Controle de Vendas", "catalogo/controledevendas"),
    ("Automações", "Conversor de Extrato SICOOB", "automacoes/pdftoexcel"),
    ("Automações", "Formatar Exportação", "automacoes/formatar-exportacao"),
    ("Automações", "Gerador de Cards", "automacoes/gerador-cards"),
    ("Filial IV", "Visão geral", "catalogo/filial-4"),
    ("Filial IV", "Webapp: versão Veja", "catalogo/webapp-filial-iv-veja"),
    ("Filial IV", "Webapp: interno", "catalogo/webapp-filial-iv-interno"),
    ("Filial IV", "Planilha de Contrato", "catalogo/planilha-contrato-filial-iv"),
    ("Filial IV", "DARB", "catalogo/darb-filial-iv"),
    ("Filial IV", "Relação de Despesas", "catalogo/relacao-despesas-filial-iv"),
    ("Filial IV", "Manual Operacional", "catalogo/manual-filial-iv"),
    ("Governança", "Princípios", "governanca/principios"),
    ("Governança", "Acessos e responsabilidades", "governanca/acessos"),
    ("Governança", "Mudanças e versionamento", "governanca/mudancas"),
    ("Governança", "Desenvolvimento com IA", "governanca/desenvolvimento-com-ia"),
    ("Governança", "Vibe coding", "governanca/vibe-coding"),
    ("Governança", "Credenciais e backup", "governanca/credenciais-e-backup"),
]

# Anexo A: menu lateral do manual da Filial IV (cooperacre4-manual/astro.config.mjs)
GRUPO_ANEXO = "Anexo A: Manual Operacional da Filial IV"
ANEXO = [
    ("O que é este manual", "intro"),
    ("Glossário", "glossario"),
    ("Rotina Diária", "rotinas/rotina-diaria"),
    ("Rotina de Sexta-Feira", "rotinas/sexta-feira"),
    ("Recebimento de Borracha", "procedimentos/recebimento-borracha"),
    ("Embarque de GEB", "procedimentos/embarque"),
    ("Despesas Semanais", "procedimentos/despesas"),
    ("Compra de Lenha", "procedimentos/compra-lenha"),
    ("Entrega de EPIs", "procedimentos/entrega-epis"),
    ("Solicitação de Serviços", "procedimentos/solicitacao-servicos"),
    ("Relatório Quinzenal RH", "procedimentos/relatorio-rh"),
    ("DARB", "procedimentos/darb"),
    ("Protocolo de Correspondência", "procedimentos/protocolo-correspondencia"),
    ("Planilha de Contrato: visão geral", "planilha/visao-geral"),
    ("Planilha de Contrato: detalhamento das abas", "planilha/abas"),
    ("Webapp: visão geral", "webapp/visao-geral"),
    ("Webapp: seções do app", "webapp/secoes"),
]

# (grupo, título, slug, site): tudo que entra no PDF, na ordem
# O anexo entra logo depois da ficha "Manual Operacional" (Filial IV), antes da governança
_fim_filial = next(i for i, p in enumerate(PAGINAS) if p[2] == "catalogo/manual-filial-iv") + 1
ITENS = ([(g, t, s, "hub") for g, t, s in PAGINAS[:_fim_filial]]
         + [(GRUPO_ANEXO, t, s, "anexo") for t, s in ANEXO]
         + [(g, t, s, "hub") for g, t, s in PAGINAS[_fim_filial:]])

# Impressão do anexo: o CSS dele só mostra o checklist; aqui entra o padrão do hub (10 pt, sem menus)
CSS_ANEXO = """<style>@media print {
  body * { visibility: visible !important; }
  .print-checklist, .btn-print { display: none !important; }
  header.header, .sidebar, .right-sidebar, mobile-starlight-toc, starlight-menu-button, footer,
  .pagination-links { display: none !important; }
  :root { --sl-content-width: 100%; --sl-sidebar-width: 0px; --sl-nav-height: 0px; }
  .main-frame, .main-pane, .content-panel { padding: 0 !important; margin: 0 !important; max-width: 100% !important; }
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  html { font-size: 13.5px; }
  .sl-markdown-content img { width: 90%; max-width: 90% !important; max-height: 12cm; object-fit: contain; break-inside: avoid; }
  .sl-markdown-content .sl-heading-wrapper, .sl-markdown-content h2, .sl-markdown-content h3, .sl-markdown-content h4 { break-after: avoid; break-inside: avoid; }
  .sl-markdown-content table, .sl-markdown-content tr, .sl-markdown-content .starlight-aside { break-inside: avoid; }
  .sl-markdown-content table { border-collapse: collapse !important; border: 1.5px solid #475569 !important; }
  .sl-markdown-content table th, .sl-markdown-content table td { border: 1px solid #94a3b8 !important; }
  .sl-markdown-content table th { background: #cbd5e1 !important; color: #0f172a !important; }
  .sl-markdown-content table tbody tr:nth-child(even) td { background: #f1f5f9 !important; }
  @page { size: A4; margin: 2cm 1.5cm 1.5cm;
    @top-left { content: "Cooperacre · Manual Operacional da Filial IV"; font-family: "Segoe UI", sans-serif; font-size: 9pt; color: #475569; } }
}</style>"""

# Referência de página: cada link interno ganha "(p. XXX)", onde XXX é um código derivado do destino
# (mesmo cálculo no hub, em astro.config.mjs). Depois da montagem, o código vira o número da página.
JS_REF = """<script>
document.addEventListener('DOMContentLoaded', () => {
  const cod = (k) => { let h = 0; for (const c of k) h = (h * 31 + c.charCodeAt(0)) % 456976;
    return String.fromCharCode(65 + h % 26, 65 + Math.floor(h / 26) % 26, 65 + Math.floor(h / 676) % 26, 65 + Math.floor(h / 17576) % 26); };
  document.querySelectorAll('.sl-markdown-content a[href]').forEach((a) => {
    const h = a.getAttribute('href');
    if (!h.startsWith('/') || h.startsWith('//')) return;
    const chave = 'A:' + h.split('#')[0].split('?')[0].replace(/^\\/|\\/$/g, '');
    const s = document.createElement('span');
    s.textContent = ' (p. ' + cod(chave) + ')';
    a.after(s);
  });
});
</script>"""


def codigo(chave: str) -> str:
    h = 0
    for c in chave:
        h = (h * 31 + ord(c)) % 456976
    return chr(65 + h % 26) + chr(65 + (h // 26) % 26) + chr(65 + (h // 676) % 26) + chr(65 + (h // 17576) % 26)


def chave_de(site: str, slug: str) -> str:
    return ("A:" if site == "anexo" else "") + slug.strip("/")


def imprimir(url: str, destino: Path) -> None:
    subprocess.run(
        [EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=15000", f"--print-to-pdf={destino}", url],
        check=True, capture_output=True, timeout=180,
    )


def construir_anexo(destino: Path) -> None:
    """Constrói o manual da Filial IV fora do repositório dele e prepara as páginas para o papel."""
    npx = shutil.which("npx") or "npx.cmd"
    subprocess.run([npx, "astro", "build", "--outDir", str(destino)], cwd=ANEXO_REPO,
                   check=True, capture_output=True, timeout=600)
    for html in destino.rglob("index.html"):
        txt = html.read_text(encoding="utf-8")
        # O último "</head>" é o real: o script printChecklist do manual da Filial IV tem a mesma string dentro de um texto
        i = txt.rfind("</head>")
        html.write_text(txt[:i] + CSS_ANEXO + JS_REF + txt[i:], encoding="utf-8")


def html_capa_sumario(inicios: list[int], versao: str, pag_folha: int | None = None) -> str:
    linhas, grupo_atual = [], None
    for (grupo, titulo, _, _), pag in zip(ITENS, inicios):
        if grupo != grupo_atual:
            linhas.append(f'<h3>{grupo}</h3>')
            grupo_atual = grupo
        linhas.append(f'<div class="l"><span>{titulo}</span><i></i><b>{pag}</b></div>')
    if pag_folha:
        linhas.append('<h3>Assinatura</h3>')
        linhas.append(f'<div class="l"><span>Folha de validação</span><i></i><b>{pag_folha}</b></div>')
    return f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><style>
@page {{ size: A4; margin: 18mm 20mm }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1f2937; margin: 0 }}
.capa {{ height: 255mm; display: flex; flex-direction: column; justify-content: center; page-break-after: always;
  border-left: 8px solid #21c25e; padding-left: 14mm }}
.capa small {{ color: #15803d; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; font-size: 12pt }}
.capa h1 {{ font-size: 34pt; margin: 6mm 0 4mm; color: #14532d }}
.capa p {{ font-size: 13pt; color: #475569; max-width: 130mm; line-height: 1.5 }}
.capa .v {{ margin-top: 14mm; font-size: 11pt }}
h2 {{ color: #14532d; font-size: 20pt; margin: 0 0 6mm }}
h3 {{ color: #15803d; font-size: 11pt; margin: 4mm 0 1mm; text-transform: uppercase; letter-spacing: .06em }}
.l {{ display: flex; align-items: baseline; font-size: 10.5pt; line-height: 1.55 }}
.l i {{ flex: 1; border-bottom: 1px dotted #94a3b8; margin: 0 2mm }}
</style>
<div class="capa"><small>Cooperacre · T.I.</small><h1>Manual de Sistemas<br>Matriz e Filial IV</h1>
<p>Catálogo dos sistemas, planilhas e automações desenvolvidos para a Cooperacre, com a governança que os sustenta.</p>
<p class="v">{versao}<br>Desenvolvido por Lucas Castro, T.I. da Cooperacre</p></div>
<h2>Sumário</h2>{''.join(linhas)}</html>"""


def eh_ficha(slug: str) -> bool:
    return 'class="selos' in (DIST / slug / "index.html").read_text(encoding="utf-8")


def limpar_parte(doc: pymupdf.Document) -> None:
    """Remove páginas em branco e o contador "Página x de y" do Edge (a numeração é global)."""
    for n in range(len(doc) - 1, -1, -1):
        pg = doc[n]
        util = [l for l in pg.get_text().splitlines()
                if l.strip() and not l.startswith("Cooperacre") and not re.match(r"P.gina \d+ de \d+", l)]
        if not util and not pg.get_images() and not pg.get_drawings():
            doc.delete_page(n)
    for pg in doc:
        achou = False
        for bloco in pg.get_text("dict")["blocks"]:
            for linha in bloco.get("lines", []):
                texto = "".join(s["text"] for s in linha["spans"]).strip()
                if linha["bbox"][1] < 45 and re.fullmatch(r"P.gina \d+ de \d+", texto):
                    pg.add_redact_annot(pymupdf.Rect(linha["bbox"]) + (-2, -2, 2, 2), fill=False)
                    achou = True
        if achou:
            pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)


def resolver_referencias(final: pymupdf.Document, pagina_de: dict[str, int], codigos: dict[str, str]) -> None:
    """Troca "(p. XXX)" pelo número da página, liga o link ao destino e apaga o que não tem destino."""
    for pg in final:
        for l in pg.get_links():
            uri = l.get("uri", "")
            u = urlparse(uri)
            if u.hostname != "127.0.0.1":
                continue
            site = "anexo" if u.port == PORTAS["anexo"] else "hub"
            chave = chave_de(site, u.path)
            pg.delete_link(l)
            if chave in pagina_de:
                pg.insert_link({"kind": pymupdf.LINK_GOTO, "from": l["from"], "page": pagina_de[chave] - 1,
                                "to": pymupdf.Point(0, 0)})
        achados = set(re.findall(r"\(p\. ([A-Z]{4})\)", pg.get_text()))
        for cod in achados:
            alvo = pagina_de.get(codigos.get(cod, ""))
            texto = f"(p. {alvo})" if alvo else ""
            for r in pg.search_for(f"(p. {cod})"):
                pg.add_redact_annot(r, text=texto, fontname="helv", fontsize=9, text_color=(0.2, 0.25, 0.3),
                                    fill=False, align=pymupdf.TEXT_ALIGN_LEFT)
        if achados:
            pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)


def html_folha(mes_ano: str, paginas_anexo: int | None = None) -> str:
    linhas, grupo_atual = [], None
    for grupo, titulo, slug in PAGINAS:
        if not (eh_ficha(slug) or grupo == "Governança"):
            continue
        if grupo == "Governança":
            if grupo_atual == grupo:
                continue
            titulo = "Governança (as 6 páginas)"
        if grupo != grupo_atual:
            linhas.append(f'<tr class="g"><td colspan="3">{grupo}</td></tr>')
            grupo_atual = grupo
        linhas.append(f'<tr><td>{titulo}</td><td class="v">v1.0 · {mes_ano}</td><td class="c"></td></tr>')
    linhas.append('<tr class="g"><td colspan="3">Anexo</td></tr>')
    nome_anexo = "Anexo A: Manual Operacional da Filial IV" + (f" ({paginas_anexo} páginas)" if paginas_anexo else "")
    linhas.append(f'<tr><td>{nome_anexo}</td>'
                  f'<td class="v">v1.0 · {mes_ano}</td><td class="c"></td></tr>')
    return f"""<!doctype html><html lang="pt-BR"><meta charset="utf-8"><style>
@page {{ size: A4; margin: 14mm 18mm }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1f2937; margin: 0; font-size: 9.5pt }}
h2 {{ color: #14532d; font-size: 18pt; margin: 0 0 2mm }}
p {{ margin: 0 0 3mm; line-height: 1.45 }}
table {{ width: 100%; border-collapse: collapse; margin-top: 3mm }}
td {{ padding: 0.45mm 2mm; border-bottom: 1px solid #e2e8f0 }}
th {{ text-align: left; background: #f1f5f9; padding: 1.5mm 2mm; font-size: 8.5pt; text-transform: uppercase; color: #475569 }}
tr.g td {{ background: #ecfdf5; color: #15803d; font-weight: 700; font-size: 8.5pt; text-transform: uppercase }}
td.v {{ width: 34mm; color: #475569 }} td.c {{ width: 40mm; border-bottom: 1px solid #94a3b8 }}
.ass {{ display: flex; gap: 14mm; margin-top: 6mm; break-inside: avoid }}
.ass div {{ flex: 1; text-align: center; font-size: 9pt }}
.ass i {{ display: block; border-top: 1px solid #1f2937; margin-bottom: 1.5mm }}
.ass span {{ color: #475569; font-size: 8pt }}
.loc {{ margin-top: 5mm; font-size: 9pt }}
</style>
<h2>Folha de validação</h2>
<p>Registra a ciência e a validação das fichas, das páginas de governança e do anexo do Manual de Sistemas da Cooperacre (Matriz e Filial IV), na versão e no mês indicados.
O manual é digital e é atualizado conforme os sistemas mudam; esta folha amarra a assinatura à versão de cada ficha listada abaixo.
Cada ficha é informativa e retrata o sistema como foi conferido nesta edição; ela pode ser atualizada sem alterar esta validação.
Um sistema novo, ou uma mudança de finalidade, de responsável ou de situação, gera um adendo ou uma nova validação.</p>
<table><tr><th>Item</th><th>Versão da ficha</th><th>Ciência (rubrica)</th></tr>{''.join(linhas)}</table>
<p class="loc">Local: ______________________________ &nbsp;&nbsp; Data: ____ / ____ / ________</p>
<div class="ass"><div><i></i><b>Edinar</b><br><span>Gerente administrativa</span></div>
<div><i></i><b>Lucas Castro</b><br><span>T.I., responsável técnico</span></div></div>
<p style="margin-top:3mm;font-size:8pt;color:#64748b">Emitida em duas vias de igual teor: uma para a gestão e uma para o responsável técnico.</p>
</html>"""


def gerar_folha(destino: Path, mes_ano: str) -> None:
    """PDF avulso só com a Folha de validação (o que a gestão assina; o manual em si fica digital)."""
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        html = Path(tmp) / "folha.html"
        html.write_text(html_folha(mes_ano), encoding="utf-8")
        imprimir(html.as_uri(), destino)
    doc = pymupdf.open(destino)
    limpar_parte(doc)
    doc.set_metadata({"title": "Folha de validação do Manual de Sistemas da Cooperacre",
                      "author": "Lucas Castro, T.I. da Cooperacre"})
    out = destino.with_suffix(".tmp.pdf")
    doc.save(out, garbage=3, deflate=True)
    n = len(doc)
    doc.close()
    out.replace(destino)
    print(f"OK: {destino} ({n} páginas)")


def gerar_protocolos(docs: list[pymupdf.Document], destino: Path) -> None:
    """PDF só com os protocolos de registro (uma página por sistema), cada um em duas vias, para assinar."""
    saida = pymupdf.open()
    toc = []
    for (grupo, titulo, slug, site), doc in zip(ITENS, docs):
        if site != "hub":
            continue
        for pg in doc:
            if "Protocolo de registro do sistema" not in pg.get_text():
                continue
            for via, rotulo in ((1, "1ª via: gestão"), (2, "2ª via: responsável técnico")):
                saida.insert_pdf(doc, from_page=pg.number, to_page=pg.number)
                nova = saida[-1]
                nova.insert_text((nova.rect.width - 150, nova.rect.height - 22), rotulo, fontsize=8, fontname="helv",
                                 color=(0.4, 0.45, 0.5))
                if via == 1:
                    toc.append([1, f"{titulo}", len(saida)])
    saida.set_toc(toc)
    saida.set_metadata({"title": "Protocolos de registro de sistemas da Cooperacre (2 vias)",
                        "author": "Lucas Castro, T.I. da Cooperacre"})
    saida.save(destino, garbage=3, deflate=True)
    print(f"OK: {destino} ({len(saida)} páginas, {len(toc)} protocolos em 2 vias)")


def gerar(modo: str, destino: Path, mes_ano: str, versao: str) -> None:
    sufixo = "?pdf&sem-protocolo" if modo == "leitura" else "?pdf"
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = Path(tmp)
        docs = []
        for i, (_, titulo, slug, site) in enumerate(ITENS):
            alvo = tmp / f"{i:02d}.pdf"
            imprimir(f"http://127.0.0.1:{PORTAS[site]}/{slug}/{sufixo}", alvo)
            doc = pymupdf.open(alvo)
            limpar_parte(doc)
            docs.append(doc)
            print(f"[{modo} {i + 1}/{len(ITENS)}] {titulo}")
        if modo == "completo":
            gerar_protocolos(docs, SAIDA / "protocolos-2-vias.pdf")
        contagens = [len(d) for d in docs]
        paginas_anexo = sum(c for c, it in zip(contagens, ITENS) if it[3] == "anexo")

        n_frente = 2
        for _ in range(3):
            inicios, atual = [], n_frente + 1
            for c in contagens:
                inicios.append(atual)
                atual += c
            html = tmp / "frente.html"
            html.write_text(html_capa_sumario(inicios, versao, atual if modo == "leitura" else None), encoding="utf-8")
            frente = tmp / "frente.pdf"
            imprimir(html.as_uri(), frente)
            n_real = len(pymupdf.open(frente))
            if n_real == n_frente:
                break
            n_frente = n_real

        final = pymupdf.open(frente)
        toc, pagina_de = [], {}
        for (grupo, titulo, slug, site), doc, ini in zip(ITENS, docs, inicios):
            final.insert_pdf(doc)
            toc.append([1, f"{grupo}: {titulo}" if site == "hub" else f"Anexo A: {titulo}", ini])
            pagina_de[chave_de(site, slug)] = ini
        if modo == "leitura":
            html = tmp / "folha.html"
            html.write_text(html_folha(mes_ano, paginas_anexo), encoding="utf-8")
            folha = tmp / "folha.pdf"
            imprimir(html.as_uri(), folha)
            toc.append([1, "Folha de validação", len(final) + 1])
            final.insert_pdf(pymupdf.open(folha))

        codigos = {codigo(k): k for k in pagina_de}
        # outros destinos (ex.: modelo de ficha) caem em códigos sem página e a referência é apagada
        assert len(codigos) == len(pagina_de), "colisão de códigos de página"
        resolver_referencias(final, pagina_de, codigos)

        total = len(final)
        for n in range(1, total):
            pg = final[n]
            pg.insert_text((pg.rect.width / 2 - 8, pg.rect.height - 16), f"{n + 1} / {total}",
                           fontsize=8, color=(0.4, 0.45, 0.5))
        final.set_toc(toc)
        final.set_metadata({"title": "Manual de Sistemas da Cooperacre (Matriz e Filial IV)",
                            "author": "Lucas Castro, T.I. da Cooperacre"})
        # Imagens a 130 dpi (de ~68 MB para ~13 MB): o PDF é baixado pelo site e o texto não é afetado
        final.rewrite_images(dpi_threshold=170, dpi_target=130, quality=72)
        final.save(destino, garbage=4, deflate=True)
        print(f"OK: {destino} ({total} páginas)")


def servir(pasta: Path, porta: int) -> http.server.ThreadingHTTPServer:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(pasta))
    handler.log_message = lambda *a, **k: None
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", porta), handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor


def main() -> None:
    SAIDA.mkdir(exist_ok=True)
    hoje = date.today()
    mes_ano = f"{MESES[hoje.month - 1][:3]}/{hoje.year}"
    versao = f"Edição 1 · {MESES[hoje.month - 1].capitalize()} de {hoje.year} · versão para leitura e revisão"
    gerar_folha(SAIDA / "folha-de-validacao.pdf", mes_ano)
    if "--so-folha" in sys.argv:
        return
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp_anexo:
        construir_anexo(Path(tmp_anexo) / "dist")
        servidores = [servir(DIST, PORTAS["hub"]), servir(Path(tmp_anexo) / "dist", PORTAS["anexo"])]
        gerar("completo", SAIDA / "manual-sistemas-matriz.pdf", mes_ano, versao)
        gerar("leitura", SAIDA / "manual-sistemas-leitura.pdf", mes_ano, versao)
        for s in servidores:
            s.shutdown()


if __name__ == "__main__":
    main()
