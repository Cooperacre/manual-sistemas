---
title: Modelo de ficha
description: Formato padrão da ficha de cada sistema, planilha e automação do catálogo.
---

Toda ficha segue a mesma estrutura, para que qualquer sistema, planilha ou automação possa ser comparado e entendido do mesmo jeito. O texto é escrito para quem decide e para quem usa, não só para quem programa. A parte técnica de manutenção (onde roda, como atualizar) fica no README de cada repositório.

## Estrutura da ficha

O selo de estágio e as quatro seções da primeira tabela aparecem em toda ficha. As demais entram conforme o tipo e a situação do item, e nenhuma é preenchida só para constar.

### Em toda ficha

<div class="tabela-modelo">

| Seção | O que você encontra |
|---|---|
| **Selo de estágio** | Em que ponto o item está: Em uso, Pronto para uso ou Em desenvolvimento (veja abaixo). |
| **Em uma frase** | O que o item entrega, dito de forma direta, com um parágrafo curto de contexto logo depois. |
| **Antes e depois** | Dois cartões lado a lado: o "Antes", descrito de forma neutra e só com fatos, e o "Depois", com o ganho na prática. |
| **Pontos fortes** | Cartões com o que o item tem de mais sofisticado, cada um com título curto e explicação sem jargão. |
| **Quem está por trás** | Quatro cartões: Quem pediu, Quem usa, Quem construiu e Até quando. |

</div>

### Conforme o item

<div class="tabela-modelo">

| Seção | Quando entra |
|---|---|
| **Linha do tempo** | Nos sistemas: pedido, início, entrega, situação e o que falta. |
| **O que faz** ou **Como funciona** | O funcionamento por etapas ou por recurso, em linguagem do usuário. Cada ficha dá o nome que combina com o item. |
| **Resultados** | Só quando há número real de uso (horas poupadas, volume tratado). Sem número comprovado, não entra. |
| **O que falta** | Nos itens ainda fora de uso: o que separa o item do dia a dia. Some quando ele passa a rodar. |
| **Pontos de atenção** | Limites e cuidados de uso, quando existem. |
| **Telas** | Prints com legenda, sempre sem dado pessoal. Algumas automações não têm. |
| **Planilhas relacionadas** | Links para as planilhas que alimentam o item ou que ele alimenta. |

</div>

## Selos de estágio

- **Em uso**: já roda no dia a dia.
- **Pronto para uso**: entregue e testado, aguardando a decisão de adoção de quem pediu.
- **Em desenvolvimento**: ainda em construção.

Uma ficha pode ter um selo a mais de situação (por exemplo, "Aguardando decisão de adoção"). Os selos usam as cores de papéis fixos do manual, sempre com o mesmo significado: verde para em uso, azul para pronto, laranja para em desenvolvimento, amarelo para atenção.

## Cartão "Quem está por trás"

<div class="tabela-modelo">

| Cartão | O que registrar |
|---|---|
| **Quem pediu** | Pessoa e setor que solicitou. Pode ser iniciativa do desenvolvedor. |
| **Quem usa** | Áreas e perfis de usuário. |
| **Quem construiu** | Responsável técnico, com o nível técnico em uma linha abaixo. |
| **Até quando** | Vida útil: **atualiza conforme a necessidade**, ou **temporário** (por exemplo, até a troca do Meta pelo TOTVS, em 01/01/2027). |

</div>

Esses quatro cartões e a linha do tempo são os únicos lugares onde nomes de pessoas aparecem. Eles registram quem está no papel agora, e o nome é atualizado quando a pessoa muda.

## Prints

Só entram prints sem dado pessoal. Quando a tela real tem dado de cliente, o print é gerado com dados fictícios, rodando o sistema de verdade. As imagens têm largura padrão; telas estreitas de aplicativo de computador usam a variante que evita esticar.

:::note
Credenciais, senhas, tokens e chaves **nunca** entram na ficha. A ficha apenas indica **onde** cada credencial é administrada.
:::
