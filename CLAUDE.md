# Cooperacre Sistemas — hub central de projetos (PRD em construção)

Regras comuns da Cooperacre (mudanças, changelog, credenciais, IA): @GOVERNANCA.md

## Como retomar (leia primeiro)

O estado atual, o que já foi feito e as tarefas pendentes estão em [`TODO.md`](TODO.md). Comandos:
`npm run dev` (site em localhost:4321). As fichas em `src/content/docs/catalogo/` são editadas à mão (fonte única);
os scripts que geraram as fichas iniciais estão aposentados em `tools/_arquivo/` e **não devem ser rodados** (sobrescreveriam as edições).

## Problema que este projeto resolve

Lucas (matriz, T.I.) desenvolveu e vem desenvolvendo dezenas de sistemas,
painéis e planilhas para a Cooperacre, cada um numa pasta separada em
`c:\xampp\htdocs\`, sem centralização. Foi solicitada uma consolidação:
o que foi feito, quem pediu, pra que serve, onde está hospedado, onde está
o banco, como os dados são atualizados. Este projeto é essa centralização.

## Objetivo estratégico do manual (atualizado em 27/09/2026)

> O modelo visual das fichas (cartões, selos, paleta) está **provisório**: o front será repensado. O conteúdo
> das fichas continua sendo escrito agora, e a apresentação é aplicada depois.

Além de documentar, o manual **mostra o que o T.I. já entrega e o que consegue entregar**. O público-alvo é o
superintendente e a administração. O que se quer que eles concluam está no `CLAUDE.local.md` (fora do git).

**Tom de voz:** confiante, promocional e orientado a benefício. Abrir com o valor entregue (o que muda para quem
usa), destacar o que há de mais sofisticado, usar números quando existirem (horas economizadas, erros evitados,
volume tratado) e mostrar ambição com uma seção "o que esta base permite fazer a seguir".

**Leitor não técnico (regra de escrita):** a maioria dos leitores não é técnica. Todo termo técnico ou sigla
aparece com uma explicação curta e concreta, no próprio texto, e depois entra no glossário. Traduzir para o que muda
na prática, e isso também impressiona: por exemplo, **PWA** vira "aplicativo para celular que se instala direto pelo
navegador, sem loja de aplicativos"; **hash de integridade** vira "selo que prova que o conteúdo não foi alterado".
O glossário (`src/content/docs/glossario.md`) será ampliado no fim, com todas as fichas fechadas, incluindo MVP, PWA,
vibe coding, programação assistida por IA, automação, backend e front-end, entre outros.

**Padrão visual (preferências do Lucas):** selos e etiquetas com texto **centralizado**, em **negrito**, fonte
**arredondada** (Nunito), **padding interno generoso** e formato de pílula; nunca alinhados à direita nem em fonte
monoespaçada. Cores por **papéis fixos**, em tons modernos (faixa 600 a 700 de Tailwind/Bootstrap, nunca o azul puro de alto
contraste): sucesso #047857, informação #2563eb, destaque/novidade #7c3aed, atenção #f59e0b (amarelo com texto escuro,
é a cor padrão de atenção), perigo #e11d48, neutro #475569. Letra branca sobre a cor (exceto o amarelo). As variáveis
estão em `src/styles/custom.css` (`--cx-*`). Cuidar sempre do
alinhamento e da orientação dos elementos (o estilo está em `src/styles/custom.css`, classe `.selos`).

**Uma única linha que não se cruza:** o tom pode ser forte, mas **cada afirmação tem de ser verdadeira e verificável**.
Não dizer que algo está em uso quando não está, não prometer o que o sistema não faz, não atacar fornecedores nem
comparar preços no manual. O motivo é prático: os leitores decidem com base no texto, e uma frase que não se
sustenta gasta a credibilidade que o manual quer construir. Ambição vai marcada como proposta, e o que funciona
pode ser dito com toda a força.

**Recursos de apresentação (a aplicar nas fichas):**
- Selo de estágio em cada sistema: **Em uso**, **Pronto para uso** ou **Em desenvolvimento**
- Linha do tempo: data do pedido, data da entrega, estado atual, o que falta para começar a usar e quem decide
- Números de resultado quando houver (ex.: Contábil, de duas semanas por conta para dois dias)
- Página "O que esta base permite fazer a seguir" (propostas, marcadas como tal)

**Duas entregas diferentes, com propósitos diferentes:**

1. **Hub web** (catálogo vivo, cresce a cada projeto novo) — nível "README
   honesto": arquitetura, stack, onde roda, como atualizar, em alto nível.
   Não expõe lógica de negócio fina, queries sensíveis nem decisões de
   design mais delicadas — é documentação de manutenção, não o código-fonte
   explicado linha a linha.
2. **Protocolo impresso** (documento formal, não técnico) — gerado *sempre
   que um projeto novo for formalizado*, para assinatura da gestora e do
   Lucas, em 2 vias. Registra oficialmente que aquele sistema existe, pra
   que serve e quem é responsável.

## Status

- **E-mail dedicado: `sistemascooperacre@gmail.com`** (fechado em 24/09/2026).
  Usar esse e-mail para a conta GitHub/Netlify deste projeto daqui pra
  frente.
- **Escopo confirmado em 24/09/2026:** lista de 26 pastas (11 sistemas mais a página da Filial IV, após as remoções) em
  [`inventario.md`](inventario.md). Vários projetos do `htdocs` não são da
  Cooperacre e ficam de fora.
- **Contas e propriedade:** os arquivos (planilhas e demais recursos) serão
  compartilhados com o e-mail de sistemas. A chave da conta de serviço
  Google continua sendo do Lucas: quem um dia precisar mexer cria a sua e
  autoriza na planilha. Nem todo projeto depende dessa chave, então a
  documentação não deve tratá-la como requisito geral.
- **ERP atual (Firebird):** existe só até a migração prevista para
  01/01/2027 (go live do TOTVS, confirmado). Vários projetos podem ser descontinuados por
  causa disso. Cada ficha terá o campo "Vida útil" (ver `inventario.md`),
  com comentário genérico quando não der para determinar.
- **Como descrever o `meta-pipeline`:** a descrição deve ser verdadeira:
  uma API/script de extração com usuário de banco **somente leitura**
  (podendo ganhar nome como "Meta API"). Antes de escrever isso, confirmar
  na prática que ele usa esse usuário e que uma tentativa de escrita
  falha, e que o SYSDBA não é mais usado pelo pipeline. Não documentar
  nada que não seja verdade.
- Nome final da pasta/hub (atual: `cooperacre-sistemas`, provisório).
- **Hub criado (24/09/2026):** Astro + Starlight na raiz deste projeto,
  reaproveitando o setup do [cooperacre4-manual](../cooperacre4-manual/CLAUDE.md)
  (mesma identidade visual verde). Conteúdo em `src/content/docs/`
  (intro, glossário, catálogo, governança), tudo marcado como rascunho.
  Comandos: `npm run dev` (localhost:4321), `npm run build`. Repositório no
  GitHub (`https://github.com/Cooperacre/manual-sistemas`, organização Cooperacre) e hospedado no Netlify
  (`https://sistemascooperacre.netlify.app/`). Falta decidir a visibilidade
  (site público x protegido por senha).
  `inventario.md` e `protocolos/` ficam fora do site.
