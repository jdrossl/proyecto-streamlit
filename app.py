import sys
from pathlib import Path

import streamlit as st

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from db import init_db, seed_db
from reporte import show as reporte_show
from transacciones import show as transacciones_show
from nueva import show as nueva_show

init_db()

# Verificar query param para seed_db (solo ejecuta una vez por sesión)
if st.query_params.get("seed") == "true":
    if "seed_executed" not in st.session_state:
        seed_db()
        st.session_state.seed_executed = True
        st.success("✅ Datos de prueba agregados correctamente!")
        st.rerun()

st.title("💰 Finanzas Personales")

tabs = st.tabs(["Transacciones", "Reporte", "Nueva"])

with tabs[0]:
    transacciones_show()

with tabs[1]:
    reporte_show()

with tabs[2]:
    nueva_show()
