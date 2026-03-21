import streamlit as st
from .db import insertar

CATEGORIAS = {
    "Gasto": ["Super", "Restaurantes", "Transporte", "Deuda", "Entretenimiento", "Otro"],
    "Ingreso": ["Salario", "Freelance", "Otro"]
}

def show():
    st.subheader("Registrar transacción")

    tipo = st.radio("Tipo", ["Gasto", "Ingreso"], horizontal=True)
    fecha = st.date_input("Fecha")
    descripcion = st.text_input("Descripción")
    categoria = st.selectbox("Categoría", CATEGORIAS[tipo])
    monto = st.number_input("Monto (₡)", min_value=0.0, step=500.0)

    if st.button("Guardar", type="primary"):
        if descripcion and monto > 0:
            insertar(str(fecha), descripcion, categoria, tipo, monto)
            st.success("✅ Transacción guardada.")
        else:
            st.warning("Completá la descripción y el monto.")
