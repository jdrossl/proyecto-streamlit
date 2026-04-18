import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
from datetime import datetime
from babel.dates import format_date
from db import get_transacciones

def show():
    col1, col2 = st.columns(2)
    with col1:
        fecha_inicio = st.date_input("Desde", value=datetime(datetime.now().year, datetime.now().month, 1))
    with col2:
        fecha_fin = st.date_input("Hasta", value=datetime.now())
    
    # Mostrar título con el rango de fechas en español
    titulo_fecha = f"{format_date(fecha_inicio, 'd de MMMM', locale='es_ES')} - {format_date(fecha_fin, 'd de MMMM de y', locale='es_ES')}"
    st.subheader(f"Resumen: {titulo_fecha}")
    
    df = get_transacciones(fecha_inicio, fecha_fin)

    if df.empty:
        st.info("Aún no hay transacciones registradas.")
        return

    ingresos = df[df["tipo"] == "Ingreso"]["monto"].sum()
    gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
    balance = ingresos - gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos", f"₡{ingresos:,.0f}")
    col2.metric("Gastos", f"₡{gastos:,.0f}")
    
    balance_emoji = "🟢" if balance > 0 else "🟡" if balance == 0 else "🔴"
    col3.metric(f"Balance {balance_emoji}", f"₡{balance:,.0f}", delta=f"₡{balance:,.0f}")

    gastos_df = df[df["tipo"] == "Gasto"]
    if not gastos_df.empty:
        st.subheader("Gastos por categoría")
        por_categoria = {}
        
        # Procesar cada transacción
        for _, row in gastos_df.iterrows():
            try:
                categorias = json.loads(row["categoria"])
            except (json.JSONDecodeError, TypeError):
                categorias = [row["categoria"]]
            
            # Distribuir el monto entre las categorías de esa transacción
            monto_por_categoria = row["monto"] / len(categorias)
            for cat in categorias:
                por_categoria[cat] = por_categoria.get(cat, 0) + monto_por_categoria
        
        if por_categoria:
            fig = go.Figure(data=[go.Pie(labels=list(por_categoria.keys()), values=list(por_categoria.values()))])
            st.plotly_chart(fig, use_container_width=True)
