# Justificativa das métricas — Dashboard 2

Os indicadores usam o dataset tratado dos atletas das Olimpíadas de Paris 2024. O público principal é composto por gestores esportivos e comissões técnicas que precisam comparar a composição de delegações e modalidades. Os filtros de país e modalidade do Dashboard 2 são opcionais e recalculam todos os KPIs.

## Métrica 1: Total de atletas
- **Variável:** `code` (identificador do atleta)
- **O que mede:** quantidade de atletas únicos no recorte. A contagem usa identificadores distintos para não contar uma pessoa mais de uma vez.
- **Por que foi escolhida:** contextualiza o tamanho da amostra considerada pelos outros indicadores.
- **Público-alvo:** gestores esportivos e comissões técnicas que acompanham o tamanho das delegações.
- **Qual decisão pode ser apoiada por essa métrica?** avaliar o volume de participantes incluídos em uma comparação por país ou modalidade.
- **O que comunica ao público-alvo:** quantos atletas estão representados após aplicar os filtros.

## Métrica 2: Idade mediana
- **Variável:** `age` (idade em anos)
- **O que mede:** mediana das idades válidas dos atletas incluídos.
- **Por que foi escolhida:** representa a idade central sem ser tão influenciada por idades extremas quanto a média.
- **Público-alvo:** comissões técnicas que comparam o perfil etário das delegações e modalidades.
- **Qual decisão pode ser apoiada por essa métrica?** comparar o perfil etário entre países ou modalidades.
- **O que comunica ao público-alvo:** metade dos atletas tem idade igual ou inferior à mediana e metade igual ou superior.

## Métrica 3: Participação feminina
- **Variável:** `gender` (gênero registrado no dataset)
- **O que mede:** percentual de atletas com gênero registrado como feminino entre os registros com gênero conhecido.
- **Por que foi escolhida:** resume a composição por gênero da amostra de forma fácil de comparar entre recortes.
- **Público-alvo:** gestores esportivos que acompanham a representação de gênero nas delegações e modalidades.
- **Qual decisão pode ser apoiada por essa métrica?** identificar recortes com diferentes níveis de participação feminina e direcionar análises mais detalhadas.
- **O que comunica ao público-alvo:** a proporção de atletas identificadas como mulheres; registros sem gênero não entram no denominador.

## Métrica 4: Modalidades representadas
- **Variável:** `disciplines` (modalidade ou modalidades associadas ao atleta)
- **O que mede:** quantidade de modalidades distintas presentes entre os atletas filtrados.
- **Por que foi escolhida:** mostra a amplitude esportiva do recorte e ajuda a contextualizar as comparações.
- **Público-alvo:** gestores de delegações que avaliam a variedade de modalidades representadas.
- **Qual decisão pode ser apoiada por essa métrica?** avaliar se um recorte cobre várias modalidades ou está concentrado em poucas.
- **O que comunica ao público-alvo:** quantas modalidades diferentes aparecem entre os atletas considerados.
