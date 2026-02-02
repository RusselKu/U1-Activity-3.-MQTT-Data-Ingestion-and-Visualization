# 📄 Reporte Técnico del Proyecto: Ingesta y Visualización de Datos IoT con MQTT y Streamlit

**Fecha:** 02 de Febrero de 2026
**Autores:** [Tu Nombre], [Nombre de Tu Compañero de LaTeX]
**Estado:** ✅ Backend Completo, Frontend Funcional, Documentación Preliminar Lista

---

## 🚀 1. Resumen Ejecutivo

Este documento detalla la implementación de un sistema integral de ingesta y visualización de datos de Internet de las Cosas (IoT). El proyecto utiliza un Publisher para simular la generación de datos, un broker MQTT (Mosquitto) para la mensajería, un Subscriber para almacenar los datos en una base de datos PostgreSQL, y un dashboard interactivo desarrollado con Streamlit para la visualización en tiempo real. El objetivo es proveer una plataforma robusta y escalable para el monitoreo de datos IoT.

---

## 📋 2. Arquitectura del Sistema

El sistema sigue una arquitectura modular y desacoplada, facilitando el mantenimiento y la escalabilidad.

```
┌─────────────────────┐
│  Publisher          │
│  (Genera datos)     │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │  MQTT Topics │
    ├──────────────┤
    │lake/raw/int  │
    │lake/raw/float│
    └──────┬───────┘
           │
    ┌──────▼──────────┐
    │ Mosquitto       │
    │ (Broker MQTT)   │
    │ Port 1883       │
    └──────┬──────────┘
           │
    ┌──────▼───────────┐
    │ Subscriber       │
    │ (Docker Service) │
    └──────┬───────────┘
           │
    ┌──────▼────────────────┐
    │   PostgreSQL           │
    ├────────────────────────┤
    │ • lake_raw_data_int    │
    │ • lake_raw_data_float  │
    │ • events_log           │
    └──────┬─────────────────┘
           │
    ┌──────▼──────────────┐
    │  Streamlit Dashboard │
    │  http://localhost   │
    │        :8501        │
    └─────────────────────┘
```

**Componentes Clave:**

*   **Publisher (Python):** Simula un dispositivo IoT, generando valores aleatorios (enteros y flotantes) y publicándolos en tópicos MQTT específicos (`lake/raw/int`, `lake/raw/float`).
*   **Mosquitto MQTT Broker (Docker):** Actúa como el centro de mensajería, recibiendo los datos del Publisher y distribuyéndolos a los suscriptores.
*   **Subscriber (Python, Docker Service):** Escucha los tópicos de Mosquitto, procesa los mensajes y los inserta en la base de datos PostgreSQL.
*   **PostgreSQL Database (Docker):** Almacena los datos IoT en tablas separadas para enteros (`lake_raw_data_int`) y flotantes (`lake_raw_data_float`), con campos de ID, tópico, valor y timestamp.
*   **Streamlit Dashboard (Python):** Se conecta a la base de datos PostgreSQL para recuperar los datos y los visualiza en tiempo real a través de gráficos interactivos y estadísticas.

---

## ⚙️ 3. Configuración del Entorno

Para levantar el proyecto, se requieren los siguientes prerrequisitos y pasos:

### 3.1. Prerrequisitos

*   **Docker Desktop:** Instalado y en ejecución (incluye Docker Engine y Docker Compose).
*   **Python 3.11+:** Instalado localmente.
*   **Git:** Para clonar el repositorio.

### 3.2. Clonación del Repositorio

```bash
git clone <URL_DEL_REPOSITORIO> U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization
cd U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization
```

### 3.3. Configuración de Variables de Entorno para Streamlit

El dashboard de Streamlit requiere credenciales de base de datos que se configuran a través de un archivo `.env` en el directorio `streamlit_app/`.

1.  Asegúrate de que el archivo `streamlit_app/.env` exista con el siguiente contenido:
    ```env
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=user
    DB_PASSWORD=password
    DB_NAME=sensordata
    ```
    (Nota: Se usa `localhost` para la ejecución local de Streamlit, conectándose al puerto expuesto de PostgreSQL).

---

## 📥 4. Flujo de Datos: Publisher a PostgreSQL

Esta sección describe cómo los datos se generan, transmiten y almacenan en la base de datos.

### 4.1. Inicio de Servicios Docker (Backend)

Todos los servicios de backend (Mosquitto, PostgreSQL y Subscriber) se orquestan con Docker Compose.

```bash
# Desde la raíz del proyecto:
docker-compose down --volumes --rmi all # Limpieza completa (opcional, pero recomendada)
docker-compose up -d --build             # Iniciar todos los servicios en segundo plano
```

**Verificación de Servicios:**
```bash
docker-compose ps
```
**[CAPTURAR PANTALLA 1: Salida de `docker-compose ps` mostrando los servicios `mosquitto`, `postgres_db` y `subscriber` como "Up"]**

### 4.2. Ejecución del Publisher

El script `run_publisher.py` genera datos aleatorios y los envía al broker MQTT. Debe ejecutarse en una terminal separada y permanecer activo para que haya flujo de datos.

```bash
# Desde la raíz del proyecto, en una TERMINAL NUEVA:
python run_publisher.py
```

