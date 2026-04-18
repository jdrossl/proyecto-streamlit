import streamlit as st
from datetime import datetime
from db import insertar

CATEGORIAS = {
    "Gasto": ["Super", "Restaurantes", "Transporte", "Deuda", "Entretenimiento", "Otro"],
    "Ingreso": ["Salario", "Freelance", "Otro"]
}

def show():
    st.subheader("Registrar transacción")

    tipo = st.radio("Tipo", ["Gasto", "Ingreso"], horizontal=True)
    titulo = st.text_input("Título")
    categorias = st.multiselect("Categorías", CATEGORIAS[tipo])
    monto = st.number_input("Monto (₡)", min_value=0.0, step=500.0)

    # Inicializar variables con valores por defecto
    fecha = datetime.now().date()
    notas = ""
    metodo = "efectivo"
    
    with st.expander("Avanzado"):
        fecha = st.date_input("Fecha", value=datetime.now())
        notas = st.text_area("Notas", placeholder="Agregar notas opcionales...")
        metodo = st.selectbox("Método de pago", ["efectivo", "transferencia", "sinpe", "tarjeta"])

    if st.button("Guardar", type="primary"):
        if titulo and monto > 0 and categorias:
            insertar(str(fecha), titulo, categoria, tipo, monto, notas, metodo)
            st.success("✅ Transacción guardada correctamente!")
            # Cambiar a la pestaña de Transacciones después de 5 segundos
            st.session_state.tab_index = 0
            import time
            time.sleep(2)
            st.rerun()
        else:
            st.warning("Completá el título y el monto.")
