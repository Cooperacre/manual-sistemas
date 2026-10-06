---
title: Planilhas
description: As planilhas online que apoiam a operação, como são organizadas e por que foram feitas em Google Sheets.
---

## Por que planilhas online

Parte dos controles da operação foi construída em planilhas online (Google Sheets) em vez de Excel local. A escolha foi deliberada:

- **Acesso simultâneo:** várias pessoas usam a mesma planilha ao mesmo tempo.
- **Backup automático e imediato:** cada alteração é salva na hora.
- **Disponibilidade:** funciona de qualquer lugar, sem instalar nada.
- **Controle de acesso:** simples de configurar e de conferir depois, quem tem acesso, qual permissão cada pessoa tem (visualizar, comentar ou editar) e quem é o dono do documento.
- **Rastreabilidade:** o histórico mostra quem usou e quem alterou cada célula.
- **Reversão fácil:** qualquer alteração pode ser desfeita voltando a uma versão anterior.
- **Versão única:** todos os usuários enxergam a mesma versão, sem cópias divergentes.
- **Integração com automações:** aceita ser alimentada por uma automação, sem intervenção manual, como o [Meta Pipeline](/catalogo/meta-pipeline/) faz ao manter o Controle de Saída sempre atualizado.

## Como estão organizadas

As planilhas ficam no Drive da Cooperacre, na pasta **Cooperacre - Planilhas**, separadas por unidade e setor. A organização está sendo centralizada na conta `sistemascooperacre@gmail.com`, criada a pedido do Maxsuel para reunir Drive, GitHub e Netlify numa conta dedicada ao projeto.

- **01 - Matriz:** hoje apenas o setor Comercial.
- **04 - Filial IV:** documentada no manual da Filial IV.

## De onde vêm os dados: uma origem só, para várias planilhas

As planilhas do Comercial não são ilhas separadas: todas nascem do mesmo lugar. O [Meta Pipeline](/catalogo/meta-pipeline/) traz uma cópia dos pedidos faturados do Meta e a grava, poucos minutos depois de cada venda, na aba **DADOS** do [Controle de Saída](/catalogo/controle-de-saida/), alimentada por automação.

A partir daí, cada planilha nova busca só o que precisa dessa fonte, em vez de reaproveitar a aba inteira. Por exemplo, a Transferência Estoque Balcão mantém sua própria cópia **reduzida**, com apenas a chave de busca de que precisa (pedido + produto), o que a deixa mais leve e rápida do que se ela lesse a base completa do Controle de Saída a cada consulta. É uma escolha de desempenho, repetida em cada planilha nova: pegar da fonte só o necessário, do jeito mais leve possível.

## Planilhas do Comercial (Matriz)

<div class="tabela-resumo">

| Planilha | Para que serve | Situação |
|---|---|---|
| [Controle de Saída](/catalogo/controle-de-saida/) | Acompanhar o status das entregas e emitir o protocolo de entrega por motorista | Em uso |
| [Transferência Estoque Balcão](/planilhas/transferencia-estoque-balcao/) | Calcular a quantidade de cada item vendido por pedido, para a nota de transferência ao estoque eletrônico da Filial 09 | Em uso |
| [Controle Interno](/planilhas/controle-interno/) | Conferir a forma de pagamento de cada pedido do comercial de polpa e os totais, para o faturamento posterior | Em uso |
| [Estoque Polpa](/catalogo/estoquepolpa/) | Mostrar o saldo de estoque de polpa por sabor e tamanho dia a dia, cruzando entradas, saídas e contagem física com o que o Meta Pipeline traz do Meta | Em uso |

</div>
