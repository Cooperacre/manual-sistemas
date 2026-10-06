"""Mockups do CooperFlow para o manual. SOMENTE LEITURA (login + navegacao por links).
Antes de cada captura, um sanitizador troca na propria pagina clientes, vendedores, numeros de pedido e
valores por dados ficticios. A senha do gestor vem de variavel de ambiente (nao fica em arquivo)."""
import os, re
from playwright.sync_api import sync_playwright

BASE = "https://cooperflow.netlify.app"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flow2")
os.makedirs(OUT, exist_ok=True)

creds = {}
for linha in open(r"C:\xampp\htdocs\cooperflow\CLAUDE.md", encoding="utf-8"):
    m = re.match(r"\|\s*`([^`]+)`\s*\|\s*`([^`]+)`", linha)
    if m:
        creds[m.group(1)] = m.group(2)
creds[os.environ["FLOW_GESTOR_USER"]] = os.environ["FLOW_GESTOR_PW"]

SANITIZE_JS = r"""
() => {
  const empresas = ["Mercado Bom Preço","Padaria Estrela do Norte","Restaurante Sabor da Terra","Sorveteria Polar","Lanchonete Central",
    "Mercearia Nova Era","Empório Verde Vida","Cantina do Sol","Supermercado Boa Compra","Bar e Petiscaria do Largo",
    "Hotel Rio Acre","Cafeteria Grão Nobre","Minimercado São José","Casa de Sucos Tropical","Rede Fresca Alimentos","Distribuidora Aurora"];
  const pessoas = ["Carla Mendes","Rafael Costa","Mariana Alves","Bruno Lima","Helena Prado","Diego Nunes"];
  const UI = new Set(["PEDIDO","CLIENTE","VENDEDOR","VALOR","STATUS","DATA","PRAZO","AÇÕES","TOTAL","SAÍDA","MOTORISTA","PROTOCOLO","ITENS","PRODUTO","QUANTIDADE","AGUARDANDO CONFIRMAÇÃO","RECEBIDO","EM SEPARAÇÃO","SEPARADO","HOJE","AMANHÃ","FUTURA","SEM DATA","SEPARADOS","OK","PDF","CF","ERP","CFOP","NF","CNPJ"]);
  const h = s => { let x = 7; for (const c of s) x = (x * 31 + c.charCodeAt(0)) >>> 0; return x; };
  const w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
  for (const n of nodes) {
    const orig = n.nodeValue; if (!orig || !orig.trim()) continue;
    let t = orig;
    t = t.replace(/Lucas \(teste motorista\)/g, "Carlos Almeida").replace(/Lucas Camara Fria/g, "Marcos Silva").replace(/K[áa]ssio/g, "Renata Gomes");
    t = t.replace(/R\$\s*[\d.]+,\d{2}/g, m => "R$ " + (180 + (h(m) % 2800) + (h(m + "c") % 100) / 100).toLocaleString("pt-BR", {minimumFractionDigits: 2, maximumFractionDigits: 2}));
    t = t.replace(/\b1[0-9]{5}\b/g, m => String(140000 + (h(m) % 9000)));
    t = t.replace(/(\d{1,3}) - ([A-ZÀ-Ú][A-ZÀ-Ú .]{3,})/g, (m, num) => num + " - " + pessoas[h(m) % pessoas.length].toUpperCase());
    const tr = t.trim();
    if (!/^\d{1,3} - /.test(tr) && /^[A-ZÀ-Ú0-9&.,\-'\/ ]{5,}$/.test(tr) && /[A-ZÀ-Ú]{3}/.test(tr) && !/^(R\$|CF-)/.test(tr) && !/^[\d\/ .,:-]+$/.test(tr) && !UI.has(tr)) {
      t = t.replace(tr, empresas[h(tr) % empresas.length]);
    }
    if (t !== orig) n.nodeValue = t;
  }
  // passe por estrutura: elementos folha com a mesma classe de um nome ja mascarado (pega nomes em caixa mista)
  const seletores = new Set();
  document.querySelectorAll("*").forEach(e => {
    if (e.children.length === 0 && e.classList.length && empresas.includes(e.textContent.trim()))
      seletores.add(e.tagName.toLowerCase() + "." + [...e.classList].join("."));
  });
  // tabelas: tratamento por coluna (pelo cabecalho), preservando motivo/status
  document.querySelectorAll("table").forEach(tb => {
    const heads = [...tb.querySelectorAll("thead th")].map(th => th.textContent.trim().toLowerCase());
    tb.querySelectorAll("tbody tr").forEach((tr, ri) => {
      const tds = tr.querySelectorAll("td");
      heads.forEach((hd, i) => {
        const td = tds[i]; if (!td || td.children.length) return;
        if (hd === "cliente") td.textContent = empresas[(ri * 3 + 1) % empresas.length];
        else if (hd === "vendedor") td.textContent = (11 + (ri % 4)) + " - " + pessoas[(ri + 1) % pessoas.length].toUpperCase();
        else if (hd === "motorista") td.textContent = "Carlos Almeida";
      });
    });
  });
  // remove o selo do Netlify (plano gratuito)
  [...document.querySelectorAll("*")].filter(e => e.children.length <= 3 && e.textContent.trim() === "Powered by Netlify").forEach(e => {
    let p = e; while (p.parentElement && p.parentElement !== document.body && getComputedStyle(p).position !== "fixed") p = p.parentElement;
    if (p !== document.body) p.remove();
  });
  seletores.forEach(sel => document.querySelectorAll(sel).forEach(x => {
    if (x.children.length || x.closest("table")) return;
    const tx = x.textContent.trim();
    if (tx.length >= 3 && !empresas.includes(tx) && !pessoas.includes(tx) && !UI.has(tx.toUpperCase()) && !/^(R\$|CF-)/.test(tx) && !/^[\d\/ .,:-]+$/.test(tx)
        && !/^(entregue|não entregue|nao entregue|em rota|aguardando|recebido|na câmara|separado|recebida)/i.test(tx))
      x.textContent = empresas[h(tx) % empresas.length];
  }));
}
"""

