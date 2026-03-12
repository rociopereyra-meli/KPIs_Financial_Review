import streamlit as st

# 1. Configuración de página
st.set_page_config(page_title="KPIs Financial Review", layout="wide", page_icon="🟡")

# 2. CSS Mejorado: Título Centrado y Logo a la Derecha
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    /* Fuente Global */
    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }

    /* Banner Superior Estilo MeLi */
    .header-banner {
        background-color: #FFE600;
        color: #2D3277;
        text-align: center;
        padding: 50px 20px;
        margin: -60px -50px 30px -50px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        position: relative; /* Necesario para ubicar el logo adentro */
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

    /* Logo posicionado a la derecha sin afectar el centro */
    .logo-meli {
        position: absolute;
        right: 50px;
        top: 50%;
        transform: translateY(-50%); /* Centra el logo verticalmente respecto a la franja */
        height: 45px;
    }

    /* Estilo para las cajas de código */
    .stCode {
        border-radius: 10px !important;
        border: 1px solid #f0f0f0 !important;
    }
    </style>
    
    <div class="header-banner">
        <h1>KPIs Financial Review</h1>
        <p>Repositorio de queries para la carga de KPIs utilizados en el FR</p>
        <img src="https://http2.mlstatic.com/frontend-assets/ml-web-navigation/ui-navigation/5.21.22/mercadolibre/logo__large_plus@2x.png" class="logo-meli">
    </div>
    """, unsafe_allow_html=True)

# 3. BASE DE DATOS DE QUERIES (Aquí editas tus 20+ queries)
queries_db = {
    "KPIs FR - Economics": {
        "desc": "Muestra los KPIs: SIs,  SHPs,  SIs/SHPs,  CPS,  RPS,  GMV,  NR,  RPS/GMV,  CPS/GMV, y % SIs FBM ",
        "sql": """CREATE OR REPLACE TABLE meli-bi-data.SBOX_SHPCDG.KPI_FR_ECONOMICS AS (

WITH data_preparada AS (
  SELECT
    SIT_SITE_ID,
    SHP_MONTH_HANDLING AS MONTH,
    SHP_PICKING_TYPE_ID_AGG AS PICKING_TYPE,
    HORIZONTE ,

    SUM(Q_SHP) AS SHP, 
    SUM(SIS) AS SIS,
    
    -- Revenue Total
    SUM(IFNULL(REV_REAL,0) + IFNULL(AGING,0) + IFNULL(RESTO_FBM_CHARGES,0)) AS REVENUE,
    
    -- Costo Total
    SUM(IFNULL(TRANSFERENCES_COST,0) + IFNULL(TOTAL_COST,0)) AS COSTO,
    
    -- GMV
    SUM(IFNULL(GMV,0)) AS GMV_VAL,
    
    -- Net Revenue
    SUM( (IFNULL(REV_REAL,0) + IFNULL(AGING,0) + IFNULL(RESTO_FBM_CHARGES,0)) - (IFNULL(TRANSFERENCES_COST,0) + IFNULL(TOTAL_COST,0)) ) AS NET_REVENUE

  FROM `meli-bi-data.SBOX_SHPCDG.BAJADA_WATERFALL_ME`
  WHERE 1=1
    AND SHP_MONTH_HANDLING >= 202506
    AND CURRENCY = 'LOCAL'
  GROUP BY 1, 2, 3, 4
)

-- 1. TOTAL SITE 
SELECT 
    MONTH, 
    SIT_SITE_ID AS SITE,   
    HORIZONTE ,
    'SI_TOT' AS KPI_CODE,  
    'SIs' AS KPI_NAME,
    SUM(SIS) AS NUMERADOR, 
    1 AS DENOMINADOR,
    SAFE_DIVIDE(SUM(SIS),1) AS KPI_VALUE 
FROM data_preparada GROUP BY 1,2,3

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    'SHP_TOT', 
    'SHPs', 
    SUM(SHP), 
    1, 
    SAFE_DIVIDE(SUM(SHP),1) 
FROM data_preparada GROUP BY 1,2,3

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    'CPS', 
    'CPS', 
    SUM(COSTO), 
    SUM(SHP), 
    SAFE_DIVIDE(SUM(COSTO), SUM(SHP)) 
FROM data_preparada GROUP BY 1,2,3

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    'RPS+FF', 
    'RPS', 
    SUM(REVENUE), 
    SUM(SHP), 
    SAFE_DIVIDE(SUM(REVENUE), SUM(SHP)) 
FROM data_preparada GROUP BY 1,2,3

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    'GMV_SHP', 
    'GMV/SHP', 
    SUM(GMV_VAL), 
    SUM(SHP), 
    SAFE_DIVIDE(SUM(GMV_VAL), SUM(SHP)) 
FROM data_preparada GROUP BY 1,2,3

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    'CPS_GMV', 
    'CPS/GMV', 
    SUM(COSTO), 
    SUM(GMV_VAL), 
    SAFE_DIVIDE(SUM(COSTO), SUM(GMV_VAL)) 
FROM data_preparada GROUP BY 1,2,3

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    'NR+FF/GMV', 
    'OSM', 
    SUM(NET_REVENUE), 
    SUM(GMV_VAL), 
    SAFE_DIVIDE(SUM(NET_REVENUE), SUM(GMV_VAL)) 
FROM data_preparada GROUP BY 1,2,3

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    'RPS_GMV', 
    'RPS/GMV', 
    SUM(REVENUE), 
    SUM(GMV_VAL), 
    SAFE_DIVIDE(SUM(REVENUE), SUM(GMV_VAL)) 
FROM data_preparada GROUP BY 1,2,3

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    'SI_SHP', 
    'SI/SHP', 
    SUM(SIS), 
    SUM(SHP), 
    SAFE_DIVIDE(SUM(SIS), SUM(SHP)) 
FROM data_preparada GROUP BY 1,2,3

UNION ALL

-- 2. BY PICKING TYPE
SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    CONCAT('SI_', PICKING_TYPE), 
    CONCAT('SIs ', PICKING_TYPE), 
    SUM(SIS), 
    1, 
    SAFE_DIVIDE(SUM(SIS),1) 
FROM data_preparada GROUP BY 1,2,3,PICKING_TYPE

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE , 
    CONCAT('SHP_', PICKING_TYPE), 
    CONCAT('SHPs ', PICKING_TYPE), 
    SUM(SHP), 
    1, 
    SAFE_DIVIDE(SUM(SHP),1) 
FROM data_preparada GROUP BY 1,2,3,PICKING_TYPE

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    CONCAT('CPS_', PICKING_TYPE), 
    CONCAT('CPS ', PICKING_TYPE), 
    SUM(COSTO), 
    SUM(SHP), 
    SAFE_DIVIDE(SUM(COSTO), SUM(SHP)) 
FROM data_preparada GROUP BY 1,2,3,PICKING_TYPE

UNION ALL

SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    CONCAT('SI_SHP_', PICKING_TYPE), 
    CONCAT('SIs/SHP ', PICKING_TYPE), 
    SUM(SIS), 
    SUM(SHP), 
    SAFE_DIVIDE(SUM(SIS), SUM(SHP)) 
FROM data_preparada GROUP BY 1,2,3,PICKING_TYPE

UNION ALL

-- 3. % SIs FBM
SELECT 
    MONTH, 
    SIT_SITE_ID, 
    HORIZONTE ,
    'SHARE_SIS_FBM', 
    '% SIs FBM', 
    SUM(CASE WHEN PICKING_TYPE = 'FBM' THEN SIS ELSE 0 END) AS NUMERADOR, 
    SUM(SIS) AS DENOMINADOR, 
    SAFE_DIVIDE( SUM(CASE WHEN PICKING_TYPE = 'FBM' THEN SIS ELSE 0 END), SUM(SIS)) AS KPI_VALUE
FROM data_preparada 
GROUP BY 1,2,3
ORDER BY 1, 2, 3, 4) ;"""

    },
    "KPIs FR - from ME Excecutive": {
        "desc": "Trae los KPis del Dashboard ME Excecutive : Net Productivity XD y Net Productivity SVC , Ratio In/Out , Cap5  y % Box ",
        "sql": """"CREATE OR REPLACE TABLE meli-bi-data.SBOX_SHPCDG.KPIs_ME_FR AS (

SELECT 
  CAST (YEAR_MONTH AS STRING) AS MONTH_HANDLING,
  SITE_ID AS SIT_SITE_ID,   
  'REAL' AS HORIZONTE,
  KPI_CODE AS METRIC_NAME,
  KPI_NAME AS Descripcion, 
  NUMERADOR AS NUMERATOR,
  DENOMINADOR AS DENOMINATOR,
  SAFE_DIVIDE(NUMERADOR,DENOMINADOR) AS KPI_VALUE
FROM `meli-bi-data.WHOWNER.DM_SHP_ME_EXECUTIVE_SUMMARY` A
LEFT JOIN `meli-bi-data.WHOWNER.LK_SHP_CDG_CALENDAR` B
  ON A.DATE_VALUE = B.MONTH_START_DATE 
WHERE 1 = 1                         
  AND SITE_ID IN ('MLB','MLM', 'MLA','MLC','MCO','MLU')
  AND DATE_UNIT IN ('MONTH')  
  AND KPI_NAME IN ( 'Global Net Productivity XD',
                    'Global Net Productivity SVC',
                    'Ratio In/Out FBM Procesado',
                    'Buffering FBM (Cap 5) Fast',
                    'Share Cajas'
                    )

  AND DATE_VALUE >= '2024-01-01'
GROUP BY ALL );"""
    }

    ,
    "Tasa de Cancelación": {
        "desc": "Calcula el porcentaje de órdenes canceladas vs totales por mes.",
        "sql": "SELECT date_trunc('month', created_at), avg(case when status='cancelled' then 1 else 0 end) FROM orders GROUP BY 1;"
    }

    ,
    "Tasa de Cancelación": {
        "desc": "Calcula el porcentaje de órdenes canceladas vs totales por mes.",
        "sql": "SELECT date_trunc('month', created_at), avg(case when status='cancelled' then 1 else 0 end) FROM orders GROUP BY 1;"
    }

    ,
    "Tasa de Cancelación": {
        "desc": "Calcula el porcentaje de órdenes canceladas vs totales por mes.",
        "sql": "SELECT date_trunc('month', created_at), avg(case when status='cancelled' then 1 else 0 end) FROM orders GROUP BY 1;"
    }

    ,
    "Tasa de Cancelación": {
        "desc": "Calcula el porcentaje de órdenes canceladas vs totales por mes.",
        "sql": "SELECT date_trunc('month', created_at), avg(case when status='cancelled' then 1 else 0 end) FROM orders GROUP BY 1;"
    }

    ,
    "Tasa de Cancelación": {
        "desc": "Calcula el porcentaje de órdenes canceladas vs totales por mes.",
        "sql": "SELECT date_trunc('month', created_at), avg(case when status='cancelled' then 1 else 0 end) FROM orders GROUP BY 1;"
    }

    ,
    "Tasa de Cancelación": {
        "desc": "Calcula el porcentaje de órdenes canceladas vs totales por mes.",
        "sql": "SELECT date_trunc('month', created_at), avg(case when status='cancelled' then 1 else 0 end) FROM orders GROUP BY 1;"
    }
    
}
# 4. SIDEBAR CON BUSCADOR
st.sidebar.title("🔍 Buscador")
opcion = st.sidebar.selectbox(
    "Selecciona una query:", 
    options=list(queries_db.keys())
)

# 5. CONTENIDO PRINCIPAL (Sin el índice, directo al grano)
st.markdown(f"## {opcion}")
st.info(queries_db[opcion]["desc"])

with st.expander("📂 Ver Código SQL", expanded=True):
    st.code(queries_db[opcion]["sql"], language="sql")

st.divider()
