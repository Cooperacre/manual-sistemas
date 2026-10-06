# Manual de Sistemas da Cooperacre

Catálogo vivo dos sistemas, planilhas e automações que a T.I. construiu para a Cooperacre: o que cada um faz, quem
pediu, em que estágio está e como é mantido. O site é feito com [Astro](https://astro.build) e
[Starlight](https://starlight.astro.build).

## Como rodar

```bash
npm install
npm run dev      # http://localhost:4321
npm run build    # gera dist/
```

Requer Node 22.19 ou superior.

## Onde editar

- `src/content/docs/catalogo/`: fichas dos sistemas (cada uma tem selo de estágio, linha do tempo e cartões).
- `src/content/docs/planilhas/` e `src/content/docs/automacoes/`: planilhas e automações.
- `src/content/docs/governanca/`: princípios de acesso, mudanças e uso de IA.
- `src/content/docs/glossario.md`: termos explicados em português simples.
- `src/styles/custom.css`: identidade visual. `astro.config.mjs`: menu e impressão das fichas.

As fichas são editadas à mão e são a fonte única do conteúdo. Antes de publicar prints, conferir se não há cliente,
vendedor, valor ou nome de colega real.

## Autoria

Lucas Castro, T.I. da Cooperacre ([LukystarWar](https://github.com/LukystarWar)).
