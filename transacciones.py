import streamlit as st
import json
from db import get_transacciones, eliminar

def show():
    st.subheader("Historial de transacciones")
    df = get_transacciones()

    if df.empty:
        st.info("No hay transacciones aún.")
        return

    for _, row in df.iterrows():
        # Parsear categorías desde JSON
        try:
            categorias = json.loads(row["categoria"])
            categoria_str = ", ".join(categorias)
        except (json.JSONDecodeError, TypeError):
            categoria_str = row["categoria"]
        
        col1, col2, col3, col4 = st.columns([2, 3, 2, 1])
        col1.write(row["fecha"])
        col2.write(f"{row['titulo']} ({categoria_str})")
        color = "🟢" if row["tipo"] == "Ingreso" else "🔴"
        col3.write(f"{color} ₡{row['monto']:,.0f}")
        if col4.button("🗑️", key=f"del_{row['id']}"):
            eliminar(row["id"])
            st.rerun()
