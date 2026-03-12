import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Mis Queries Pro", layout="wide")

st.title("🚀 Repositorio de Queries Estratégicas")
st.markdown("Consulta y copia las queries autorizadas. Deja tus comentarios abajo.")

# Diccionario con tus queries (puedes tener 20+)
queries = {
    "Ventas Mensuales": {
        "desc": "Extrae el total de ventas agrupado por mes y región.",
        "code": "SELECT month, region, SUM(sales) FROM database GROUP BY 1, 2;"
    },
    "Usuarios Activos": {
        "desc": "Calcula el DAU (Daily Active Users) de los últimos 30 días.",
        "code": "SELECT date, COUNT(distinct user_id) FROM logins WHERE date > current_date - 30 GROUP BY 1;"
    }
}

# Buscador / Selector lateral
query_sel = st.sidebar.selectbox("Selecciona una Query", list(queries.keys()))

# Mostrar contenido
st.header(f"Query: {query_sel}")
st.info(queries[query_sel]["desc"])

# Bloque de código con botón de copiar automático
st.code(queries[query_sel]["code"], language='sql')

---
# Sección de Comentarios (Simple con Google Forms o Disqus)
st.subheader("💬 Feedback y Comentarios")
st.write("¿Falta algo o encontraste un error? Déjanos tu comentario.")
# Aquí puedes embeber un link a un Google Form para que sea prolijo
st.markdown("[Haz clic aquí para dejar un comentario](URL_DE_TU_FORMULARIO)")
