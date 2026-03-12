import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="KPIs Financial Review", layout="wide", page_icon="🟡")

# 2. CSS Optimizado: Equilibrio de espacios y centrado vertical
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }

    /* Header Fijo - Ajustamos el padding para centrar mejor el texto */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #FFE600;
        padding: 25px 0px 20px 0px; /* Reducido para que el texto suba dentro de la franja */
        color: #2D3277;
        text-align: center;
        z-index: 999;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        height: 130px; /* Altura más equilibrada */
    }
    
    .sticky-header h2 {
        margin: 0;
        font-weight: 700;
        font-size: 2rem;
        line-height: 1.1;
    }
    
    .sticky-header p {
        margin: 5px 0 0 0;
        font-size: 1rem;
    }

    /* Espaciador - Ajustado para eliminar el espacio muerto */
    .content-spacer {
        margin-top: 150px; /* Antes era 220, ahora sube todo el contenido */
    }

    /* Ajuste de márgenes laterales */
    .block-container {
        padding-top: 2rem !important;
        padding-left: 4rem !important;
        padding-right: 4rem !important;
    }

    /* Estilo de la caja de código */
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
