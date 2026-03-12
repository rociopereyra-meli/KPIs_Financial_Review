import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="KPIs Financial Review", layout="wide", page_icon="🟡")

# 2. CSS Mejorado: Centrado, Sombra y Espaciado Correcto
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }

    /* Header Fijo y Centrado */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #FFE600;
        padding: 20px 0px; /* Más padding arriba y abajo */
        color: #2D3277;
        text-align: center; /* CENTRADO */
        z-index: 999;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.15); /* Sombra más marcada */
    }
    
    .sticky-header h2 {
        margin: 0;
        font-weight: 700;
        font-size: 1.8rem;
    }
    
    .sticky-header p {
        margin: 5px 0 0 0;
        font-size: 1rem;
        opacity: 0.8;
    }

    /* Espaciador dinámico para que el contenido no se meta debajo del header */
    .content-spacer {
        margin-top: 130px; /* Ajusta este número si quieres que el título de abajo suba o baje */
    }

    /* Estilo para que la caja expandible se vea más limpia */
    .stCode {
        border-radius: 10px !important;
    }
    </style>
    
    <div class="sticky-header">
        <h2>📊 KPIs Financial Review</h2>
        <p>Repositorio centralizado de queries estratégicas</p>
    </div>
    <div class="content-spacer"></div>
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
    # Sigue agregando aquí abajo...
}

# 4. SIDEBAR CON BUSCADOR
st.sidebar.markdown("<br><br><br>", unsafe_allow_html=True)
st.sidebar.title("🔍 Buscador")
opcion = st.sidebar.selectbox(
    "Selecciona una consulta:", 
    options=list(queries_db.keys())
)

# 5. CONTENIDO PRINCIPAL (Ya centrado visualmente por el spacer)
st.markdown(f"## {opcion}")
st.write(queries_db[opcion]["desc"])

# La cajita expandible que te gustó
with st.expander("📂 Ver Código SQL", expanded=False): # Cambié a False para que empiece cerrada y sea más prolijo
    st.code(queries_db[opcion]["sql"], language="sql")

st.divider()

# 6. FEEDBACK
st.subheader("💬 Feedback")
st.link_button("Sugerir cambio en esta Query", "https://forms.google.com")
