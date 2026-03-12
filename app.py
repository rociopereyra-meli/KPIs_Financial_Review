import streamlit as st

# 1. Configuración de la página (DEBE SER LA PRIMERA LÍNEA DE STREAMLIT)
st.set_page_config(page_title="KPIs Financial Review", layout="wide", page_icon="📊")

# 2. Título principal
st.title("📊 KPIs Financial Review")
st.markdown("Repositorio centralizado de queries. Selecciona una opción a la izquierda.")

# 3. Diccionario de Queries (Aquí es donde editas/agregas tus 20+ queries)
# Estructura: "Nombre": ["Descripción", "Código SQL"]
queries = {
    "Ingresos Trimestrales": [
        "Extrae el total de ingresos agrupado por trimestre fiscal.",
        "SELECT quarter, SUM(revenue) FROM financial_table GROUP BY 1;"
    ],
    "Margen de Ganancia": [
        "Calcula el porcentaje de margen operativo mensual.",
        "SELECT month, (revenue - costs) / revenue AS margin FROM data;"
    ],
    "Gastos por Departamento": [
        "Desglose de gastos operativos por área.",
        "SELECT dept, SUM(expense) FROM expenses GROUP BY dept;"
    ]
}

# 4. Menú Lateral (Sidebar)
st.sidebar.header("🔍 Buscador de Queries")
lista_titulos = list(queries.keys())
seleccion = st.sidebar.selectbox("Selecciona una métrica:", lista_titulos)

# 5. Mostrar Contenido Seleccionado
st.header(f"Métrica: {seleccion}")

# Mostramos la descripción (primer elemento de la lista)
st.info(queries[seleccion][0])

# Mostramos el código (segundo elemento de la lista)
st.subheader("Código SQL")
st.code(queries[seleccion][1], language='sql')

# 6. Pie de página y Comentarios
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.write("¿Necesitas un ajuste en esta query?")
    # REEMPLAZA EL LINK DE ABAJO CON TU GOOGLE FORM REAL
    st.link_button("💬 Dejar comentario o sugerencia", "https://forms.google.com")

with col2:
    st.caption("Actualizado por última vez: Marzo 2024")
    st.caption("Acceso restringido - Solo lectura")
