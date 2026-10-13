# Auditoria dos critérios do enunciado

| Critério | Peso | Evidência e situação |
|---|---:|---|
| Configuração e execução | 10% | StrykerJS 10.0.0 + Jest runner 10.0.0; configuração e lockfile; duas execuções de cada etapa com os mesmos resultados. Atendido. |
| Análise dos mutantes | 35% | IDs 11, 183 e 200, capturas reais, causa da sobrevivência e testes que os mataram no PDF; equivalentes explicados separadamente. Atendido. |
| Eficácia dos testes | 35% | 99 novos testes; 149 aprovados; 100% de cobertura; 56 não detectados reduzidos a 5. Melhoria comprovada, mas **meta >98% pendente**: oficial 97,65%. |
| Relatório | 20% | PDF novo com 4 páginas, capa, comparação, três mutantes com capturas, soluções, resultado, conclusão e limitação explícita. Atendido documentalmente. |

## Integridade

- Produção e suíte original preservadas, verificadas por conteúdo contra o commit base.
- Mesmo universo de 213 mutantes em ambas as etapas.
- Sem operadores excluídos, mutantes ignorados ou ajustes no denominador.
- Sem execução simulada ou captura fictícia.
- Cinco equivalentes continuam `Survived` no resultado oficial.
- Não foi enviado material ao portal acadêmico; a tarefa solicitou preparar os entregáveis e publicar no fork.

O trabalho **não é declarado integralmente concluído**: a meta estrita do
enunciado requer uma decisão acadêmica sobre os equivalentes documentados.
