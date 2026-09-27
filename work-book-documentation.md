# PROJECT WORK BOOK

Esse documento tem como objetivo registrar todo o passo-a-passo seguido durante a implementação e serve como guia de decisões tomadas e caminhos seguidos de forma completa.

O projeto em questão é para entrega do Midterm Project do curso de Machine Learning promovido pelo DataTalks Club em 2026.

Além da entrega para o curso, esse projeto buscar testar o framework de metodologia de trabalho desenvolvido por mim, onde há desenho de como seguir de forma estruturada um projeto de Data Science. 
- Serão aplicados os passsos referentes a metodologia até o ponto desenvolvido durante as aulas (aula 6).
- Feedbacks desse framework serão computados nesse arquivo para ajuste posterior.
- O framework se encontra no repositório: **data-science-work-methodology**

## 1 - Definição do problema

O primeiro passo da metodologia adota é a criação de um Problem Framing Documentation, onde a ideia é responder as seguintes perguntas antes de tocar de fato nos dados e iniciar a exploração:

    1 - Qual é a decisão de negócio que o modelo vai informar?
    2 - Qual é a unidade de análise?
    3- O target está bem definido e é observável de forma confiável?
    4 - Existe um baseline atual (processo manual, regra de negócio, heurística)?
    5- Qual é o critério de sucesso, travado antes de rodar o primeiro modelo?
    6 - Existe restrição regulatória ou de auditoria que torna explicabilidade formal um requisito, não um nice-to-have?
    7 - Qual é a data de referência e a janela de desempenho do target? 
    8 - O rótulo já maturou pra todas as observações que vão entrar no treino?
    9 - O rótulo depende de uma decisão que o processo atual já tomou sobre aquele caso? 
    10 - Qual a capacidade operacional de resposta, e quanto custa (mesmo grosseiramente) um Falso Positivo e um Falso Negativo? 

Para se manter fiel ao passo a passo dessa metodologia, criou-se o documento **problem-framing-documentation.md**, onde foi estruturado as respostas dessas perguntas seguindo o passo a passo.

## 2 - Coleta dos Dados

Os dados coletados são de uma base sintética no Kaggle. Dessa forma a questão de disponibilidade e verificação não cosnegue ser validada. Aqui separei a estrutura do dataset e colunas.

- **Link:** [Hotel Booking Dataset](https://www.kaggle.com/datasets/saadharoon27/hotel-booking-dataset)
- **Total de elementos:** 119.390.
- **Taxa de cancelamento:** 37.0% 


| Coluna                         | Descrição |
|--------------------------------|----------------------------------------------| 
| hotel                          | Tipo do hotel (cidade, resort)
| lead_time                      | Tempo entre reserva chegada
| arrival_date_year              | Ano da chegada
| arrival_date_month             | Mês da chegada
| arrival_date_week_number       | Número da semana da chegada
| arrival_date_day_of_month      | Dia do Mês da chegada
| stays_in_weekend_nights        | Número de dias do final de semana da reserva
| stays_in_week_nights           | Número de dias de semana da reserva
| adults                         | Número de adultos
| children                       | Número de crianças
| babies                         | Número de bebês
| meal                           | Tipo de refeição reservada
| country                        | País de origem
| market_segment                 | Designação de segmento de mercado
| distribution_channel           | Canal de distribuição da reserva
| is_repeated_guest              | É cliente repetido
| previous_cancellations         | Quantidade de reservas canceladas antes
| previous_bookings_not_canceled | Quantidade de reservar não canceladas antes
| reserved_room_type             | Tipo do quarto da reserva
| assigned_room_type             | Tipo do quarto designado no check-in
| booking_changes                | Número de mudanças feitas na reserva
| deposit_type                   | Tipo de depósito
| agent                          | ID da agência de viagem
| company                        | ID da companhia
| days_in_waiting_list           | Dias na lista de espera antes do agendamento
| customer_type                  | Tipo de reserva
| adr                            | Tarifa diária média
| required_car_parking_spaces    | Número de espaços para estacionamento
| total_of_special_requests      | Número de pedidos especias requisitados
| reservation_status             | Último status da reserva
| reservation_status_date        | Data do último status
| is_canceled                    | Target: indica se foi ou não cancelado
|