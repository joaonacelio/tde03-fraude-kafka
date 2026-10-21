import json
import random
import time
import uuid
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)

clientes = ["CLI-001", "CLI-002", "CLI-003", "CLI-004"]
cidades = [
    "Juazeiro do Norte",
    "Crato",
    "Barbalha",
    "Fortaleza"
]

print("Produtor de transações iniciado!")

while True:
    transacao = {
        "transaction_id": str(uuid.uuid4()),
        "client_id": random.choice(clientes),
        "amount": round(random.uniform(100, 15000), 2),
        "city": random.choice(cidades),
        "timestamp": datetime.now().isoformat()
    }

    producer.send("transacoes", value=transacao)
    producer.flush()

    print("Transação enviada:", transacao)
    time.sleep(3)
