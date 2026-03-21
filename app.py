import sys
from pathlib import Path

import streamlit as st

# Add parent directory to path to enable explicit imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ProyectoStreamlit.db import init_db
from ProyectoStreamlit import reporte, transacciones, nueva

init_db()

st.title("💰 Finanzas Personales")

tabs = st.tabs(["Transacciones", "Reporte", "Nueva"])

with tabs[0]:
    transacciones.show()

with tabs[1]:
    reporte.show()

with tabs[2]:
    nueva.show()
