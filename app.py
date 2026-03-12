import streamlit as st

# 1. Configuración estética
st.set_page_config(page_title="KPIs Financial Review", layout="wide", page_icon="📊")

# Estilo personalizado para que se vea más prolijo
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stCode {
        border: 1px solid #e6e9ef;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_status=True)

# 2. Título y encabezado
st.title("📊 KPIs Financial Review")
st.markdown("Bienvenido al repositorio central de queries financieras. Selecciona una métrica en el menú lateral para ver el código.")

# 3. Diccionario de Queries (Aquí puedes agregar tus 20+ queries)
queries = {
    "Ingresos Totales por Q": {
        "desc": "Calcula la sumatoria de ingresos brutos agrupados por trimestre fiscal.",
        "code": "SELECT quarter, SUM(revenue) as total_revenue \nFROM financial_table \nGROUP BY 1 \nORDER BY 1 DESC;"
    },
    "Margen Operativo": {
        "desc": "Métrica para analizar la eficiencia operativa restando COGS y Gastos.",
        "code": "SELECT date, (total_revenue - cogs - operating_expenses) / total_revenue as margin \nFROM monthly_reports;"
    },
    # Agrega más aquí siguiendo el mismo formato
}

# 4. Sidebar (Menú Lateral)
st.sidebar.header("Navegación")
query_sel = st.sidebar.selectbox("Selecciona una métrica:", list(queries.keys()))

# 5. Visualización de la Query Seleccionada
st.subheader(f"Métrica: {query_sel}")
st.info(queries[query_sel]["desc"])

# El bloque de código SQL
st.code(queries[query_sel]["code"], language='sql')

# 6. Sección de Comentarios (CORREGIDO)
st.markdown("---") # Esta es la forma correcta de poner la línea en Streamlit
st.subheader("💬 Feedback y Comentarios")
st.write("¿Tienes alguna duda sobre esta query o necesitas un ajuste?")

# Botón interactivo para comentarios
contact_url = "https://forms.gle/TU_URL_DE_GOOGLE_FORMS" # Cambia esto por tu link
st.link_button("Dejar un comentario / Sugerencia", contact_url)

st.caption("Mantenido por el equipo de Finanzas | 2024")
