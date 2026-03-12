import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="KPIs Financial Review", layout="wide", page_icon="🟡")

# 2. CSS Simple: Estético pero sin complicaciones de posición
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    /* Fuente Global */
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }

    /* Banner Superior Estilo MeLi (No Sticky) */
    .header-banner {
        background-color: #FFE600;
        color: #2D3277;
        text-align: center;
        padding: 50px 20px;
        margin: -60px -50px 30px -50px; /* Elimina márgenes de Streamlit para cubrir el ancho */
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    }
    
    .header-banner h1 {
        margin: 0;
        font-weight: 700;
        font-size: 2.5rem;
    }
    
    .header-banner p {
        margin: 10px 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }

    /* Estilo para las cajas de código */
    .stCode {
        border-radius: 10px !important;
        border: 1px solid #f0f0f0 !important;
    }
    </style>
    
    <div class="header-banner">
        <h1>📊 KPIs Financial Review</h1>
        <p>Repositorio centralizado de queries estratégicas</p>
    </div>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS DE QUERIES (Aquí editas tus 20+ queries)
queries_db = {
    "Ventas Netas por Canal": {
        "desc": "Muestra el GMV (Gross Merchandise Volume) filtrado por marketplace y tipo de envío.",
        "sql": "SELECT canal, SUM(price) FROM orders WHERE status = 'delivered' GROUP BY 1;"
    },
    "Tasa de Cancelación": {
        "desc": "Calcula el porcentaje de órdenes canceladas vs totales por mes.",
        "sql": "SELECT date_trunc('month', created_at), avg(case when status='cancelled' then 1 else 0 end) FROM orders GROUP BY 1;"
    }
}

# 4. SIDEBAR CON BUSCADOR
st.sidebar.title("🔍 Buscador")
opcion = st.sidebar.selectbox(
    "Selecciona una consulta:", 
    options=list(queries_db.keys())
)

# 5. CONTENIDO PRINCIPAL
st.markdown(f"## {opcion}")
st.write(queries_db[opcion]["desc"])

with st.expander("📂 Ver Código SQL", expanded=True):
    st.code(queries_db[opcion]["sql"], language="sql")

st.divider()

# 6. FEEDBACK
st.subheader("💬 Feedback")
st.link_button("Sugerir cambio en esta Query", "https://forms.google.com")
