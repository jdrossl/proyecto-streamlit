import streamlit as st
import plotly.graph_objects as go
from db import get_transacciones

def show():
    st.subheader("Resumen del mes")
    df = get_transacciones()

    if df.empty:
        st.info("Aún no hay transacciones registradas.")
        return

    ingresos = df[df["tipo"] == "Ingreso"]["monto"].sum()
    gastos = df[df["tipo"] == "Gasto"]["monto"].sum()
    balance = ingresos - gastos

    col1, col2, col3 = st.columns(3)
    col1.metric("Ingresos", f"₡{ingresos:,.0f}")
    col2.metric("Gastos", f"₡{gastos:,.0f}")
    col3.metric("Balance", f"₡{balance:,.0f}", delta=f"₡{balance:,.0f}")

    gastos_df = df[df["tipo"] == "Gasto"]
    if not gastos_df.empty:
        st.subheader("Gastos por categoría")
        por_categoria = gastos_df.groupby("categoria")["monto"].sum()
        
        fig = go.Figure(data=[go.Pie(labels=por_categoria.index, values=por_categoria.values)])
        st.plotly_chart(fig, use_container_width=True)
