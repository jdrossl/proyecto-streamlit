import sqlite3
import pandas as pd

DB = "finanzas.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            categoria TEXT NOT NULL,
            tipo TEXT NOT NULL,
            monto REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_transacciones():
    conn = get_conn()
    df = pd.read_sql("SELECT * FROM transacciones ORDER BY fecha DESC", conn)
    conn.close()
    return df

def insertar(fecha, descripcion, categoria, tipo, monto):
    conn = get_conn()
    conn.execute(
        "INSERT INTO transacciones (fecha, descripcion, categoria, tipo, monto) VALUES (?, ?, ?, ?, ?)",
        (fecha, descripcion, categoria, tipo, monto)
    )
    conn.commit()
    conn.close()

def eliminar(id):
    conn = get_conn()
    conn.execute("DELETE FROM transacciones WHERE id = ?", (id,))
    conn.commit()
    conn.close()
