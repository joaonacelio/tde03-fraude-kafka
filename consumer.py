import json
from datetime import datetime, timedelta
from kafka import KafkaConsumer
from database import salvar_transacao

consumer = KafkaConsumer(
    "transacoes",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda value: json.loads(value.decode("utf-8"))
)

historico = {}

print("Consumidor de transações iniciado!")

for mensagem in consumer:
    transacao = mensagem.value

    cliente = transacao["client_id"]
    valor = transacao["amount"]
    cidade = transacao["city"]
    momento = datetime.fromisoformat(transacao["timestamp"])

    if cliente not in historico:
        historico[cliente] = []

    historico[cliente] = [
        t for t in historico[cliente]
        if momento - t["momento"] <= timedelta(minutes=10)
    ]

    alertas = []

    if valor >= 10000:
        alertas.append("ALTO_VALOR")

    ultimos_60s = [
        t for t in historico[cliente]
        if timedelta(0) <= momento - t["momento"] < timedelta(seconds=60)
    ]

    if len(ultimos_60s) >= 3:
        alertas.append("TEMPO_60s")

    cidades_recentes = [
        t for t in historico[cliente]
        if t["cidade"] != cidade
    ]

    if cidades_recentes:
        alertas.append("GEO_10m")

    salvar_transacao(transacao, ", ".join(alertas) if alertas else "NORMAL")

    historico[cliente].append({
        "momento": momento,
        "cidade": cidade
    })

    print("\nTransação recebida:")
    print(json.dumps(transacao, indent=4, ensure_ascii=False))

    if alertas:
        print("ALERTA DE FRAUDE:", ", ".join(alertas))
    else:
        print("Transação normal.")
