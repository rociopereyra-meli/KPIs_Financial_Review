import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="KPIs Financial Review", layout="wide", page_icon="🟡")

# 2. CSS para Proxima Nova, Colores MeLi y Header Freezado
st.markdown("""
    <style>
    /* Importar fuente similar a Proxima Nova (Montserrat es la más parecida en Google Fonts) */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }

    /* Header Freezado / Sticky */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #FFE600;
        padding: 15px 20px;
        color: #2D3277; /* Azul oscuro típico de MeLi para contraste */
        text-align: left;
        z-index: 999;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    
    /* Espaciado para que el contenido no quede debajo del header */
    .main-content {
        margin-top: 80px;
    }

    /* Estilo para los bloques de código */
    .stCode {
        border-radius: 8px;
        border: 1px solid #e6e6e6;
    }
    
    /* Botones con estilo MeLi */
    div.stButton > button {
        background-color: #3483FA; /* Azul de botones MeLi */
        color: white;
        border-radius: 6px;
    }
    </style>
    
    <div class="sticky-header">
        <h2 style="margin:0;">📊 KPIs Financial Review</h2>
        <p style="margin:0; font-size: 0.9rem; opacity: 0.8;">Repositorio centralizado de queries estratégicas</p>
    </div>
    <div class="main-content"></div>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS DE QUERIES (Aquí es donde editas todo)
# Estructura: "Nombre Visible": {"desc": "Lo que hace", "sql": "El código"}
queries_db = {
    "Ventas Netas por Canal": {
        "desc": "Muestra el GMV (Gross Merchandise Volume) filtrado por marketplace y tipo de envío.",
        "sql": "SELECT canal, SUM(price) FROM orders WHERE status = 'delivered' GROUP BY 1;"
    },
    "Tasa de Cancelación": {
        "desc": "Calcula el porcentaje de órdenes canceladas vs totales por mes.",
        "sql": "SELECT date_trunc('month', created_at), avg(case when status='cancelled' then 1 else 0 end) FROM orders GROUP BY 1;"
    },
    "Top 10 Categorías": {
        "desc": "Ranking de categorías con mayor crecimiento interanual.",
        "sql": "SELECT category, growth_rate FROM market_trends ORDER BY growth_rate DESC LIMIT 10;"
    },
    # Para agregar más, solo copia una de estas estructuras y pégala aquí abajo.
}

# 4. BUSCADOR LATERAL (Sidebar)
st.sidebar.markdown("<br><br>", unsafe_allow_html=True) # Espacio para que no choque con el header
st.sidebar.title("🔍 Buscador")
opcion = st.sidebar.selectbox(
    "Selecciona una consulta:", 
    options=list(queries_db.keys()),
    help="Escribe o selecciona para filtrar"
)

# 5. CONTENIDO PRINCIPAL
st.markdown(f"### {opcion}")
st.write(queries_db[opcion]["desc"])

with st.expander("Ver Código SQL", expanded=True):
    st.code(queries_db[opcion]["sql"], language="sql")

# 6. SECCIÓN DE COMENTARIOS
st.divider()
st.subheader("💬 Feedback")
col1, col2 = st.columns([1, 2])
with col1:
    st.link_button("Sugerir cambio en esta Query", "https://forms.google.com", use_container_width=True)
