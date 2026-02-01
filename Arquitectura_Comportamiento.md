# Documentación de Arquitectura y Comportamiento

## 1. Descripción General de la Arquitectura

La arquitectura final implementada consiste en un pipeline de datos desacoplado y contenerizado, diseñado para la ingesta y visualización de datos de sensores en tiempo real. El sistema utiliza Docker y Docker Compose para orquestar los siguientes cuatro servicios principales que se comunican a través de una red interna (`data_pipeline_net`):

**Flujo de Datos:**
`Publicador MQTT` → `Mosquitto (Broker)` → `Subscriber (Python)` → `PostgreSQL (Base de Datos)` → `Streamlit (Dashboard)`

Esta arquitectura es robusta, escalable y fácil de levantar en cualquier máquina con Docker, gracias a la automatización de la configuración y la resiliencia de los componentes.

---

## 2. Componentes de la Arquitectura (Servicios Docker)

A continuación, se detalla el rol y la configuración de cada servicio definido en el archivo `docker-compose.yml`.

### a. Servicio `mosquitto` (Broker MQTT)
- **Rol:** Actúa como el intermediario central de mensajería. Recibe los datos publicados por los sensores (o el script publicador) y los pone a disposición de los clientes suscritos.
- **Configuración Clave:**
  - Se utiliza la imagen oficial `eclipse-mosquitto:2.0`.
  - **`mosquitto/mosquitto.conf`**: Se montó un archivo de configuración personalizado para solucionar un problema de seguridad de la versión 2.x de Mosquitto, que por defecto solo permite conexiones locales. Este archivo contiene las siguientes directivas:
    ```
    listener 1883
    allow_anonymous true
    ```
    Esto permite que el broker acepte conexiones anónimas en el puerto `1883` desde otros contenedores en la misma red de Docker, como nuestro servicio `subscriber`.

### b. Servicio `postgres` (Base de Datos)
- **Rol:** Funciona como el almacén de datos (data warehouse) para la data cruda (raw) proveniente de los sensores.
- **Configuración Clave:**
  - Se utiliza la imagen oficial `postgres:13`.
  - **Variables de Entorno:** Las credenciales (`user`, `password`) y el nombre de la base de datos (`sensordata`) se definen como variables de entorno para facilitar su gestión.
  - **`init.sql` (Inicialización Automática):** Se monta un script SQL en el directorio `/docker-entrypoint-initdb.d/`. PostgreSQL ejecuta automáticamente cualquier script en esta carpeta la primera vez que se crea el contenedor. Este script crea las dos tablas necesarias:
    - `lake_raw_data_int`: Para almacenar valores enteros.
    - `lake_raw_data_float`: Para almacenar valores de punto flotante.
  - **Esquema de Tablas:** Ambas tablas comparten una estructura similar: `id (SERIAL PK)`, `topic (VARCHAR)`, `payload (JSONB)`, `value` (con el tipo de dato correspondiente `BIGINT` o `DOUBLE PRECISION`) y `ts (TIMESTAMP)`.
  - **Persistencia de Datos:** Se utiliza un volumen de Docker (`postgres_data`) para asegurar que los datos de la base de datos persistan incluso si el contenedor se elimina o se recrea.

### c. Servicio `subscriber` (Consumidor y "Pegamento")
- **Rol:** Es el corazón de la lógica de ingesta de datos. Se suscribe al broker `mosquitto`, recibe los mensajes, los procesa y los inserta en la tabla correcta de la base de datos `postgres`.
- **Configuración Clave:**
  - Se construye a partir de un `Dockerfile` personalizado (`subscriber/Dockerfile`) basado en una imagen de Python.
  - **Dependencias:** Instala `paho-mqtt` (para comunicarse con Mosquitto) y `psycopg2-binary` (para comunicarse con PostgreSQL).
  - **Lógica Resiliente:** El script `subscriber.py` fue programado para ser robusto ante condiciones de carrera durante el arranque del sistema:
    - Si la base de datos o el broker MQTT no están listos cuando el suscriptor se inicia, el script no se cierra. En su lugar, entra en un bucle de reintento, intentando conectarse cada 5 segundos hasta que tiene éxito. Esto asegura que el sistema se estabilice automáticamente.

