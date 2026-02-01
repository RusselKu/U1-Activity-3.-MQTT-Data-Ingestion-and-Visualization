# 📊 Guía Completa para Damián - Dashboard Streamlit

> **Estado del Proyecto**: ✅ Backend completado (Rivaldo)  
> **Tu Responsabilidad**: Crear el frontend/dashboard de visualización  
> **Fecha**: Febrero 1, 2026

---

## 📋 Índice

1. [Situación Actual](#situación-actual)
2. [Tu Misión](#tu-misión)
3. [Pasos Detallados](#pasos-detallados)
4. [Estructura de Archivos](#estructura-de-archivos)
5. [Conexión a la Base de Datos](#conexión-a-la-base-de-datos)
6. [Código Base para Empezar](#código-base-para-empezar)
7. [Pruebas y Validación](#pruebas-y-validación)

---

## 🔍 Situación Actual

El backend está **100% funcional**:

✅ **MQTT Broker** (Mosquitto local)  
✅ **Publisher** - Publica datos cada 2 segundos:
  - Tópico: `lake/raw/int` → Valores enteros (0-1000)
  - Tópico: `lake/raw/float` → Valores flotantes (0-100)

✅ **Subscriber** - Recibe y almacena en PostgreSQL:
  - Tabla: `lake_raw_data_int` (96 registros ✅)
  - Tabla: `lake_raw_data_float` (98 registros ✅)

**Base de Datos PostgreSQL:**
- Host: `postgres_db` (dentro de Docker) o `localhost:5432` (desde afuera)
- Usuario: `user`
- Contraseña: `password`
- Base de datos: `sensordata`

---

## 🎯 Tu Misión

Crear un **dashboard interactivo con Streamlit** que:

1. ✏️ **Visualice datos en tiempo real** desde la base de datos PostgreSQL
2. 📈 **Muestre gráficas de series de tiempo** para ambos tipos de datos
3. 🎛️ **Permita filtrar por rango de tiempo** (últimos 5 min, 1 hora, 24 horas, personalizado)
4. 📊 **Muestre estadísticas** (promedio, máximo, mínimo, conteo)
5. 🎨 **Diseño limpio e intuitivo** con pestañas/páginas

---

## 📝 Pasos Detallados

### Paso 1: Preparar el Entorno

**1.1. Verifica que todo esté corriendo:**

```bash
docker-compose ps
```

Deberías ver:
- ✅ mosquitto → UP
- ✅ postgres_db → UP
- ✅ subscriber → UP

**1.2. Si algo no está corriendo:**

```bash
docker-compose down
docker-compose up -d
```

Espera 10 segundos a que PostgreSQL esté listo.

---

### Paso 2: Crear la Estructura del Proyecto Streamlit

**2.1. Los archivos ya existen en `streamlit_app/`:**

```
streamlit_app/
├── Dockerfile                 # ✅ Ya existe
├── requirement.txt           # ⚠️ Revisar (tiene typo: "requirement" en lugar de "requirements")
├── requirements.txt          # ✅ Ya existe
├── app.py                    # 🚫 NECESITAS CREAR ESTO
├── pages/
│   ├── __init__.py
│   ├── page1_datos_en_vivo.py     # 🚫 NECESITAS CREAR
│   └── page2_estadisticas.py      # 🚫 NECESITAS CREAR
├── utils/
│   ├── __init__.py
│   └── db_connection.py      # 🚫 NECESITAS CREAR
└── styles/
    └── custom.css            # Opcional (estilos personalizados)
```

**2.2. Verifica que `requirements.txt` esté correcto:**

El archivo `streamlit_app/requirements.txt` debe contener:

```txt
streamlit==1.28.1
pandas==2.0.0
plotly==5.17.0
psycopg2-binary==2.9.9
sqlalchemy==2.0.23
python-dotenv==1.0.0
pyarrow==14.0.1
```

Si no está, créalo con este contenido.

---

### Paso 3: Crear el Módulo de Conexión a Base de Datos

**3.1. Crea el archivo `streamlit_app/utils/db_connection.py`:**

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

**3.2. Crea `streamlit_app/utils/__init__.py`:** (archivo vacío)

```python
# Este archivo hace que utils sea un módulo de Python
```

---

### Paso 4: Crear la Página Principal (app.py)

**4.1. Crea `streamlit_app/app.py`:**

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

---

### Paso 5: Crear Páginas Adicionales (Opcional pero Recomendado)

**5.1. Crea `streamlit_app/pages/__init__.py`:** (archivo vacío)

```python
# Este archivo hace que pages sea un módulo de Python
```

**5.2. Crea `streamlit_app/pages/page1_datos_en_vivo.py`:**

```python
import streamlit as st
from utils.db_connection import get_int_data, get_float_data
import plotly.graph_objects as go

st.title("📈 Datos en Vivo")

st.write("""
Este página muestra los datos en tiempo real que están siendo capturados 
por el sistema MQTT y almacenados en la base de datos PostgreSQL.
""")

# Selector de horas
hours = st.slider("Últimas N horas", min_value=0.083, max_value=168, value=1.0, step=0.083)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Datos Enteros")
    df_int = get_int_data(hours)
    if df_int is not None and not df_int.empty:
        st.metric("Total de registros", len(df_int))
        st.dataframe(df_int, use_container_width=True)

with col2:
    st.subheader("Datos Flotantes")
    df_float = get_float_data(hours)
    if df_float is not None and not df_float.empty:
        st.metric("Total de registros", len(df_float))
        st.dataframe(df_float, use_container_width=True)
```

**5.3. Crea `streamlit_app/pages/page2_estadisticas.py`:**

```python
import streamlit as st
from utils.db_connection import get_stats_int, get_stats_float
import pandas as pd

st.title("📊 Estadísticas Detalladas")

st.write("""
Análisis estadístico completo de los datos capturados.
""")

hours = st.slider("Últimas N horas", min_value=0.083, max_value=168, value=24.0, step=0.083)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Estadísticas - Datos Enteros")
    stats = get_stats_int(hours)
    if stats is not None and not stats.empty:
        st.dataframe(stats, use_container_width=True)

with col2:
    st.subheader("📉 Estadísticas - Datos Flotantes")
    stats = get_stats_float(hours)
    if stats is not None and not stats.empty:
        st.dataframe(stats, use_container_width=True)
```

---

### Paso 6: Crear archivo `.env` para la App

**6.1. Crea `streamlit_app/.env`:**

```env
# Configuración de Base de Datos
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=sensordata
```

---

### Paso 7: Probar la App Localmente

**7.1. Desde tu terminal, navega a la carpeta del proyecto:**

```bash
cd c:\Users\angel\OneDrive\Documents\IOT\U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization
```

**7.2. Activa el entorno virtual (si tienes uno) o instala Streamlit:**

```bash
pip install streamlit plotly pandas psycopg2-binary sqlalchemy python-dotenv
```

**7.3. Ejecuta la aplicación:**

```bash
streamlit run streamlit_app/app.py
```

Deberías ver algo como:

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

**7.4. Abre tu navegador en `http://localhost:8501`**

---

### Paso 8: Ejecutar con Docker (Opcional - para producción)

**8.1. Actualiza `docker-compose.yml` para que incluya el servicio streamlit:**

El archivo ya tiene una sección para streamlit:

```yaml
streamlit:
  build:
    context: ./streamlit_app
  ports:
    - "8501:8501"
  depends_on:
    - postgres
    - mosquitto
  environment:
    - DB_HOST=postgres
    - DB_PORT=5432
    - DB_USER=user
    - DB_PASSWORD=password
    - DB_NAME=sensordata
  networks:
    - data_pipeline_net
```

**8.2. Asegúrate de que `streamlit_app/Dockerfile` esté correcto:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**8.3. Levanta los servicios con Docker:**

```bash
docker-compose up -d streamlit
```

**8.4. Accede en `http://localhost:8501`**

---

## 📂 Estructura de Archivos Final

```
streamlit_app/
├── Dockerfile
├── requirements.txt          # ✅ Debe existir
├── .env                     # ✅ Crea este
├── app.py                   # ✅ Crea este (app principal)
├── pages/
│   ├── __init__.py         # ✅ Crea este (vacío)
│   ├── page1_datos_en_vivo.py
│   └── page2_estadisticas.py
├── utils/
│   ├── __init__.py         # ✅ Crea este (vacío)
│   └── db_connection.py    # ✅ Crea este (módulo de conexión)
└── styles/
    └── custom.css          # Opcional
```

---

## 🔌 Conexión a la Base de Datos

### Desde tu máquina (desarrollo local):
```
Host: localhost
Puerto: 5432
Usuario: user
Contraseña: password
Base de datos: sensordata
```

### Desde Docker (dentro de docker-compose):
```
Host: postgres (nombre del servicio)
Puerto: 5432
Usuario: user
Contraseña: password
Base de datos: sensordata
```

El código que te proporcioné usa `localhost` por defecto, que funciona cuando ejecutas Streamlit localmente. Si lo corres en Docker, ajusta el `.env` a:

```env
DB_HOST=postgres
```

---

## ✅ Checklist de Implementación

- [ ] Paso 1: Verificar que Docker esté corriendo
- [ ] Paso 2: Crear estructura de carpetas y archivos
- [ ] Paso 3: Crear `streamlit_app/utils/db_connection.py`
- [ ] Paso 4: Crear `streamlit_app/app.py`
- [ ] Paso 5: Crear páginas adicionales (opcional)
- [ ] Paso 6: Crear `streamlit_app/.env`
- [ ] Paso 7: Probar localmente con `streamlit run streamlit_app/app.py`
- [ ] Paso 8: Probar con Docker (opcional)
- [ ] Paso 9: Validar que las gráficas muestren datos reales
- [ ] Paso 10: Hacer commit a Git

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'streamlit'"
**Solución**: Instala con `pip install streamlit`

### Error: "could not connect to server: Connection refused"
**Solución**: 
- Verifica que PostgreSQL esté corriendo: `docker-compose ps`
- Verifica que `DB_HOST` en `.env` sea correcto (localhost para dev, postgres para Docker)

### Error: "relation 'lake_raw_data_int' does not exist"
**Solución**:
- Verifica que el subscriber esté corriendo: `docker-compose logs subscriber`
- Verifica que PostgreSQL haya ejecutado `init.sql`: `docker-compose logs postgres_db`

### Dashboard sin datos
**Solución**:
- Verifica que el publisher esté publicando: `docker-compose logs subscriber`
- Espera a que acumule algunos segundos de datos
- Haz clic en "Refrescar" en la sidebar

---

## 📞 Próximos Pasos

1. ✅ Implementa los archivos según esta guía
2. ✅ Prueba localmente
3. ✅ Valida que las gráficas muestren datos reales
4. ✅ Mejora la UI/UX si lo deseas (colores, temas, etc.)
5. ✅ Documenta cualquier cambio que hagas
6. ✅ Comunica con el equipo cuando esté listo

---

¡Adelante, Damián! 🚀
