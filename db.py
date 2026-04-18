import sqlite3
import pandas as pd
import json

DB = "finanzas.db"

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            tipo TEXT NOT NULL,
            monto REAL NOT NULL,
            notas TEXT,
            metodo TEXT
        )
    """)
    # Alter table to add notas column if it doesn't exist
    try:
        conn.execute("ALTER TABLE transacciones ADD COLUMN notas TEXT")
    except sqlite3.OperationalError:
        pass
    # Alter table to add metodo column if it doesn't exist
    try:
        conn.execute("ALTER TABLE transacciones ADD COLUMN metodo TEXT")
    except sqlite3.OperationalError:
        pass
    conn.commit()
    conn.close()

def get_transacciones(fecha_inicio=None, fecha_fin=None):
    conn = get_conn()
    query = "SELECT * FROM transacciones"
    params = []
    
    if fecha_inicio is not None or fecha_fin is not None:
        conditions = []
        if fecha_inicio is not None:
            conditions.append("fecha >= ?")
            params.append(str(fecha_inicio))
        if fecha_fin is not None:
            conditions.append("fecha <= ?")
            params.append(str(fecha_fin))
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY fecha DESC"
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df

def insertar(fecha, titulo, categorias, tipo, monto, notas="", metodo="efectivo"):
    conn = get_conn()
    # Convertir lista de categorías a JSON
    categorias_json = json.dumps(categorias) if isinstance(categorias, list) else categorias
    conn.execute(
        "INSERT INTO transacciones (fecha, titulo, categoria, tipo, monto, notas, metodo) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (fecha, titulo, categorias_json, tipo, monto, notas, metodo)
    )
    conn.commit()
    conn.close()

def eliminar(id):
    conn = get_conn()
    conn.execute("DELETE FROM transacciones WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def seed_db():
    """Inserta datos de prueba en la base de datos basados en presupuesto realista
    Ingreso: 500,000 (Salario)
    Gasto mayor: 200,000 (Alquiler)
    Otros gastos: 290,000
    Balance final: 10,000
    """
    datos_prueba = [
        # Ingreso
        ("2026-04-05", "Salario", json.dumps(["Salario"]), "Ingreso", 500000, "Pago mensual", "transferencia"),
        # Gastos - Total 490,000 para dejar balance de 10,000
        ("2026-04-01", "Alquiler", json.dumps(["Alquiler"]), "Gasto", 200000, "Renta mensual", "transferencia"),
        ("2026-04-08", "Supermercado", json.dumps(["Super"]), "Gasto", 50000, "Compra de víveres", "efectivo"),
        ("2026-04-10", "Restaurantes", json.dumps(["Restaurantes"]), "Gasto", 40000, "", "tarjeta"),
        ("2026-04-12", "Transporte", json.dumps(["Transporte"]), "Gasto", 30000, "Gasolina y mantenimiento", "efectivo"),
        ("2026-04-14", "Deuda", json.dumps(["Deuda"]), "Gasto", 50000, "Pago de préstamo", "transferencia"),
        ("2026-04-16", "Entretenimiento", json.dumps(["Entretenimiento"]), "Gasto", 20000, "Actividades recreativas", "tarjeta"),
        ("2026-04-18", "Inversión", json.dumps(["Inversión"]), "Gasto", 50000, "Fondo de inversión", "transferencia"),
        ("2026-04-17", "Compras", json.dumps(["Compras"]), "Gasto", 50000, "Compras en línea", "tarjeta"),
    ]
    
    conn = get_conn()
    for dato in datos_prueba:
        conn.execute(
            "INSERT INTO transacciones (fecha, titulo, categoria, tipo, monto, notas, metodo) VALUES (?, ?, ?, ?, ?, ?, ?)",
            dato
        )
    conn.commit()
    conn.close()
