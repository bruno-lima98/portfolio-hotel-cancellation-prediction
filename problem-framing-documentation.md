## Problem Framing Documentation

*Cenário hipotético*

### 1. Objetivos

O objetivo do projeto é criar um modelo para prever o cancelamento (ou não) de reservas de quartos de Hotel.

Através desse modelo, serão direcionadas campanhas para as próximas reservas, para evitar que esse tipo de cancelamento ocorra e se retenha mais clientes, a depender das descobertas.

- O target do nosso dataset é `is_canceled`, que identifica no histórico se aquele reserva foi cancelada ou não. 

### 2. Ganhos efetivos

Para o problema atual, não existe nenhum tipo de estratégica especifica para tentar evitar o cancelamento de algum tipo de reserva, hoje o foco é trazer mais clientes de forma geral sem uma avaliação de reservar "fantasmas", que são canceladas após algum tempo ou em cima da hora.

#### 2.1. Critérios de Sucesso

- Hoje temos uma taxa de cancelamento de **37.0%**. *(taxa do dataset, como não temos dados reais, vamos assumir isso para o cenário)*
- O objetivo é reduzir essa taxa em 60% após 12 meses de implementação do modelo, no entanto o foco principal objetivo é saber se haverá ou não cancelamento, a eficácia e melhoria dessa taxa não entrar no escopo do modelo.
- As campanhas de marketing ou outros tipos de estratégias para a retenção de reservas ou atração de clientes sem cancelamento vai depender dos motivos de cancelamento, de forma que o modelo deve trazer esse tipo de diferenciação.

#### 2.2. Explicabilidade do modelo

É necessário que o modelo consiga trazer os motivos que geraram as previsões pois as ações tomadas deverão ser específicas para:

- Evitar reservas realizadas de serem canceladas.
- Atrair mais reservas que converterão.
- Diferenciar tipos de estratégias.

### 3. Dataset

- Unidade de medida: reservas de quarto de Hotel.
- Total de reservas: 119.390.
- Taxa de cancelamento: 37.0%.
- Data de coleta: 2014-10 até 2017-09 (35 meses).
- Estão presentes no dataset todas as reservas realizadas dentro do período, incluindo as efetivadas ou canceladas.

### 4. Utilização do modelo

A uitilização do modelo deverá ser utilizada a partir da data de reserva, de forma que as features consideradas devem ser apenas informações disponíveis nesse momento. Àquelas que são geradas posteriormente devem ser descartadas para eviatrem qualquer tipo de leakage.

Como o objetivo atual é tentar escontrar soluções para que esse cancelamento não ocorra, o quando antes for identificado esse tipo de comportamento, mais tempo haverá disponível para contra-medidas.

### 5. Custos operacionais

Como a redução dos cancelamentos a partir de estratégias de contenção é o principal objetivo desse projeto, é necessário avaliar os custos envolvidos e até onde vale de fato a implementação desse tipo de abordagem.

#### 5.1. O Problema Atual

O custo hoje médio de uma reserva realizada na redes de hotéis é USD 150 a diária e com uma locação de período médio de 3 dias, de forma que podemos extraploar para o valor total não convertido no período:

<p align="center">

$$119.390 \times 37\% \times 150 \times 3 = \text{USD } 19.878\text{ M}$$

</p>

No entanto é importante observar que uma reserva cancelada impossibilita uma outra reserva (que poderia ser convertida) de acontecer. Isso acaba se tornando um valor não convertido, pois o fato de uma reserva ser realizada, ela trava a locaçã o do quarto até o momento de cancelamento.

#### 5.2. Estratégias de Contenção

Mesmo que o modelo indique a possibilidade de cancelamento de forma extremamente confiável e precisa, não é possível pré-cancelar uma reserva dos clientes, pois isso acabaria levando à cancelamentos indevidos e até problemas com a credibilidade da rede de Hotéis.

Dessa forma, a principal atuação resultante da aplicação do modelo é a tentativa de reverter uma cancelamento (impedir que não ocorra) através de estratégias de marketing e descontos direcionais.

- Custo de uma campanha de marketingmédia = USD 20.000.
- Clientes afetados = 50.000.
- Taxa de conversão média = 5%.
- Faixas de desconto = 5%, 10%, 20%, 50%.

#### 5.3. Custos de Falsos-Negativos e Falsos-Positivos

