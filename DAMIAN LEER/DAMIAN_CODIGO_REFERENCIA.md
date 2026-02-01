# 🚀 DAMIÁN - Referencia Rápida de Código

> Todos los fragmentos de código que necesitas. Copia y pega directamente.

---

## 📄 Archivo 1: `streamlit_app/.env`

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=sensordata
```

**Ubicación**: `streamlit_app/.env`

---

## 📄 Archivo 2: `streamlit_app/utils/__init__.py`

```python
# Archivo vacío - solo para marcar como módulo Python
```

**Ubicación**: `streamlit_app/utils/__init__.py`

---

## 📄 Archivo 3: `streamlit_app/utils/db_connection.py`

```python
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno
load_dotenv()

@st.cache_resource
def get_db_connection():
    """
    Obtiene una conexión a la base de datos PostgreSQL.
    Usa st.cache_resource para evitar crear múltiples conexiones.
    """
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_NAME", "sensordata")
        )
        return connection
    except Exception as e:
        st.error(f"❌ Error conectando a la base de datos: {e}")
        return None

def query_data(query, params=None):
    """
    Ejecuta una consulta SQL y retorna los resultados como DataFrame.
    """
    connection = get_db_connection()
    if connection is None:
        return None
    
    try:
        df = pd.read_sql(query, connection, params=params)
        return df
    except Exception as e:
        st.error(f"❌ Error ejecutando consulta: {e}")
        return None

def get_int_data(hours=1):
    """
    Obtiene datos de tipo entero de las últimas N horas.
    """
    query = """
    SELECT id, topic, value, timestamp
    FROM lake_raw_data_int
    WHERE timestamp >= NOW() - INTERVAL '%s hours'
    ORDER BY timestamp ASC
    """
    return query_data(query, (hours,))

def get_float_data(hours=1):
    """
    Obtiene datos de tipo flotante de las últimas N horas.
    """
    query = """
    SELECT id, topic, value, timestamp
    FROM lake_raw_data_float
    WHERE timestamp >= NOW() - INTERVAL '%s hours'
    ORDER BY timestamp ASC
    """
    return query_data(query, (hours,))

def get_stats_int(hours=1):
    """
    Obtiene estadísticas de datos enteros.
    """
    query = """
    SELECT 
        COUNT(*) as total,
        AVG(value) as promedio,
        MIN(value) as minimo,
        MAX(value) as maximo,
        STDDEV(value) as desv_std
    FROM lake_raw_data_int
    WHERE timestamp >= NOW() - INTERVAL '%s hours'
    """
    return query_data(query, (hours,))

def get_stats_float(hours=1):
    """
    Obtiene estadísticas de datos flotantes.
    """
    query = """
    SELECT 
        COUNT(*) as total,
        AVG(value) as promedio,
        MIN(value) as minimo,
        MAX(value) as maximo,
        STDDEV(value) as desv_std
    FROM lake_raw_data_float
    WHERE timestamp >= NOW() - INTERVAL '%s hours'
    """
    return query_data(query, (hours,))
```

**Ubicación**: `streamlit_app/utils/db_connection.py`

---

## 📄 Archivo 4: `streamlit_app/app.py`

```python
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from utils.db_connection import get_int_data, get_float_data, get_stats_int, get_stats_float

