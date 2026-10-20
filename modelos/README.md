# Modelos de governança

Arquivos-padrão copiados para todos os repositórios da Cooperacre. Esta pasta é
a fonte única: mudança no padrão é feita aqui, sobe a versão no cabeçalho do
`GOVERNANCA.md` e é copiada para cada projeto. Não faz parte do site.

| Arquivo | Vai para o projeto como | Observação |
|---|---|---|
| `GOVERNANCA.md` | `GOVERNANCA.md` (versionado) | Copiado inteiro, sem editar no projeto. |
| `CHANGELOG.md` | `CHANGELOG.md` | Só quando o projeto ainda não tem; depois é mantido no projeto. |
| `rodape-readme.md` | fim do `README.md` | Igual em todos os projetos. |

No `CLAUDE.md` de cada projeto, logo abaixo do título, entra a linha que faz o
Claude Code carregar as regras comuns:

```
Regras comuns da Cooperacre (mudanças, changelog, credenciais, IA): @GOVERNANCA.md
```