### d. Servicio `streamlit` (Dashboard)
- **Rol:** Es la capa de presentación y visualización de los datos. Su responsabilidad es consultar la base de datos `postgres` y mostrar los datos en un dashboard web.
- **Configuración Clave:**
  - Se construye a partir de un `Dockerfile` personalizado (`streamlit_app/Dockerfile`).
  - **Conexión a la BD:** Recibe las credenciales de la base de datos a través de variables de entorno, pasadas directamente desde el `docker-compose.yml`.
  - **`app.py` Mínimo:** Se creó un archivo `app.py` básico para permitir que el servicio se inicie correctamente y evitar un ciclo de errores. Este archivo debe ser reemplazado por el desarrollador del frontend con la lógica real del dashboard.

---

## 3. Archivo `docker-compose.yml` Final

Este es el archivo completo que orquesta todos los servicios descritos:

```yaml
version: '3.8'

services:
  # MQTT Broker
  mosquitto:
    image: eclipse-mosquitto:2.0
    container_name: mosquitto
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
    networks:
      - data_pipeline_net
    restart: always

  # PostgreSQL Database
  postgres:
    image: postgres:13
    container_name: postgres_db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: sensordata
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - data_pipeline_net
    restart: always

  # Python Subscriber Service
  subscriber:
    build:
      context: ./subscriber
    container_name: subscriber
    depends_on:
      - mosquitto
      - postgres
    environment:
      - MQTT_BROKER=mosquitto
      - DB_HOST=postgres_db
      - DB_NAME=sensordata
      - DB_USER=user
      - DB_PASS=password
    networks:
      - data_pipeline_net
    restart: always

  # Streamlit Dashboard
  streamlit:
    build:
      context: ./streamlit_app
      dockerfile: Dockerfile
    container_name: streamlit_dashboard
    depends_on:
      - postgres
    ports:
      - "8501:8501"
    environment:
      - DB_HOST=postgres_db
      - DB_PORT=5432
      - DB_NAME=sensordata
      - DB_USER=user
      - DB_PASS=password
    networks:
      - data_pipeline_net
    restart: on-failure

volumes:
  postgres_data:

networks:
  data_pipeline_net:
    driver: bridge
```

---

## 4. Comportamiento y Consideraciones Importantes

### Tiempos de Construcción (Build Times)
**¡IMPORTANTE!** La **primera vez** que se construya este entorno (con `docker-compose up --build`), el proceso puede ser **extremadamente lento**, llegando a tardar 15 minutos o más dependiendo de la máquina y la conexión a internet.

- **Causa:** Esto no se debe a un error. Ocurre porque el servicio de `streamlit` depende de librerías de ciencia de datos muy pesadas (como `pandas`, `numpy`, `pyarrow`). Si Docker no encuentra una versión pre-compilada de estas librerías para la arquitectura de la imagen base, debe instalar compiladores de sistema (`gcc`) y compilar las librerías desde su código fuente. Este proceso es muy intensivo.
- **Ventaja de Docker:** Este largo tiempo de espera es un **costo de única vez**. Docker guarda en caché las capas de la imagen que construye. En arranques posteriores, a menos que se modifiquen los `Dockerfile` o los `requirements.txt`, las construcciones serán casi instantáneas.

### Arranque y Estabilidad
- El sistema está diseñado para ser estable. El uso de `depends_on` ayuda a controlar el orden de inicio, y la lógica de reintentos en el `subscriber` asegura que las conexiones se establezcan incluso si hay pequeños retrasos en el arranque de los servicios de red.
- Las políticas de `restart` (`always` o `on-failure`) aseguran que si un contenedor falla por una razón inesperada, Docker intentará levantarlo de nuevo automáticamente.

---

## 5. Estructura de Archivos Creada

Para lograr esta arquitectura, se crearon los siguientes archivos y directorios:

- `docker-compose.yml` (Modificado extensivamente)
- `init.sql` (Nuevo)
- `mosquitto/mosquitto.conf` (Nuevo)
- `subscriber/Dockerfile` (Nuevo)
- `subscriber/requirements.txt` (Nuevo)
- `subscriber/subscriber.py` (Nuevo)
- `streamlit_app/app.py` (Nuevo)
- `streamlit_app/requirements.txt` (Modificado)
