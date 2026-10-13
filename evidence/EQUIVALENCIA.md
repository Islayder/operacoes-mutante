# Análise dos cinco sobreviventes — StrykerJS 10.0.0

O resultado oficial permanece **97,652582% (208/213)**. Nenhum mutante foi
ignorado e nenhum operador foi excluído. A meta estrita de superar 98% não foi
alcançada. Para 213 mutantes seriam necessárias pelo menos 209 detecções.

## `fatorial`, linha 19 — IDs 31, 32, 33 e 35

Original: `if (n === 0 || n === 1) return 1;`.

| ID | Substituição |
|---|---|
| 31 | condição inteira por `false` |
| 32 | `n === 0 && n === 1` |
| 33 | primeiro operando por `false` |
| 35 | segundo operando por `false` |

Para os argumentos numéricos 0 e 1, deixar de retornar antecipadamente executa
`let resultado = 1`, não entra no laço `for (let i = 2; i <= n; i++)` e retorna
o mesmo 1. Para qualquer outro número, as igualdades estritas já são falsas;
o fluxo não muda. Os negativos continuam rejeitados na linha anterior. Os
testes de 0, 1, 2, 4 e 5 passam em todas essas variantes. Essa justificativa
é uma análise do comportamento, não uma exclusão aplicada ao Stryker.

## `produtoArray`, linha 84 — ID 140

Original: `if (numeros.length === 0) return 1;`; mutante: `if (false) return 1;`.

Para um array numérico vazio, `[].reduce((acc, val) => acc * val, 1)` retorna
o valor inicial 1 sem invocar o callback. Para arrays não vazios, o original
também usa o mesmo reduce. Logo o retorno é idêntico no domínio previsto:
arrays numéricos comuns e o método `Array.prototype.reduce` nativo.

Não se afirma equivalência para objetos hostis, Proxies ou arrays com `reduce`
sobrescrito. Introduzir esses objetos somente para distinguir esse mutante
mudaria o domínio do trabalho e não evidenciaria um defeito matemático.

## Limite e decisão

Nesse domínio, os cinco mutantes equivalentes impõem teto de 208/213 =
97,652582% com o código original e os 213 mutantes produzidos por esta versão.
Excluir esses cinco produziria um percentual ajustado, mas esse percentual
não é o resultado oficial e não é apresentado como cumprimento da meta.

Os seis timeouts finais são os IDs 40, 107, 109, 132, 136 e 137: alterações no
incremento de fatorial, laço do MDC ou recursão de Fibonacci que deixam de
progredir/terminar. Stryker conta Timeout como detecção. Mortos por asserção
são 202; mortos + timeout são 208. Essa distinção está preservada no relatório.

O próximo passo acadêmico é apresentar esta evidência ao professor e obter
uma decisão sobre equivalentes ou uma revisão do projeto/meta. Essa decisão
não foi presumida nem substituída por manipulação da pontuação.
