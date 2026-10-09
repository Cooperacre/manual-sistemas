"""Gera o PDF único do manual (capa, sumário, fichas na ordem do menu e governança).

Uso (na raiz do projeto, com `npm run build` já feito e o dev server fechado):
    python tools/gerar_pdf.py

Cada página do `dist/` vira um PDF pelo Edge sem janela; depois o PyMuPDF junta tudo
e cria os marcadores. Saída: pdf/manual-sistemas-matriz.pdf
"""
import functools
import http.server
import re
import subprocess
import tempfile
import threading
from datetime import date
from pathlib import Path

import pymupdf

RAIZ = Path(__file__).resolve().parent.parent
DIST = RAIZ / "dist"
SAIDA = RAIZ / "pdf"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORTA = 4399
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


def imprimir(url: str, destino: Path) -> None:
    subprocess.run(
        [EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=15000", f"--print-to-pdf={destino}", url],
        check=True, capture_output=True, timeout=180,
    )


def html_capa_sumario(inicios: list[int], versao: str) -> str:
    linhas, grupo_atual = [], None
    for (grupo, titulo, _), pag in zip(PAGINAS, inicios):
        if grupo != grupo_atual:
            linhas.append(f'<h3>{grupo}</h3>')
            grupo_atual = grupo
        linhas.append(f'<div class="l"><span>{titulo}</span><i></i><b>{pag}</b></div>')
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


def main() -> None:
    SAIDA.mkdir(exist_ok=True)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
    handler.log_message = lambda *a, **k: None
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", PORTA), handler)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()

    hoje = date.today()
    versao = f"{MESES[hoje.month - 1].capitalize()} de {hoje.year} · versão para leitura e revisão"

    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        tmp = Path(tmp)
        partes = []
        for i, (_, titulo, slug) in enumerate(PAGINAS):
            alvo = tmp / f"{i:02d}.pdf"
            imprimir(f"http://127.0.0.1:{PORTA}/{slug}/", alvo)
            partes.append(alvo)
            print(f"[{i + 1}/{len(PAGINAS)}] {titulo}")

        contagens = [len(pymupdf.open(p)) for p in partes]

        # capa + sumário: descobre quantas páginas ocupam e recalcula os inícios
        n_frente = 2
        for _ in range(2):
            inicios, atual = [], n_frente + 1
            for c in contagens:
                inicios.append(atual)
                atual += c
            html = tmp / "frente.html"
            html.write_text(html_capa_sumario(inicios, versao), encoding="utf-8")
            frente = tmp / "frente.pdf"
            imprimir(html.as_uri(), frente)
            n_real = len(pymupdf.open(frente))
            if n_real == n_frente:
                break
            n_frente = n_real

        final = pymupdf.open(frente)
        toc = []
        for (grupo, titulo, _), parte, ini in zip(PAGINAS, partes, inicios):
            doc = pymupdf.open(parte)
            final.insert_pdf(doc)
            toc.append([1, f"{grupo}: {titulo}", ini])

        # numeração no rodapé (a partir do sumário)
        total = len(final)
        for n in range(1, total):
            pg = final[n]
            pg.insert_text((pg.rect.width / 2 - 8, pg.rect.height - 16), f"{n + 1} / {total}",
                           fontsize=8, color=(0.4, 0.45, 0.5))
        final.set_toc(toc)
        final.set_metadata({"title": "Manual de Sistemas da Cooperacre (Matriz e Filial IV)",
                            "author": "Lucas Castro, T.I. da Cooperacre"})
        destino = SAIDA / "manual-sistemas-matriz.pdf"
        final.save(destino, garbage=3, deflate=True)
        print(f"\nOK: {destino} ({total} páginas)")
    servidor.shutdown()


if __name__ == "__main__":
    main()