PERFIS = [
    (os.environ["FLOW_GESTOR_USER"], "gestor", (1440, 900), False),
    ("lucas-camarafria", "camara-fria", (1440, 900), False),
    ("lucas-motorista", "motorista", (390, 844), True),
]

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    for user, nome, vp, mobile in PERFIS:
        ctx = browser.new_context(viewport={"width": vp[0], "height": vp[1]}, device_scale_factor=2 if mobile else 1,
                                  is_mobile=mobile, has_touch=mobile, locale="pt-BR")
        pg = ctx.new_page()
        pg.goto(BASE + "/login"); pg.wait_for_load_state("networkidle")
        pg.locator("input:not([type=password]):not([type=hidden]):not([type=checkbox])").first.fill(user)
        pg.locator("input[type=password]").fill(creds[user])
        pg.get_by_role("button", name=re.compile("entrar", re.I)).click()
        pg.wait_for_timeout(3500); pg.wait_for_load_state("networkidle")
        print(f"[{nome}] apos login: {pg.url.replace(BASE, '')}")
        if "/login" in pg.url or "trocar-senha" in pg.url:
            print(f"[{nome}] nao entrou ou exige troca de senha; pulando (nao vou trocar senha)")
            ctx.close(); continue

        def shot(rotulo):
            pg.wait_for_timeout(1200)
            pg.evaluate(SANITIZE_JS); pg.wait_for_timeout(250)
            pg.screenshot(path=os.path.join(OUT, f"{nome}-{rotulo}.png"))

        shot("inicio")
        links = pg.eval_on_selector_all("a[data-link], nav a, header a", "els=>[...new Set(els.map(e=>e.pathname).filter(Boolean))]")
        links = [l for l in links if not re.search(r"sair|logout|usuarios", l) and l not in ("/", "")]
        print(f"[{nome}] rotas: {links}")
        for path in links[:8]:
            pg.goto(BASE + path); pg.wait_for_load_state("networkidle")
            shot(re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-"))
            print("   ok", path)
        if nome == "gestor":
            for path in ["/calendario", "/documentacao"]:
                pg.goto(BASE + path); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(800)
                if "encontrada" in pg.inner_text("body").lower():
                    print("   (nao existe)", path); continue
                shot(re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-"))
                print("   ok", path)
        ctx.close()
    browser.close()
print("fim")
