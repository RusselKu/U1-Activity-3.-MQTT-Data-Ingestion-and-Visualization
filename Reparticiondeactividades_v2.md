## División de Tareas (versión sin Mongo/Airflow)

> Estado: MongoDB y Airflow ya NO serán usados en este proyecto. Todas las instrucciones y tareas deben asumir la infraestructura existente (por ejemplo PostgreSQL y Docker para Mosquitto).

### Rivaldo — Backend & Data Flow (Prioridad Alta)

1. Subscriber MQTT + PostgreSQL
- Adaptar `suscriber.ipynb` para usar PostgreSQL (volver a `psycopg2` o similar)
- Conectar al servicio PostgreSQL definido en `docker-compose` (host="db" o el nombre del servicio que exista)
- Insertar datos en las tablas: `lake_raw_data_int` y `lake_raw_data_float`
- Probar que los datos se almacenen correctamente

2. Verificación del Publisher
- Revisar que `publisher.ipynb` funcione correctamente
- Asegurar que publique ambos topics: `lake/raw/int` y `lake/raw/float`
- Documentar con capturas para Suncho


### Damián — Frontend & Visualization (Prioridad Alta)

1. Dashboard Streamlit
- Crear la app principal dentro de `streamlit_app`
- Conectar a la base de datos que defina Rivaldo (PostgreSQL por defecto)
- Diseñar la interfaz con páginas/pestañas

2. Visualizaciones
- Gráfica de series de tiempo para datos enteros
- Gráfica de series de tiempo para datos flotantes
- Usar `plotly` (u otra librería interactiva) para las gráficas
- Agregar filtros de tiempo (últimos 5 min, 1 hora, etc.)
- Mostrar estadísticas (promedio, máximo, mínimo)


### Orden de Ejecución

1. Rivaldo termina el subscriber y valida ingestión en Postgres.
2. Damián inicia la UI usando mock data mientras espera datos reales.
3. Integración final: Damián conecta la app a la base real y valida visualizaciones.


### Cambio requerido en el repo (recordatorio)

Se encontraron referencias a MongoDB y Airflow que deben eliminarse o actualizarse para evitar confusión. Archivos con menciones detectadas:
- .gitignore (líneas relacionadas con `airflow`)
- Dockerfile (base `apache/airflow:2.8.1`)
- ElementosClaveParaLevantarTodo.md (comandos de `airflow` y uso de `mongo`)
- requirements.txt (entradas `pymongo` / `pymongo[srv]`)

Si quieres, puedo:
- eliminar o comentar esas referencias en los archivos mencionados, o
- actualizar el `Dockerfile` a una imagen base apropiada (por ejemplo `python:3.11`) y ajustar `requirements.txt`.

---

Nota: Creé este archivo `Reparticiondeactividades_v2.md` en el workspace sin hacer commits.