- **Link atual do hub (deploy): https://sistemascooperacre.netlify.app/** (definido em 09/10/2026), com repositório em
  `https://github.com/Cooperacre/manual-sistemas`.
- Aviso: o Node local é 22.17 e o Astro pede >= 22.19. Funciona, mas
  atualizar quando possível.

## Peça 1 — Hub web

**Stack planejada:** Astro + Starlight, igual ao `cooperacre4-manual` (já
validado, deploy automático Netlify + GitHub). Reaproveitar o padrão em vez
de inventar um novo.

**Cada projeto do catálogo ganha uma página com duas partes:**

- **Parte não técnica** (pra qualquer pessoa, inclusive gestão):
  - Nome do sistema e uma frase do que ele faz
  - Quem solicitou / para qual área ou finalidade
  - Situação: em produção / uso interno / descontinuado
- **Parte técnica** ("README honesto", nível manutenção):
  - Stack (linguagem, framework)
  - Onde está hospedado (Netlify, host da intranet via Tailscale, etc.)
  - Onde está o banco de dados e qual é (Firebird, SQLite, planilha Google,
    MySQL...)
  - Como os dados entram/saem (pipeline, API, importação manual)
  - Como atualizar (deploy automático via `_infra`? manual? outro fluxo?)
  - Link do repositório (quando existir)