### 4.3. Verificación de Ingesta de Datos (Logs del Subscriber)

El Subscriber recibe los datos del Publisher y los inserta en PostgreSQL. Los logs del Subscriber confirman la recepción e inserción de datos.

```bash
# Desde la raíz del proyecto, en OTRA TERMINAL (o donde levantaste los servicios):
docker-compose logs subscriber -f
```
Se deben observar líneas como las siguientes, indicando la inserción exitosa de datos:

```
subscriber  | ... INFO ✅ INT inserted: topic=lake/raw/int, value=...
subscriber  | ... INFO ✅ FLOAT inserted: topic=lake/raw/float, value=...
```
**[CAPTURAR PANTALLA 2: Terminal mostrando el log del subscriber con varias líneas de "INT inserted" y "FLOAT inserted"]**

---

## 📊 5. Implementación y Ejecución del Dashboard Streamlit

El dashboard, implementado por Damián, visualiza los datos en tiempo real extraídos de PostgreSQL.

### 5.1. Archivos Clave del Dashboard

Los siguientes archivos fueron creados o actualizados para el dashboard:

*   **`streamlit_app/.env`:** Configuración de credenciales de la base de datos.
*   **`streamlit_app/utils/__init__.py`:** Archivo vacío que marca `utils` como un paquete Python.
*   **`streamlit_app/utils/db_connection.py`:** Módulo para establecer la conexión a PostgreSQL y funciones para consultar datos enteros, flotantes y sus estadísticas.
*   **`streamlit_app/app.py`:** Archivo principal de la aplicación Streamlit, que define la interfaz de usuario, los gráficos (Plotly) y la lógica de visualización.

### 5.2. Instalación de Dependencias

Asegúrate de que las dependencias de Python para Streamlit estén instaladas.

```bash
# Desde la raíz del proyecto o desde streamlit_app/:
pip install streamlit plotly pandas psycopg2-binary python-dotenv
```

### 5.3. Ejecución del Dashboard Streamlit

Para iniciar la aplicación Streamlit, se recomienda usar una terminal como PowerShell o CMD debido a problemas de interacción con MINGW64.

```bash
# Desde el directorio streamlit_app/:
cd C:/Users/angel/OneDrive/Documents/IOT/U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization/streamlit_app
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --browser.gatherUsageStats false --browser.serverAddress localhost
```
Una vez ejecutado, el dashboard debería abrirse automáticamente en tu navegador en `http://localhost:8501`.

---

## ✅ 6. Verificación y Resultados del Dashboard

El dashboard de Streamlit presenta dos pestañas principales: "Datos en Vivo" y "Estadísticas", además de una pestaña de "Información".

### 6.1. Pestaña "Datos en Vivo"

Esta pestaña muestra gráficos de series de tiempo para datos enteros y flotantes, actualizándose con los datos más recientes de la base de datos.

*   **Gráfica de Datos Enteros (Línea Azul):** Visualiza la evolución de los valores enteros a lo largo del tiempo.
*   **Gráfica de Datos Flotantes (Línea Naranja):** Visualiza la evolución de los valores flotantes a lo largo del tiempo.
*   **Últimos Registros:** Se puede expandir para ver una tabla con los últimos 10 registros de cada tipo.

**[CAPTURAR PANTALLA 3: Dashboard de Streamlit en la pestaña "Datos en Vivo", mostrando ambas gráficas con datos y los últimos registros expandidos.]**

### 6.2. Pestaña "Estadísticas"

Esta pestaña ofrece un resumen estadístico de los datos ingeridos.

*   **Métricas para Datos Enteros y Flotantes:** Incluye el total de registros, promedio, valor mínimo, valor máximo y desviación estándar.
*   **Filtro de Rango de Tiempo:** En la barra lateral, se puede seleccionar un rango de tiempo (ej. "Última 1 hora", "Últimos 7 días") para analizar datos específicos. El botón "Refrescar Datos" actualiza las gráficas y estadísticas según el filtro.

**[CAPTURAR PANTALLA 4: Dashboard de Streamlit en la pestaña "Estadísticas", mostrando todas las métricas. Asegúrate de que el filtro de rango de tiempo en la barra lateral sea visible.]**

---

## 💡 7. Conclusiones

El proyecto ha logrado establecer un pipeline de datos IoT funcional, desde la simulación de sensores hasta la visualización interactiva. La arquitectura basada en Docker y componentes desacoplados demuestra robustez y facilidad de gestión. A pesar de los desafíos iniciales en la configuración del entorno (como los problemas de interacción en MINGW64), se logró la integración exitosa de todos los componentes. El dashboard de Streamlit proporciona una herramienta intuitiva para el monitoreo en tiempo real, validando la eficacia del sistema.

---

## ⏭️ 8. Próximos Pasos

Este documento servirá como base para la creación de un informe técnico formal en LaTeX. Tu compañero deberá:

1.  Tomar las capturas de pantalla indicadas en este documento.
2.  Integrar el contenido de este Markdown en el formato LaTeX IEEE, añadiendo cualquier detalle técnico adicional que considere relevante para el informe final.
3.  Asegurarse de que las imágenes (capturas de pantalla) se inserten correctamente en el reporte LaTeX.

---
