# Entregas

Esta pasta reúne os materiais de entrega das Aulas 21, 22 e 23. Os rascunhos ficam aqui em `.jpg` ou `.png`. Os arquivos de uso de IA ficam
em [`prompts/`](../prompts/).

> **Nota sobre os wireframes desta entrega:** os arquivos atuais foram
> reconstruídos durante a revisão, depois da primeira implementação do app.
> Eles documentam o layout, mas não comprovam que o planejamento ocorreu
> antes da implementação original.

## Entregas por aula

### Aula 21 — Dashboard 1

- [x] [`rascunho-dashboard1.png`](rascunho-dashboard1.png) — wireframe da
  página com sidebar, filtros, área de correlação e histogramas.

Além do material desta pasta, a entrega da aula inclui o `app.py` com pelo
menos um seletor de variáveis e um slider de intervalo funcionando, o app
executando localmente e a declaração de uso de IA atualizada em
[`prompts/declaracao-uso-ia.md`](../prompts/declaracao-uso-ia.md).

### Aula 22 — Dashboard 2

- [x] [`rascunho-dashboard2.png`](rascunho-dashboard2.png) — wireframe com
  público-alvo, filtros, métricas e visuais do Dashboard 2.
- [x] [`justificativa-metricas.md`](justificativa-metricas.md) — justificativa
  preenchida para as métricas/KPIs.

A justificativa deve explicar, para cada métrica, a variável relacionada, o
que mede, por que foi escolhida, a quem se destina, que decisão pode apoiar e
o que comunica ao público-alvo. Atualize também a declaração de uso de IA em
[`prompts/declaracao-uso-ia.md`](../prompts/declaracao-uso-ia.md).

### Aula 23 — Finalização e publicação

Confira também os itens de entrega que não ficam nesta pasta:

- [ ] Dashboard 1 e Dashboard 2 implementados no app, em abas, com widgets,
  métricas e gráficos funcionando.
- [ ] App publicado no Streamlit Community Cloud e testado pelo link público.
- [x] Link do app (`.streamlit.app`) incluído no [`README.md`](../README.md).
- [ ] Repositório próprio no GitHub com as alterações desta revisão commitadas
  e enviadas.
- [x] `app.py`, notebooks, `requirements.txt` e `data/clean/dataset.csv`
  incluídos no repositório. O CSV atual e as saídas dos notebooks não contêm
  nomes, códigos individuais ou datas completas de nascimento.

O passo a passo e os critérios de teste do deploy estão no
[`ROTEIRO.md`](../ROTEIRO.md).

## Modelo de justificativa das métricas

Use uma seção para cada KPI. Preencha todos os campos e adapte-os à métrica e
ao público do projeto:

```markdown
## Métrica: <nome>
- **Variável:** <coluna e significado>
- **O que mede:** <definição do indicador, incluindo o recorte/denominador>
- **Por que foi escolhida:** <motivo da escolha>
- **Público-alvo:** <quem deve compreender ou usar o indicador>
- **Qual decisão pode ser apoiada por essa métrica?** <decisão ou comparação>
- **O que comunica ao público-alvo:** <interpretação em linguagem simples>
```

### Exemplo

```markdown
## Métrica: Distribuição do colesterol em relação à mediana
- **Variável:** `chol` (colesterol sérico, mg/dl)
- **O que mede:** proporção da amostra abaixo, em torno e acima da mediana de
  `chol`, além de estatísticas descritivas. Defina e explicite a faixa usada
  para "em torno" (por exemplo, ±10% da mediana).
- **Por que foi escolhida:** resume a distribuição sem exigir a leitura de um
  histograma ou boxplot.
- **Público-alvo:** pessoas que precisam de uma visão resumida da amostra.
- **Qual decisão pode ser apoiada por essa métrica?** comparar a distribuição
  entre recortes da amostra.
- **O que comunica ao público-alvo:** como os valores se distribuem em relação
  à mediana, em termos compreensíveis para quem não conhece a variável.
```

## Arquivos de apoio existentes

- `Painel de Análise Exploratória.png` — imagem de referência do painel; não
  substitui os rascunhos dos dois dashboards.
- `exemplo_professora.jpeg` — exemplo fornecido pela professora.

Os rascunhos são entregáveis próprios: não use as imagens de referência como
substitutas e não os coloque no `.gitignore`.