**Regra de conteúdo:** verdadeiro em todas as camadas, com o nível de detalhe
ajustado ao público e o tom de voz do objetivo estratégico acima. A parte não técnica resume sem assustar; a parte
técnica traz o que uma pessoa qualificada precisa para manter e dar
continuidade (onde roda, onde está o banco, como atualizar). Nunca
credenciais, nunca descrição diferente do que o sistema realmente faz. O
controle sobre quem altera vem de permissões técnicas (acessos, proteção do
`main`, processo de mudança), não de omitir informação.

## Peça 2 — Protocolo de criação de projeto (documento assinado)

Documento impresso, autocontido (HTML → PDF via impressão do navegador,
A4, mesmo padrão usado em `cooperacre-orcamento`), gerado a cada novo
projeto formalizado.

- **Numeração:** código por projeto, formato `PROJ-<NOME>-<ANO>`
  (ex.: `PROJ-COOPERFLOW-2026`).
- **Vias:** 2 — responsável técnico (Lucas) e gestora.
- **Conteúdo (não técnico, linguagem de gestão):**
  - Código do protocolo e data
  - Nome do projeto/sistema
  - Solicitante / área
  - Finalidade (o que resolve, em 1-2 frases)
  - Responsável técnico
  - Situação (novo / migração de planilha existente / substituição de X)
  - Duas linhas de assinatura (Lucas e gestora), com data e local

Template em [`protocolos/template/template-protocolo.html`](protocolos/template/template-protocolo.html).
Cada protocolo assinado deve virar uma pasta própria em `protocolos/`
(ex.: `protocolos/PROJ-COOPERFLOW-2026/`), guardando o HTML preenchido e o
PDF gerado — mesmo padrão de "pasta por item" usado em
`cooperacre-orcamento`.

## Padrão de nomes (decisão do Lucas, 24/09/2026)

- **Repositório e pasta com o mesmo nome**, em minúsculas, sem acento, sem
  separador, curto (uma ou duas palavras): `cooperflow`, `analisecomercial`.
- O nome legível ("Análise Comercial") vive no **nome de exibição** das
  fichas e documentos, separado do identificador técnico.
- Projetos existentes **não são renomeados localmente por enquanto**. Na
  transferência para a organização, o repo é renomeado para bater com a
  pasta (o GitHub redireciona o nome antigo). Os que já têm hífen ficam
  como estão.
- Referência: nas 40 maiores organizações do GitHub, 91,5% dos nomes
  compostos usam kebab-case, mas a escolha aqui é por consistência e
  simplicidade. O que evitar sempre: maiúsculas e acentos.

## Inventário de partida

Ver [`inventario.md`](inventario.md) — levantamento inicial de todas as
pastas em `htdocs` com sinal de relação com a Cooperacre (nome, se tem
README/CLAUDE.md, se tem repositório GitHub, sinais de Netlify/`.env`).
Serve de matéria-prima para popular o hub aos poucos; muitos itens ainda
não têm documentação nenhuma e precisam ser visitados um a um para
descobrir quem pediu, pra que serve e onde roda antes de ganharem página
no hub.

## Próximos passos (nesta ordem)

1. ~~Fechar e-mail dedicado~~ (feito: `sistemascooperacre@gmail.com`).
2. Criar conta GitHub com esse e-mail e decidir o nome final do
   hub/pasta/repo (pode manter `cooperacre-sistemas`).
3. Rodar o scaffold do hub (Astro + Starlight) só depois do passo 2,
   pra não ter que migrar remote/nome depois.
4. Ir preenchendo `inventario.md`: para cada projeto sem documentação,
   levantar quem pediu, finalidade, stack, hospedagem, banco — e só então
   criar a página no hub.
5. Ao formalizar um projeto novo (documentado no hub por completo), gerar
   o protocolo correspondente e colher as assinaturas.

## Regra do projeto

Este catálogo é sobre *onde as coisas estão e como mantê-las rodando*, não
sobre *como foram construídas por dentro*. Antes de escrever a parte
técnica de qualquer projeto no hub, confirmar com o Lucas o nível de
detalhe daquele projeto específico — alguns podem exigir mais reserva que
outros.
