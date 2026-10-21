import sqlite3

def conectar():
    conexao = sqlite3.connect("transacoes.db")
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            client_id TEXT NOT NULL,
            amount REAL NOT NULL,
            city TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            fraud_type TEXT
        )
    """)
    conexao.commit()
    return conexao


def salvar_transacao(transacao, fraud_type):
    conexao = conectar()

    conexao.execute("""
        INSERT OR IGNORE INTO transactions
        (transaction_id, client_id, amount, city, timestamp, fraud_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        transacao["transaction_id"],
        transacao["client_id"],
        transacao["amount"],
        transacao["city"],
        transacao["timestamp"],
        fraud_type
    ))

    conexao.commit()
    conexao.close()
