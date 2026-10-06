---
title: Desenvolvimento com IA
description: Onde a inteligência artificial entra no trabalho de T.I., onde não entra, e os cuidados para usá-la com segurança.
---

A inteligência artificial faz parte do jeito de trabalhar do T.I.: ajuda a construir mais rápido, desde o código até a arte e os textos. A regra que mantém isso seguro é simples: **a IA ajuda a construir, e uma pessoa responde pelo resultado.**

## Onde a IA entra e onde não entra

<div class="tabela-padrao">

| Etapa | Papel da IA |
|---|---|
| **Desenvolvimento** | **Entra.** Na construção e na evolução do sistema, ajuda a escrever e revisar código, montar protótipos, documentar e criar arte e rascunhos de texto, sempre sob a responsabilidade de uma pessoa. |
| **Execução** | **Não entra, por padrão.** Com o sistema em funcionamento, ele roda por regras fixas, que dão sempre o mesmo resultado para os mesmos dados. A IA não decide nada sobre os dados de produção. |

</div>

Se um sistema vier a usar IA durante a execução, isso é uma exceção e fica declarado na ficha: o que a IA decide, com quais dados e quem confere o resultado.

## Quem responde

A ferramenta que produziu uma alteração não substitui a responsabilidade de quem a publica. Código feito com IA passa pelos mesmos testes, revisão e registro que qualquer outro, no fluxo de [Mudanças e versionamento](/governanca/mudancas/). Compilar, rodar ou "a ferramenta garantiu que está certo" não bastam para considerar uma alteração segura.

## Quem não programa também constrói

Quem conhece bem o processo pode construir descrevendo o que quer e deixando a IA escrever o código (o chamado *vibe coding*). Essa pessoa contribui com as regras de negócio e testa o resultado, e a **publicação em produção** passa sempre pelo responsável técnico. Os papéis estão em [Vibe coding](/governanca/vibe-coding/).

## Cuidados no uso

- **Senhas e chaves** nunca são coladas em conversas com a IA.
- **Dados reais** (clientes, valores, nomes de colegas) não vão para exemplos, prints nem documentação. Usam-se dados fictícios.
- **Ações em produção que exigem credenciais** ficam com a pessoa responsável, não com a IA.
- **Pedidos críticos** começam por um plano: a IA apresenta o que pretende alterar, o que será afetado, os riscos, como pretende testar e como reverter.

## Orientação por sistema

Cada sistema pode ter um arquivo de orientação para assistentes de IA (`CLAUDE.md`) com as regras do projeto: por exemplo, não alterar a versão em uso diretamente, não publicar automaticamente, não apagar dados sem análise e não colocar credenciais no código.

:::note[Importante]
Esse arquivo **orienta**, mas não protege sozinho. A proteção real vem de permissões de acesso, cópias de segurança, revisão e separação de ambientes.
:::
