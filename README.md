# Análise de Eficácia de Testes com Teste de Mutação

**Testes de Software — Islayder Jackson Ribeiro de Oliveira — matrícula 859552.**

Fork de [CleitonSilvaT/operacoes-mutante](https://github.com/CleitonSilvaT/operacoes-mutante),
base `c10621a4fe20f8332e783e06cad0e1b98449aad2`. As 50 funções e os 50 testes
originais estão preservados. Foram acrescentados 99 testes em arquivo separado.

## Resultado real e limitação da meta

| Métrica | Inicial | Final |
|---|---:|---:|
| Testes aprovados / total | 50 / 50 | 149 / 149 |
| Testes reprovados | 0 | 0 |
| Cobertura de instruções | 85,41% | 100% |
| Cobertura de ramos | 58,82% | 100% |
| Cobertura de funções (inclui callbacks) | 100% | 100% |
| Cobertura de linhas | 98,64% | 100% |
| Mutation Score oficial | **73,71%** | **97,65%** |
| Mutantes mortos | 154 | 202 |
| Timeouts | 3 | 6 |
| Sobreviventes | 44 | 5 |
| Sem cobertura | 12 | 0 |
| Ignorados / erros | 0 / 0 | 0 / 0 |
| Total de mutantes | 213 | 213 |

Stryker calcula `(Killed + Timeout) / total válido`; o resultado final exato é
`208 / 213 × 100 = 97,652582%`. A melhora é de 23,94 pontos percentuais.
**A meta superior a 98% não foi atingida.** Os cinco sobreviventes são
equivalentes para o domínio matemático previsto. A [análise de equivalência](evidence/EQUIVALENCIA.md)
explica cada ID e o teto de 97,65%, sem alterar o resultado oficial. Nenhum
arquivo de produção ou operador de mutação foi excluído. É necessária uma
decisão do professor sobre essa incompatibilidade entre a meta e os equivalentes.

## Reproduzir

Ambiente executado: Windows x64, Node **24.19.0**, npm **11.17.0**, Jest
**29.7.0**, StrykerJS e Jest runner **10.0.0**. Use Node 24 e o lockfile incluído.

```sh
git clone https://github.com/Islayder/operacoes-mutante.git
cd operacoes-mutante
npm ci
npm test -- --coverage --runInBand
npx stryker run
```

O Stryker usa `src/**/*.js` integralmente, análise de cobertura por teste,
dois processos e os operadores padrão. A lista `files` restringe somente os
arquivos copiados para o sandbox aos arquivos do projeto; não filtra mutantes.
`disableTypeChecks: false` evita processamento de tipos externos neste projeto JS.
O Jest original usa Babel e CommonJS apesar de `type: module`; a execução por
Jest foi preservada, sem reescrever a implementação para ESM.

Para reconstruir a comparação mantendo os relatórios históricos:

```sh
npm run validate:initial
npm run validate:final
npm run audit:evidence
```

Os dois primeiros comandos executam Jest e Stryker de verdade e geram
`reports/reproduced/initial/` e `reports/reproduced/final/`. A etapa inicial
seleciona somente `test/operacoes.test.js`; a final seleciona ambas as suítes.
Os comandos terminam com sucesso quando as ferramentas concluem; isso não
significa superar a meta. `evidence/summary.json` registra `targetAbove98Met: false`.
`audit:evidence` compara as fontes com o commit base (normalizando CRLF/LF),
confere o mesmo universo de mutantes e verifica os três casos analisados.

## Entrega e evidências

- [Relatório acadêmico em PDF — 4 páginas](docs/Relatorio_Teste_Mutacao.pdf).
- [HTML Stryker inicial](evidence/initial/mutation/mutation.html) e [final](evidence/final/mutation/mutation.html).
- JSONs completos e logs em `evidence/initial/` e `evidence/final/`.
- Coberturas Jest e contagens originais nas mesmas pastas.
- [Resumo extraído dos JSONs](evidence/summary.json).
- [Segunda execução de confirmação](evidence/recheck/summary.json), com logs.
- Capturas reais do HTML inicial em `evidence/screenshots/`.
- [Auditoria dos critérios do enunciado](evidence/CRITERIOS.md).

Para navegar no HTML, abra o arquivo localmente ou sirva a pasta:

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Acesse `http://127.0.0.1:8765/evidence/initial/mutation/mutation.html`.
O GitHub mostra o código do HTML; baixe ou clone o repositório para usar o relatório interativo.

Os mutantes críticos são **11** (`divisao`, mensagem de erro), **183**
(`isMaiorQue`, `>` para `>=`) e **200** (`medianaArray`, ordenação removida).
Os três foram `Survived` na linha de base e `Killed` na execução final.

## Regenerar o PDF

```sh
python -m pip install reportlab pypdf
python scripts/gerar_relatorio.py
```

O script lê as métricas e as capturas já preservadas; não simula execuções.
O relatório distingue a entrega documental da meta numérica ainda pendente.

## Referências

- Enunciado: *Análise de Eficácia de Testes com Teste de Mutação*, fornecido pelo professor.
- [StrykerJS — documentação oficial](https://stryker-mutator.io/docs/stryker-js/getting-started/).
- [Estados e métricas dos mutantes](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/).