# Configuración de Streamlit
st.set_page_config(
    page_title="IoT Dashboard - MQTT Data",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
    .main-title {
        color: #1f77b4;
        text-align: center;
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    .status-online {
        color: #2ecc71;
        font-weight: bold;
    }
    .status-offline {
        color: #e74c3c;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown('<div class="main-title">📊 Dashboard IoT - MQTT Data Ingestion</div>', unsafe_allow_html=True)

# Barra lateral - Filtros
with st.sidebar:
    st.header("⚙️ Configuración")
    
    time_range = st.selectbox(
        "Rango de tiempo",
        options=[
            ("Últimos 5 minutos", 0.083),  # 5 min ≈ 0.083 horas
            ("Última 1 hora", 1),
            ("Últimas 4 horas", 4),
            ("Últimas 24 horas", 24),
            ("Últimos 7 días", 168)
        ],
        format_func=lambda x: x[0]
    )
    
    hours_to_fetch = time_range[1]
    
    # Botón para refrescar
    if st.button("🔄 Refrescar Datos", use_container_width=True):
        st.cache_resource.clear()
        st.rerun()
    
    st.markdown("---")
    st.info("ℹ️ Los datos se actualizan cada 2 segundos en el backend.\nHaz clic en 'Refrescar' para ver cambios.")

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📈 Datos en Vivo", "📊 Estadísticas", "ℹ️ Información"])

# ===================== TAB 1: DATOS EN VIVO =====================
with tab1:
    col1, col2 = st.columns(2)
    
    # Gráfica de Datos Enteros
    with col1:
        st.subheader("🔢 Datos Enteros (Integer)")
        
        df_int = get_int_data(hours_to_fetch)
        
        if df_int is not None and not df_int.empty:
            st.write(f"📍 Registros: {len(df_int)}")
            
            # Gráfica interactiva con Plotly
            fig_int = go.Figure()
            fig_int.add_trace(go.Scatter(
                x=df_int['timestamp'],
                y=df_int['value'],
                mode='lines+markers',
                name='Datos Enteros',
                line=dict(color='#1f77b4', width=2),
                marker=dict(size=6)
            ))
            
            fig_int.update_layout(
                title="Serie de Tiempo - Valores Enteros",
                xaxis_title="Tiempo",
                yaxis_title="Valor",
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig_int, use_container_width=True)
            
            # Mostrar últimos registros
            with st.expander("📋 Ver últimos registros"):
                st.dataframe(df_int.tail(10), use_container_width=True)
        else:
            st.warning("No hay datos disponibles para el rango seleccionado")
    
    # Gráfica de Datos Flotantes
    with col2:
        st.subheader("🔢 Datos Flotantes (Float)")
        
        df_float = get_float_data(hours_to_fetch)
        
        if df_float is not None and not df_float.empty:
            st.write(f"📍 Registros: {len(df_float)}")
            
            # Gráfica interactiva con Plotly
            fig_float = go.Figure()
            fig_float.add_trace(go.Scatter(
                x=df_float['timestamp'],
                y=df_float['value'],
                mode='lines+markers',
                name='Datos Flotantes',
                line=dict(color='#ff7f0e', width=2),
                marker=dict(size=6)
            ))
            
            fig_float.update_layout(
                title="Serie de Tiempo - Valores Flotantes",
                xaxis_title="Tiempo",
                yaxis_title="Valor",
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig_float, use_container_width=True)
            
            # Mostrar últimos registros
            with st.expander("📋 Ver últimos registros"):
                st.dataframe(df_float.tail(10), use_container_width=True)
        else:
            st.warning("No hay datos disponibles para el rango seleccionado")

# ===================== TAB 2: ESTADÍSTICAS =====================
with tab2:
    st.subheader("📊 Estadísticas por Tipo de Dato")
    
    col1, col2 = st.columns(2)
    
    # Estadísticas de Enteros
    with col1:
        st.markdown("### 🔢 Datos Enteros")
        
        stats_int = get_stats_int(hours_to_fetch)
        
        if stats_int is not None and not stats_int.empty:
            stats_int = stats_int.iloc[0]
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Total", f"{int(stats_int['total'])}", help="Total de registros")
                st.metric("Promedio", f"{stats_int['promedio']:.2f}", help="Valor promedio")
            
            with metric_col2:
                st.metric("Mínimo", f"{int(stats_int['minimo'])}", help="Valor mínimo")
                st.metric("Máximo", f"{int(stats_int['maximo'])}", help="Valor máximo")
            
            st.metric("Desv. Estándar", f"{stats_int['desv_std']:.2f}", help="Desviación estándar")
        else:
            st.warning("No hay datos para calcular estadísticas")
    
    # Estadísticas de Flotantes
    with col2:
        st.markdown("### 🔢 Datos Flotantes")
        
        stats_float = get_stats_float(hours_to_fetch)
        
        if stats_float is not None and not stats_float.empty:
            stats_float = stats_float.iloc[0]
            
            metric_col1, metric_col2 = st.columns(2)
            with metric_col1:
                st.metric("Total", f"{int(stats_float['total'])}", help="Total de registros")
                st.metric("Promedio", f"{stats_float['promedio']:.2f}", help="Valor promedio")
            
            with metric_col2:
                st.metric("Mínimo", f"{stats_float['minimo']:.2f}", help="Valor mínimo")
                st.metric("Máximo", f"{stats_float['maximo']:.2f}", help="Valor máximo")
            
            st.metric("Desv. Estándar", f"{stats_float['desv_std']:.2f}", help="Desviación estándar")
        else:
            st.warning("No hay datos para calcular estadísticas")

# ===================== TAB 3: INFORMACIÓN =====================
with tab3:
    st.markdown("""
    ## 📋 Información del Proyecto
    
    ### Arquitectura
    
    Este dashboard se conecta a un sistema IoT que utiliza:
    
    - **MQTT Broker**: Eclipse Mosquitto (local en Docker)
    - **Publisher**: Genera datos cada 2 segundos
      - Tópico `lake/raw/int`: Valores enteros (0-1000)
      - Tópico `lake/raw/float`: Valores decimales (0-100)
    - **Subscriber**: Recibe datos y los almacena en PostgreSQL
    - **Base de Datos**: PostgreSQL 13
      - Tabla: `lake_raw_data_int`
      - Tabla: `lake_raw_data_float`
    
    ### Variables de Entorno
    
    El dashboard usa las siguientes variables (en `.env`):
    
    ```
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=user
    DB_PASSWORD=password
    DB_NAME=sensordata
    ```
    
    ### Filtros Disponibles
    
    - **Últimos 5 minutos**: Muestra solo datos de los últimos 5 minutos
    - **Última 1 hora**: Muestra datos de la última hora
    - **Últimas 4 horas**: Muestra datos de las últimas 4 horas
    - **Últimas 24 horas**: Muestra datos del último día
    - **Últimos 7 días**: Muestra datos de la última semana
    
    ### Estadísticas Mostradas
    
    Para cada tipo de dato:
    - **Total**: Cantidad de registros
    - **Promedio**: Valor medio
    - **Mínimo**: Valor más bajo
    - **Máximo**: Valor más alto
    - **Desv. Estándar**: Desviación estándar
    """)
```

**Ubicación**: `streamlit_app/app.py`

---

## 🔧 Comandos para Ejecutar

### Instalar dependencias
```bash
pip install streamlit plotly pandas psycopg2-binary python-dotenv
```

### Ejecutar la app
```bash
cd streamlit_app
streamlit run app.py
```

### Ver logs de Docker
```bash
docker-compose logs -f subscriber
docker-compose logs -f postgres
```

### Verificar estado de servicios
```bash
docker-compose ps
```

---

## 📂 Estructura Final

```
streamlit_app/
├── .env                      ← CREAR
├── app.py                    ← CREAR
├── Dockerfile                ✅ Ya existe
├── requirements.txt          ✅ Ya existe
├── utils/
│   ├── __init__.py          ← CREAR (vacío)
│   └── db_connection.py     ← CREAR
└── pages/
    ├── __init__.py          (opcional)
    └── (adicionales)        (opcional)
```

---

## ✅ Resumen

1. **Copia el contenido** de cada archivo arriba
2. **Créa los 4 archivos** en las ubicaciones indicadas
3. **Ejecuta**: `streamlit run streamlit_app/app.py`
4. **Abre**: http://localhost:8501

¡Listo! 🚀
