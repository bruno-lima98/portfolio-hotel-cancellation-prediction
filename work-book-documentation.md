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

