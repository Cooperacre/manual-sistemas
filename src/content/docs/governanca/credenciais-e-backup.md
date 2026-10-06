---
title: Credenciais e backup
description: Onde senhas e chaves são guardadas, o que é conferido antes de publicar um código e como cada sistema garante cópia de segurança.
---

## Senhas e chaves

Nenhuma senha, chave ou credencial real fica dentro do código. Elas ficam num arquivo de configuração protegido, no ambiente onde o sistema roda, e cada sistema traz um arquivo-modelo que lista só os **nomes** das configurações, nunca os valores. Este manual também não guarda senhas nem chaves: cada ficha indica **onde** elas são administradas.

<div class="tabela-padrao">

| Item | Como é |
|---|---|
| **Quem cuida** | O responsável técnico indicado na ficha do sistema. |
| **Onde ficam** | Fora do código, em arquivo de configuração protegido. |
| **Se uma se perder** | Emite-se outra no painel do próprio serviço. |
| **Troca periódica** | Cria-se a nova, atualiza-se a configuração e cancela-se a antiga. |

</div>

## Antes de publicar um código

Antes de um código ser enviado a um repositório, passa por quatro conferências:

1. **Verificação automática** que procura senhas e chaves esquecidas, inclusive em scripts e arquivos de exemplo.
2. **Lista do que nunca vai para o repositório**, conferida arquivo por arquivo.
3. **Dados reais** em exemplos, documentação e imagens: clientes, valores e nomes de pessoas.
4. **Histórico limpo.** Se algo sensível já tiver entrado, o histórico é refeito antes da publicação (ou o repositório recomeça de um primeiro registro limpo) e a credencial exposta é trocada.

## Backup e recuperação

O código de cada sistema tem cópia no repositório. Os dados continuam na fonte (a planilha ou o sistema de gestão), com a proteção que ela já tem. Os sistemas que **guardam dados próprios** registram na ficha:

- o que tem cópia de segurança (dados, arquivos enviados, configurações);
- com que frequência e por quanto tempo as cópias são guardadas;
- quem cuida delas e onde ficam;
- como restaurar.

Uma cópia só vale quando a **restauração já foi testada** ao menos uma vez.

## Ambientes

Quando aplicável, as mudanças são testadas num ambiente de desenvolvimento antes de chegar à produção. Em geral, esse ambiente é a máquina de quem desenvolve.
