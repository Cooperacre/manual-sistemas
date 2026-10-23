# CHANGELOG

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/). Versionamento: [SemVer](https://semver.org/lang/pt-BR/) (MAJOR.MINOR.PATCH).

O número atual vive em `package.json` (`version`, hoje 0.1.0).

## [Não lançado]

### Adicionado
- `GOVERNANCA.md` (padrão Cooperacre v1.0) e este changelog. O histórico anterior a 2026-10-20 está no git.

### Alterado
- Padrão Cooperacre v1.1 (`modelos/GOVERNANCA.md` e página Mudanças e versionamento): seção `### Implantação` no changelog quando publicar não basta (o que fazer e como desfazer); versão `0.x` até a entrada oficial em produção, que é a `1.0.0`; cada sistema documenta onde testa sem expor nem alterar dado real; como ler o resultado do `gitleaks dir`.
- `CLAUDE.md` (guia de manutenção para quem desenvolve e para a IA) passa a ser versionado; notas só da máquina local ficam em `CLAUDE.local.md`, fora do git.
- Padrão Cooperacre v1.2 (`modelos/GOVERNANCA.md`, `modelos/gitignore-base` e páginas Mudanças e versionamento e Desenvolvimento com IA): seção Organização do repositório, com raiz limpa, pastas gerais em inglês e regra de negócio em português, testes em `tests/`, dados reais em `local/` (fora do git), `CLAUDE.md` enxuto com o que é local em `CLAUDE.local.md`, e o PRD apagado na entrega, com o que vale passando para `docs/`. Vale para projeto novo e reorganização planejada; projeto em uso não renomeia pasta só por isso.
