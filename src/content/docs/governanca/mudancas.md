---
title: Mudanças e versionamento
description: Como uma alteração é feita, registrada e publicada, e como se volta atrás se algo der errado.
---

Toda mudança em um sistema segue o mesmo caminho curto. Para a cooperativa, isso significa três coisas: nada entra em uso sem teste, tudo fica registrado e, se algo der errado, dá para voltar atrás.

## O caminho de uma mudança

1. **Pedido.** A necessidade é registrada: o que mudar e por quê.
2. **Cópia de trabalho.** A alteração é feita numa cópia separada do sistema, nunca direto na versão que está em uso.
3. **Teste.** A mudança é testada, inclusive no que ela pode afetar.
4. **Revisão.** Antes de entrar na versão oficial, a mudança é revisada pelo responsável técnico, ou por uma segunda pessoa quando houver (no jargão técnico, um *Pull Request*).
5. **Registro.** A nova versão recebe um número e uma linha no histórico de mudanças.
6. **Publicação.** A nova versão passa a ser usada.

## O que isso garante

- **A versão em uso fica protegida.** Ela não é lugar de experimento. Quando a plataforma permitir, essa proteção é técnica; até lá, vale como regra de trabalho.
- **Tudo tem histórico.** Cada sistema mantém um histórico de mudanças com versão, data e o que mudou, para saber o quê, quando e por quê.
- **Dá para voltar atrás.** Antes de publicar, fica claro como retornar à última versão estável, principalmente quando a mudança mexe nos dados.
- **Operações de risco têm cópia de segurança.** Reescrever o histórico do código, apagar dados ou mudar a estrutura do banco só acontece depois de uma cópia de segurança e com a confirmação de que ninguém está editando ao mesmo tempo.
- **Mudança feita com IA segue o mesmo caminho.** Veja [Desenvolvimento com IA](/governanca/desenvolvimento-com-ia/).
