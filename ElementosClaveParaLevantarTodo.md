# 🚀 Elementos Clave para Levantar el Sistema Completo

Este documento describe los pasos necesarios para iniciar el sistema de ingesta de datos IoT con MQTT, PostgreSQL y Streamlit.

## 📋 Prerrequisitos

- Docker y Docker Compose instalados
- Python 3.11+
- Acceso a las credenciales de CloudAMQP (MQTT Broker)

## 🗄️ Crear la Base de Datos

Antes de ejecutar Docker Compose, es necesario crear las tablas en PostgreSQL.

### 1. Conectar a PostgreSQL

```bash
psql -h localhost -U iot_usr -d iot_course -W
```

Ingresa la contraseña: `upy_student_Admin1`

### 2. Crear Tablas de Datos Raw

```sql
-- Tabla para datos enteros
CREATE TABLE IF NOT EXISTS lake_raw_data_int (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    payload JSONB,
    value INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla para datos flotantes
CREATE TABLE IF NOT EXISTS lake_raw_data_float (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    payload JSONB,
    value FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejorar rendimiento
CREATE INDEX idx_topic_int ON lake_raw_data_int(topic);
CREATE INDEX idx_topic_float ON lake_raw_data_float(topic);
CREATE INDEX idx_timestamp_int ON lake_raw_data_int(timestamp DESC);
CREATE INDEX idx_timestamp_float ON lake_raw_data_float(timestamp DESC);
```

## 🐳 Iniciar con Docker Compose

```bash
# Navegar al directorio del proyecto
cd U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization

# Construir las imágenes
docker-compose build

# Iniciar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

## 📡 Iniciar el Publisher

El publisher publica datos de prueba en los topics:
- `lake/raw/int` - valores enteros
- `lake/raw/float` - valores flotantes

Ejecutar en Jupyter Notebook o terminal:

```bash
cd Project_Elements
jupyter notebook publisher.ipynb
```

## 📥 Iniciar el Subscriber

El subscriber escucha los mensajes MQTT y los almacena en PostgreSQL.

```bash
cd Project_Elements
jupyter notebook suscriber.ipynb
```

Ejecuta la celda `main()` para comenzar a escuchar mensajes.

## 📊 Visualizar Datos en Streamlit

La aplicación Streamlit estará disponible en: **http://localhost:8501**

```bash
# Si ejecutas localmente (sin Docker)
cd streamlit_app
streamlit run app.py
```

## ✅ Verificar que Todo Funciona

1. **Verificar PostgreSQL**:
   ```sql
   SELECT COUNT(*) FROM lake_raw_data_int;
   SELECT COUNT(*) FROM lake_raw_data_float;
   ```

2. **Ver logs de Docker**:
   ```bash
   docker-compose logs subscriber  # Si existe servicio subscriber
   docker-compose logs streamlit
   ```

3. **Prueba de conectividad**:
   ```bash
   # Verificar que PostgreSQL está disponible
   docker-compose exec db psql -U iot_usr -d iot_course -c "SELECT 1"
   ```

## 🛑 Detener Todo

```bash
docker-compose down

# Incluir volúmenes (elimina datos)
docker-compose down -v
```

## 📝 Notas Importantes

- Los datos de PostgreSQL se persisten en `postgres_data` volume
- Las credenciales están definidas en `docker-compose.yml`
- El topic MQTT es `#` (suscripción a todos los tópicos)
- Los datos se almacenan con timestamp automático

## 🐛 Solución de Problemas

### Error de conexión a PostgreSQL
```
psycopg2.OperationalError: could not connect to server
```
**Solución**: Asegúrate que PostgreSQL esté corriendo en Docker:
```bash
docker-compose ps
```

### Error de conexión a MQTT Broker
```
socket.gaierror: [Errno -2] Name or service not known
```
**Solución**: Verifica credenciales de CloudAMQP en `suscriber.ipynb` y `publisher.ipynb`

### Permisos denegados en pgAdmin
```
FATAL: password authentication failed for user "iot_usr"
```
**Solución**: Reinicia PostgreSQL:
```bash
docker-compose restart db
```



