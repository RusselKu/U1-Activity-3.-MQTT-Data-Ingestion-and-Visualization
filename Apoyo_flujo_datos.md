# Guía de Apoyo para el Flujo de Datos

## 1. Introducción

Esta guía está dirigida a los desarrolladores encargados de implementar la lógica de publicación de datos (sensores) y la visualización en el dashboard.

La infraestructura backend está completamente configurada y en funcionamiento. Todos los servicios (broker, base de datos, suscriptor) se inician y comunican automáticamente. Lo único que se necesita para levantar todo el entorno es ejecutar el siguiente comando en la raíz del proyecto:

```bash
docker-compose up
```

---

## 2. Guía para el Desarrollador del Publicador (MQTT)

Tu tarea es crear un script que simule uno o varios sensores y publique los datos en el broker MQTT.

### Detalles de Conexión al Broker
El broker `mosquitto` está expuesto a tu máquina local. Para conectarte a él desde tu script de Python (ejecutado en tu propia máquina, fuera de Docker), usa los siguientes parámetros:

- **Host:** `'localhost'` o `'127.0.0.1'`
- **Puerto:** `1883`
- **Usuario/Contraseña:** No se requieren. La conexión es anónima.

### Formato del Mensaje
El servicio suscriptor espera que cada mensaje sea un objeto JSON con una clave específica "value".

- **Formato Requerido:** `{"value": <numero>}`
  - Ejemplo con entero: `{"value": 42}`
  - Ejemplo con flotante: `{"value": 3.14159}`

### Tópicos (Topics)
El suscriptor está escuchando en todos los tópicos (`#`). La inserción en la base de datos se realiza de la siguiente manera:

- Si el `value` en el mensaje es un **entero**, los datos se guardarán en la tabla `lake_raw_data_int`.
- Si el `value` es un **flotante**, los datos se guardarán en la tabla `lake_raw_data_float`.

Puedes usar diferentes tópicos para organizar tus datos (ej. `sensor/temperatura`, `sensor/humedad`), y mientras el formato del mensaje sea correcto, el suscriptor lo procesará y lo guardará en la tabla correspondiente según el tipo de dato.

---

## 3. Guía para el Desarrollador del Dashboard (Streamlit)

Tu tarea es implementar la lógica de visualización en el dashboard de Streamlit, consumiendo los datos que ya están siendo almacenados en la base de datos PostgreSQL.

### Conexión a la Base de Datos
**No necesitas configurar la conexión.** El servicio `streamlit` ya recibe todas las credenciales necesarias a través de variables de entorno desde `docker-compose.yml`.

Tu código dentro de `streamlit_app/app.py` puede (y debe) leer estas variables de entorno para establecer la conexión. El script `subscriber.py` contiene un buen ejemplo de cómo hacer esto:

```python
import os
import psycopg2

# Ejemplo de cómo leer las variables de entorno para la conexión
conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    port=os.environ.get("DB_PORT")
)
```

### Esquema de las Tablas
Tienes dos tablas a tu disposición para consultar los datos:

1.  **`lake_raw_data_int`**: Contiene los valores enteros.
2.  **`lake_raw_data_float`**: Contiene los valores flotantes.

Ambas tablas tienen las siguientes columnas que puedes usar en tus queries (`SELECT`):
- `id`: Identificador único de la fila.
- `topic`: El tópico MQTT en el que se publicó el mensaje.
- `payload`: El mensaje JSON completo que se recibió.
- `value`: El valor numérico extraído del payload.
- `ts`: La fecha y hora en que se insertó el registro en la base de datos.

### Punto de Partida
Ya existe un archivo `streamlit_app/app.py` con contenido básico. Este archivo fue creado para asegurar que el servicio se levante correctamente. **Debes borrar su contenido y reemplazarlo con tu propia lógica** para consultar los datos de PostgreSQL y generar las gráficas.
