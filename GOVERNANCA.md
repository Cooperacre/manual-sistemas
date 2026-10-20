# Governança

> **Padrão Cooperacre v1.1 (2026-10-20).** Cópia do modelo mantido em
> `Cooperacre/manual-sistemas`, pasta `modelos/`. Não editar aqui: mudança no
> padrão é feita no modelo e copiada para todos os projetos. O que é
> específico deste sistema (como publicar, onde ficam as credenciais, o banco)
> fica no `CLAUDE.md` e no `README.md`.

Regras que todo sistema da Cooperacre segue, resumidas da seção Governança do
[Manual de Sistemas](https://sistemascooperacre.netlify.app/governanca/principios/).
Valem para quem desenvolve e para assistentes de IA.

## Mudanças

- A alteração é feita e testada na cópia de trabalho (a máquina de quem
  desenvolve), nunca direto no ambiente em uso.
- Cada sistema diz no `CLAUDE.md` (ou no `README.md`) onde as mudanças são
  testadas: num banco de teste próprio ou, quando só existe o de produção,
  como testar sem expor nem alterar dado real (registros fictícios
  identificáveis, apagados ao fim do teste).
- Antes de enviar para a branch principal, o responsável técnico confere o
  que mudou. O plano gratuito do GitHub não protege a branch de repositório
  privado: essa proteção vale como regra de trabalho.
- Antes de publicar, fica claro como voltar à última versão estável,
  principalmente quando a mudança mexe em dados.
- Reescrever o histórico do git, apagar dados ou mudar a estrutura do banco
  só acontece com cópia de segurança feita e com a confirmação de que ninguém
  está editando ao mesmo tempo.

## Histórico de mudanças (CHANGELOG)

- `CHANGELOG.md` na raiz, um só por repositório, atualizado **antes do
  commit** de cada entrega. Ele alimenta a ficha do sistema no manual.
- Formato [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/) em
  português, com as seções Adicionado, Alterado, Corrigido e Removido (só as
  que tiverem item).
- Versão [SemVer](https://semver.org/lang/pt-BR/): MAJOR quando muda o jeito
  de usar, rodar ou publicar; MINOR para funcionalidade nova; PATCH para
  correção. Quando o projeto tem número de versão no código (`package.json`,
  `versao.py`), ele acompanha o changelog.
- Data absoluta (AAAA-MM-DD). Cada item diz primeiro o que muda para quem
  usa, depois o detalhe técnico, se precisar. Projeto com vários módulos:
  cada item diz o módulo.
- O que ainda não foi publicado fica em `## [Não lançado]`.
- Quando publicar a versão exige mais do que publicar o código (migração de
  banco, variável de ambiente nova, outro sistema a atualizar, ação manual,
  dado alterado sem volta), a versão ganha a seção `### Implantação`: o que
  fazer para implantar e como desfazer. Fora desses casos, a seção não
  aparece; desfazer é voltar o código e publicar de novo.
- Enquanto o sistema não entra oficialmente em produção (usuários reais no
  dia a dia e testes de aceite encerrados), a versão fica em `0.x`. A entrada
  oficial em produção é a `1.0.0`.

## Credenciais e dados

- Nenhuma senha, chave ou token no código, em exemplo, em print ou em
  conversa com IA. Ficam em arquivo de configuração fora do git (`.env` ou
  equivalente); o repositório traz só o modelo com os nomes, nunca os valores.
- O `.gitignore` cobre arquivos de configuração local, chaves e cópias de
  banco.
- Antes de enviar ao repositório, roda-se a verificação de segredos
  (`gitleaks git` e `gitleaks dir`). Se algo sensível já tiver entrado, o
  histórico é refeito antes da publicação e a credencial é trocada. O
  `gitleaks dir` lê também arquivos fora do git: acusar o `.env` local é
  esperado. Pede ação o achado no `gitleaks git` ou em arquivo versionado.
- Dados reais (clientes, valores, nomes de colegas) não vão para exemplos,
  testes versionados, documentação nem prints. Usam-se dados fictícios.

## Assistentes de IA

- A IA ajuda a construir; uma pessoa responde pelo resultado. Código feito
  com IA passa pelos mesmos testes e pela mesma conferência.
- Não publicar em produção, não enviar ao repositório e não rodar deploy sem
  pedido explícito.
- Não apagar dados nem rodar migração ou script destrutivo sem análise e sem
  confirmação de quem é responsável.
- Ação em produção que exige credencial fica com a pessoa responsável.
- Pedido crítico começa por um plano: o que muda, o que é afetado, os riscos,
  como testar e como reverter.
- O sistema em funcionamento roda por regras fixas: a IA não decide sobre os
  dados de produção. Se um dia isso mudar, é exceção declarada na ficha do
  manual.

## Documentação

- `README.md` termina com o rodapé padrão que aponta para o Manual de
  Sistemas.
- Mudança que altera o que a ficha do manual diz (o que o sistema faz, quem
  usa, stack, hospedagem, banco, como atualizar) é avisada para a ficha ser
  atualizada.
- Repositório na organização Cooperacre no GitHub; serviços em nome do e-mail
  institucional sempre que a plataforma permitir, com conta individual para
  cada pessoa.
