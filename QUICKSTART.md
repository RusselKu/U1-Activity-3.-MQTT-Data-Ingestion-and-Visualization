# ⚡ QUICK START - Inicio Rápido (Mosquitto Local)

## 5 Pasos para Empezar

### 1️⃣ Preparar el Entorno
```bash
# Navegar al proyecto
cd U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization

# Copiar configuración
cp .env.example .env

# Verificar que todo está OK
python verify_setup.py
```

### 2️⃣ Iniciar Todos los Servicios
```bash
# Construir imágenes Docker
docker-compose build

# Iniciar todos los servicios (PostgreSQL, Mosquitto, Subscriber, Streamlit)
docker-compose up -d

# Ver logs
docker-compose logs -f

# Si todo OK, deberías ver:
# ✅ mosquitto - Running on port 1883
# ✅ postgres_db - Ready to accept connections
# ✅ subscriber - Connected to MQTT Broker
# ✅ streamlit_dashboard - Ready
```

### 3️⃣ Ejecutar Publisher (genera datos de prueba)
```bash
# Opción A: Jupyter Notebook (recomendado)
cd Project_Elements
jupyter notebook publisher.ipynb
# Ejecutar todas las celdas

# Opción B: Terminalmente en Python
python publisher.py  # Si creas el archivo
```

### 4️⃣ Verificar Datos en PostgreSQL
```bash
# En otra terminal
docker-compose exec postgres_db psql -U user -d sensordata

# Conectado a PostgreSQL, ejecuta:
SELECT COUNT(*) FROM lake_raw_data_int;
SELECT COUNT(*) FROM lake_raw_data_float;
SELECT * FROM lake_raw_data_int ORDER BY timestamp DESC LIMIT 5;
```

### 5️⃣ Ver Datos en Streamlit
```bash
# Abre navegador → http://localhost:8501
```

## ✅ Verificar que Funciona

### Opción 1: Ver logs del subscriber
```bash
docker-compose logs subscriber -f
# Deberías ver:
# ✅ Connected to MQTT Broker successfully
# 📡 Subscribed to topic: #
# ✅ INT inserted: topic=lake/raw/int, value=...
# ✅ FLOAT inserted: topic=lake/raw/float, value=...
```

### Opción 2: Ver los mensajes MQTT
```bash
# Conectar a Mosquitto desde otra terminal
docker exec mosquitto mosquitto_sub -t '#' -v
```

### Opción 3: Ver logs de PostgreSQL
```bash
docker-compose logs postgres_db -f
```

## 🐛 Si Algo Falla

```bash
# Ver todos los logs
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f subscriber
docker-compose logs -f mosquitto

# Reiniciar un servicio
docker-compose restart subscriber

# Reiniciar todo
docker-compose down
docker-compose up -d

# Ver qué está corriendo
docker-compose ps
```

## 📁 Estructura para Desarrollo Local

```
U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization/
├── docker-compose.yml           # Orquestación
├── mosquitto/
│   └── mosquitto.conf           # Config del broker MQTT
├── init.sql                     # Script de inicialización DB
├── Project_Elements/
│   ├── publisher.ipynb          # Genera datos
│   └── suscriber.ipynb          # Escucha datos
├── subscriber/
│   ├── Dockerfile               # Contenedor del subscriber
│   └── subscriber.py            # Script Python
└── streamlit_app/               # Dashboard
```

## 🔐 Credenciales por Defecto

```
PostgreSQL:
  Usuario: user
  Contraseña: password
  DB: sensordata
  
MQTT (Mosquitto):
  Sin autenticación (para desarrollo)
  Puerto: 1883
```

## 📞 Comandos Útiles

```bash
# Crear backup de datos
docker-compose exec postgres_db pg_dump -U user sensordata > backup.sql

# Restaurar backup
docker-compose exec postgres_db psql -U user sensordata < backup.sql

# Ver estado de servicios
docker-compose ps

# Seguir logs en tiempo real
docker-compose logs -f

# Ejecutar comando en contenedor
docker-compose exec subscriber python -c "import paho.mqtt.client; print('OK')"

# Acceder a shell de PostgreSQL
docker-compose exec postgres_db psql -U user -d sensordata
```

---

¡Listo! Todo debería funcionar 🚀

