import streamlit as st
from .db import init_db
from . import inicio, transacciones, nueva

init_db()

st.title("💰 Finanzas Personales")

tabs = st.tabs(["Inicio", "Transacciones", "Nueva"])

with tabs[0]:
    inicio.show()

with tabs[1]:
    transacciones.show()

with tabs[2]:
    nueva.show()
