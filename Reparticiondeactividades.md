
## Distribución de Trabajo (Equipo de 4)

### 1. Tú (Russel) - Data Architect

Tu misión es que la infraestructura no falle. Eres el que monta el escenario.

* 
**Dockerización:** Crear el `docker-compose.yml` para levantar el broker (Mosquitto) y la base de datos (PostgreSQL).


* 
**Estructura de Datos:** Crear las tablas `lake_raw_data_int` y `lake_raw_data_float` siguiendo el esquema exacto de SQL que pide la actividad.


* 
**Conectividad:** Asegurarte de que el flujo de datos sea consistente desde que entra al broker hasta que se guarda en la DB.



### 2. Manchas y Baby Pelusa - Desarrolladoras (MQTT & Dashboard)

Ellas se encargan de la lógica de programación sobre la base que tú construyas.

* 
**MQTT (Scripts):** Usar los códigos de clase para publicar valores aleatorios (enteros y flotantes) y suscribirse para guardarlos en la DB.


* 
**Streamlit:** Construir el dashboard que jale los datos de tus tablas y los muestre en gráficas de series de tiempo.


* 
**Diferenciación:** Asegurarse de que en la interfaz se distingan claramente los dos flujos de datos.



### 3. Suncho - Technical Documentation (LaTeX Master)

Su trabajo es que el proyecto se vea impecable para el profesor.

* 
**Reporte IEEE:** Montar todo en LaTeX siguiendo el formato IEEE (máximo 6 páginas).


* 
**Diagramas:** Dibujar el diagrama de arquitectura que incluya el publisher, broker, subscriber, DB y dashboard.


* 
**Evidencias:** Capturar las tablas de la base de datos con datos reales una vez que el sistema de Russel esté corriendo.



---

### Plan de Acción "Rapidín"

| Fase | Actividad | Responsable |
| --- | --- | --- |
| **Paso 1** | Levantar Docker con Postgres y Mosquitto. | **Russel** |
| **Paso 2** | Adaptar scripts de clase y conectar al Docker de Russel. | **Manchas y Baby Pelusa** |
| **Paso 3** | Tomar capturas de datos insertados y armar el diagrama. | **Suncho** |
| **Paso 4** | Pulir gráficas en Streamlit y cerrar el PDF en LaTeX. | **Todos** |

**Opinión técnica:** Como se usara Docker, Manchas y Suncho en sus scripts cambien `localhost` por el nombre del servicio que definas en tu archivo (ej. `host="db"`). Eso les ahorrará media hora de errores de conexión.
