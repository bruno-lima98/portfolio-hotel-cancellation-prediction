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
- O objetivo é reduzir essa taxa em 60%, chegando em uma taxa de cancelamento máxima de 15% ao final dos próximo 12 meses, a partir da utilização do modelo.
- As campanhas de marketing ou outros tipos de estratégias para a retenção de reservas ou atração de clientes sem cancelamento vai depender dos motivos de cancelamento, de forma que o modelo deve trazer esse tipo de diferenciação.

#### 2.2. Explicabilidade do modelo

É necessário que o modelo consiga trazer os motivos que geraram as previsões pois as ações tomadas deverão ser específicas para:

- Evitar reservas realizadas de serem canceladas.
- Atrair mais reservas que converterão.
- Diferenciar tipos de estratégias.

### 3. Dataset

- Total de reservas: 119.390.
- Taxa de cancelamento: 37.0%.
- Data de coleta: 2014-10 até 2017-09 (35 meses).