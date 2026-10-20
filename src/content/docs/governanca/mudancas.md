---
title: Mudanças e versionamento
description: Como uma alteração é feita, registrada e publicada, e como se volta atrás se algo der errado.
---

Toda mudança em um sistema segue o mesmo caminho curto. Para a cooperativa, isso significa três coisas: nada entra em uso sem teste, tudo fica registrado e, se algo der errado, dá para voltar atrás.

## O caminho de uma mudança

1. **Pedido.** A necessidade é registrada: o que mudar e por quê.
2. **Cópia de trabalho.** A alteração é feita numa cópia separada do sistema, em geral a máquina de quem desenvolve, nunca direto na versão que está em uso.
3. **Teste.** A mudança é testada, inclusive no que ela pode afetar. Cada sistema define onde testa (um banco de teste próprio ou, quando só existe o de produção, registros fictícios apagados ao fim) e registra isso na sua documentação técnica. Em nenhum caso o teste expõe ou altera dado real.
4. **Revisão.** Antes de entrar na versão oficial, o responsável técnico confere o que mudou. Quando houver uma segunda pessoa na equipe, a revisão passa a ser feita por ela, por meio de um pedido formal de revisão (no jargão técnico, um *Pull Request*).
5. **Registro.** A nova versão recebe um número e uma linha no histórico de mudanças.
6. **Publicação.** A nova versão passa a ser usada.

## O que isso garante

- **A versão em uso fica protegida.** Ela não é lugar de experimento. Quando a plataforma permitir, essa proteção é técnica; até lá, vale como regra de trabalho.
- **Tudo tem histórico.** Cada sistema mantém um histórico de mudanças com versão, data e o que mudou, para saber o quê, quando e por quê.
- **Dá para voltar atrás.** Antes de publicar, fica claro como retornar à última versão estável, principalmente quando a mudança mexe nos dados.
- **Operações de risco têm cópia de segurança.** Reescrever o histórico do código, apagar dados ou mudar a estrutura do banco só acontece depois de uma cópia de segurança e com a confirmação de que ninguém está editando ao mesmo tempo.
- **A implantação fica escrita quando não é só publicar.** Se a nova versão exige migrar o banco, configurar algo novo, atualizar outro sistema ou fazer uma ação manual, o histórico de mudanças daquela versão diz o que fazer e como desfazer.
- **Mudança feita com IA segue o mesmo caminho.** Veja [Desenvolvimento com IA](/governanca/desenvolvimento-com-ia/).

## Números de versão

Cada versão recebe um número no formato `MAJOR.MINOR.PATCH` (por exemplo, `1.2.0`):

- **MAJOR** sobe quando muda o jeito de usar, rodar ou publicar o sistema.
- **MINOR** sobe quando entra uma funcionalidade nova.
- **PATCH** sobe para correções.

Enquanto o sistema ainda está em desenvolvimento ou em teste com os usuários, a versão começa com zero (`0.1.0`, `0.2.0`…). A versão **1.0.0** marca a entrada oficial em produção: usuários reais no dia a dia e testes de aceite encerrados.
