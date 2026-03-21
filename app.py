import sys
from pathlib import Path

import streamlit as st

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from db import init_db
from reporte import show as reporte_show
from transacciones import show as transacciones_show
from nueva import show as nueva_show

init_db()

st.title("💰 Finanzas Personales")

tabs = st.tabs(["Transacciones", "Reporte", "Nueva"])

with tabs[0]:
    transacciones_show()

with tabs[1]:
    reporte_show()

with tabs[2]:
    nueva_show()
