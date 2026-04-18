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
    formato_inicio = "d 'de' MMMM"
    formato_fin = "d 'de' MMMM 'de' y"
    titulo_fecha = f"{format_date(fecha_inicio, formato_inicio, locale='es_ES')} - {format_date(fecha_fin, formato_fin, locale='es_ES')}"
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
        # Procesar categorías
        por_categoria_primera = {}
        por_categoria_todas = {}
        
        for _, row in gastos_df.iterrows():
            try:
                categorias = json.loads(row["categoria"])
            except (json.JSONDecodeError, TypeError):
                categorias = [row["categoria"]]
            
            # Para pastel: contar solo la primera categoría
            primera_cat = categorias[0] if categorias else "Otro"
            por_categoria_primera[primera_cat] = por_categoria_primera.get(primera_cat, 0) + row["monto"]
            
            # Para barras: sumar todas las categorías sin distribuir
            for cat in categorias:
                por_categoria_todas[cat] = por_categoria_todas.get(cat, 0) + row["monto"]
        
        # Gráficos lado a lado
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribución (primera categoría)")
            if por_categoria_primera:
                fig_pie = go.Figure(data=[go.Pie(labels=list(por_categoria_primera.keys()), values=list(por_categoria_primera.values()))])
                st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.subheader("Total por categoría")
            if por_categoria_todas:
                categorias_sorted = sorted(por_categoria_todas.items(), key=lambda x: x[1], reverse=True)
                categories = [c[0] for c in categorias_sorted]
                values = [c[1] for c in categorias_sorted]
                
                fig_bar = go.Figure(data=[go.Bar(x=categories, y=values)])
                fig_bar.update_layout(xaxis_tickangle=-45, height=400)
                st.plotly_chart(fig_bar, use_container_width=True)
