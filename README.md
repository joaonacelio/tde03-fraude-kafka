# TDE 03 — Detecção de Fraudes com Apache Kafka

## Objetivo

Desenvolver uma aplicação de processamento de transações financeiras utilizando Apache Kafka e Python, identificando possíveis atividades suspeitas em tempo real.

## Tecnologias utilizadas

- Python
- Apache Kafka
- kafka-python
- SQLite
- Docker Compose

## Estrutura do projeto

- `producer.py`: gera e publica transações financeiras no Kafka.
- `consumer.py`: consome as transações e aplica regras de detecção de fraude.
- `database.py`: cria e gerencia o banco de dados SQLite.
- `docker-compose.yml`: configura o serviço Kafka.
- `requirements.txt`: lista as dependências Python.
- `transacoes.db`: banco de dados gerado durante a execução.

## Regras de detecção de fraudes

1. **Alto valor:** identifica transações com valor igual ou superior a R$ 10.000.
2. **Frequência de transações:** identifica três ou mais transações do mesmo cliente em menos de 60 segundos, contando a transação atual.
3. **Mudança de cidade:** identifica uma transação realizada em cidade diferente da transação anterior do cliente dentro da janela de dez minutos.

As transações são classificadas como normais ou suspeitas e armazenadas no banco de dados SQLite.

## Requisitos

- Python instalado.
- Apache Kafka em execução e acessível em `localhost:9092`.
- Dependência `kafka-python` instalada.

## Instalação

Instale as dependências Python executando:

```bash
pip install -r requirements.txt
```

## Execução

Primeiro, inicie o serviço Kafka conforme a configuração do projeto.

Em um terminal, execute o consumidor:

```bash
python consumer.py
```

Em outro terminal, execute o produtor:

```bash
python producer.py
```

O produtor enviará transações periodicamente, enquanto o consumidor processará as mensagens, identificará possíveis fraudes e exibirá os resultados no terminal.

## Banco de dados

As transações processadas são armazenadas no arquivo `transacoes.db`, utilizando SQLite.

A tabela `transactions` contém os seguintes campos:

- `transaction_id`: identificador único da transação.
- `client_id`: identificador do cliente.
- `amount`: valor da transação.
- `city`: cidade da transação.
- `timestamp`: data e horário da transação.
- `fraud_type`: classificação da transação ou alerta identificado.

## Observação

Este projeto possui finalidade acadêmica. As regras implementadas identificam transações potencialmente suspeitas, mas não confirmam a ocorrência de fraude real.