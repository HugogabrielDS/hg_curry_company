# 1. O Problema de negócio

A Curry Company é uma empresa de tecnologia que criou um aplicativo que conecta Restaurantes, Entregadores e Pessoas.

Através desse aplicativo, é possível realizar o pedido de uma refeição, em qualquer restaurante cadastrado, e recebê-lo no
conforto da sua casa por um entregador também cadastrado no aplicativo da Curry Company.

A Empresa realiza negócios entre Restaurantes, Entregadores e Pessoas, e gera muitos dados sobre entregas, tipos de pedidos,
condições climáticas, avaliação dos entregadores e etc. Apesar da entrega estar crescendo, em termos de entregas, o CEO não 
tem visibilidade completa dos KPIs de crescimento da empresa.

A Curry Company me contratou como Cientista de Dados para sanar a necessidade de ter os principais KPIs estratégicos
organizados em uma única Ferramenta, para que o CEO possa consultar e conseguir tomar decisões simples, porém importantes.

A Curry Company possui um modelo de negócio chamado Marketplace, que faz o intermédio do negócio entre os 3 (três)
interessados principais: Restaurantes, Entregadores e Pessoas compradoras. Para acompanhar o crescimento desses negócios, o CEO
gostaria de ver as seguintes métricas de crescimento:

## Do lado da empresa:
1. Quantidade de pedidos por dia.
2. Quantidade de pedidos por semana.
3. Distribuição dos pedidos por tipo de tráfego.
4. Comparação do volume de pedidos por Cidade e tipo de tráfego.
5. Quantidade de pedidos por entregador por semana.
6. A localização central de cada cidade por tipo de tráfego.

## Do lado do entregador:
1. A menor e a maior idade dos entregadores.
2. A pior e a melhor condição dos veículos.
3. A Avaliação média por entregador.
4. A Avaliação média e o Desvio Padrão por tipo de tráfego.
5. A Avaliação média e o Desvio Padrão por condições climáticas.
6. Os 10 entregadores mais rápidos por cidade
7. Os 10 entregadores mais lentos por cidade.

## Do lado do restaurante:
1. A Quantidade de entregadores únicos.
2. A distância média dos restaurantes e dos locais de entrega.
3. O Tempo médio e o desvio padrão de entrega por cidade
4. O Tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.
5. O Tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego.
6. O Tempo médio de entrega durante os Festivais.

O Objetivo deste projeto é criar um conjunto de dados e/ou tabelas que exibam essas métricas da melhor forma
possível para o CEO.

# 2. Premissas assumidas para a Análise

1. A Análise foi realizada com dados entre 11/02/2022 e 06/04/2022
2. Marketplace foi o modelo de negócio assumido.
3. As 3 principais visões de negócio foram: Visão Empresa, Visão Entregadores e Visão Restaurante.

# 3. Estratégia da solução

O painel estratégico foi desenvolvido utilizando as métricas que refletem as 3 principais visões do modelo de negócio
da Empresa.

1. Visão Empresa
2. Visão Entregadores
3. Visão Restaurantes.

Cada visão é representada pelo seguinte conjunto de mpetricas.

1. Visão do crescimento da empresa
   1. Pedidos por dia
   2. Porcentagem de pedidos por condições de trânsito.
   3. Quantidade de pedidos por tipo e por cidade.
   4. Pedidos por semana.
   5. Quantidade de pedidos por tipo de entrega.
   6. Quantidade de pedidos por condições do trânsito e tipo de cidade.

2. Visão do crescimento dos Restaurantes.
   1. Quantidade de pedidos únicos.
   2. Distância média percorrida.
   3. Tempo médio de entrega durante o Festival e dias normais.
   4. Desvio padrão e Tempo médio de entrega durante o Festival e dias normais.
   5. Tempo médio de entrega por cidade.
   6. Distribuição do tempo médio de entrega por cidade.
   7. Tempo médio de entrega por tipo de pedido.

3. Visão crescimento dos entregadores
   1. Idade do entregador mais velho e do mais novo.
   2. Avaliação do melhor e do pior veículo.
   3. Avaliação média por entregador.
   4. Avaliação média por condições de trânsito.
   5. Avaliação média por condições climáticas.
   6. Tempo médio do entregador mais rápido.
   7. Tempo médio do entregador mais rapido por cidade.

# 4. Top 3 Insights de Dados

  1. A Sazonalidade da quantidade de pedidos é diária. Há uma variação de aproximadamente 10% do número de pedidos em
dias sequênciais.
  2. As Cidades do Tipo Semi-Urban não possuem condições baixas de trânsito.
  3. As maiores variações no tempo de entrega, acontecem durante o clima ensolarado.

# 5. O Produto Final

Painel online, hospedado em Cloud e disponível para acesso em qualquer dispositivo conectado com a Internet.  

O Painel pode ser acessado atráves do link: 

# 6. Conclusão

O Objetivo deste projeto é criar um conjunto de gráficos e/ou tabelas que exibam métricas da melhor forma possível para o CEO.

Da visão da Empresa, podemos concluir que o número de pedidos cresceu entre a semana 06 e a semana 13 do ano de 2022.

# 7. Próximos passos

  1. Reduzir o número de métricas
  2. Criar novos filtros.
  3. Adicionar novas visões de negócio.

