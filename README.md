# 🚀 IoT MQTT Data Ingestion and Visualization (Mosquitto Local)

Un sistema completo de ingesta, almacenamiento y visualización de datos IoT utilizando Mosquitto (MQTT local), PostgreSQL y Streamlit.

**Perfectamente diseñado para proyectos escolares y desarrollo local.**

## 📋 Arquitectura del Sistema

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

## 🎯 Componentes Principales

### 1. **Mosquitto MQTT Broker**
- Broker MQTT local en Docker
- Puerto 1883 (MQTT) y 9001 (WebSocket)
- Sin autenticación (desarrollo)
- Configuración en `mosquitto/mosquitto.conf`

### 2. **PostgreSQL Database**
- Base de datos relacional
- Tablas para datos enteros y flotantes
- Inicialización automática con `init.sql`
- Puerto 5432

### 3. **Publisher** (`Project_Elements/publisher.ipynb`)
- Publica datos aleatorios en MQTT
- Tópicos:
  - `lake/raw/int` → valores enteros
  - `lake/raw/float` → valores flotantes
- Se ejecuta en Jupyter Notebook

### 4. **Subscriber** (Docker Service)
- Escucha mensajes MQTT desde Mosquitto
- Almacena datos en PostgreSQL automáticamente
- Se ejecuta como contenedor Docker
- Código en `subscriber/subscriber.py`

### 5. **Streamlit Dashboard**
- Visualización de datos en tiempo real
- Gráficos interactivos
- Accesible en `http://localhost:8501`

## � Guías por Rol

### 🔧 Para Rivaldo (Backend)
✅ **COMPLETADO** - Backend totalmente funcional
- [Verificación de Rivaldo](DAMIAN_QUICK_START.md#verificación-rápida) en la guía de pruebas

### 🎨 Para Damián (Frontend)
⏳ **EN PROGRESO** - Tu dashboard Streamlit necesita ser construido

📖 **Lee primero**: [DAMIAN_QUICK_START.md](DAMIAN_QUICK_START.md) (2 min)  
📚 **Guía completa**: [DAMIAN_FRONTEND_GUIA.md](DAMIAN_FRONTEND_GUIA.md) (30 min)

---

## 🚀 Inicio Rápido (3 Comandos)

```bash
# 1. Clonar y navegar
cd U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization

# 2. Iniciar todos los servicios
docker-compose up -d

# 3. Ejecutar el publisher
python run_publisher.py
# O desde Jupyter: jupyter notebook Project_Elements/publisher.ipynb
```

**¡Eso es! Ya está corriendo.** Los datos fluyen automáticamente.

### Acceso a Servicios

- 📊 **Streamlit Dashboard**: http://localhost:8501 (cuando Damián cree la app)
- 🗄️ **PostgreSQL**: localhost:5432 (usuario: `user`, contraseña: `password`)
- 📡 **MQTT Broker**: localhost:1883

## 📁 Estructura del Proyecto

```
U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization/
├── docker-compose.yml          # Orquestación Docker
├── init.sql                    # Script SQL de inicialización
├── .env.example                # Variables de entorno
│
├── mosquitto/
│   └── mosquitto.conf          # Configuración del broker MQTT
│
├── Project_Elements/
│   ├── publisher.ipynb         # Genera datos aleatorios
│   ├── suscriber.ipynb         # Cliente MQTT (Jupyter)
│   └── requirements.txt
│
├── subscriber/
│   ├── Dockerfile              # Contenedor del servicio
│   ├── subscriber.py           # Script del suscriptor
│   └── requirements.txt
│
├── streamlit_app/
│   ├── Dockerfile
│   ├── app.py                  # Dashboard principal
│   └── requirements.txt
│
└── [Documentación]
    ├── README.md               # Este archivo
    ├── QUICKSTART.md           # Inicio rápido
    ├── CHANGELOG.md            # Cambios
    └── COMPLETION_SUMMARY.md   # Resumen
```

## 🔧 Configuración

### Variables de Entorno (`.env`)

```env
# PostgreSQL
DB_HOST=postgres_db
DB_PORT=5432
DB_NAME=sensordata
DB_USER=user
DB_PASSWORD=password

# MQTT Mosquitto
MQTT_BROKER=mosquitto
MQTT_PORT=1883
MQTT_USER=           # Dejar vacío
MQTT_PASS=           # Dejar vacío
MQTT_TOPIC=#

# Streamlit
STREAMLIT_PORT=8501
```

### Credenciales por Defecto

```
PostgreSQL:
  • Usuario: user
  • Contraseña: password
  • DB: sensordata

Mosquitto:
  • Sin autenticación (es desarrollo)
  • Puerto: 1883
```

## 🐳 Comandos Docker Principales

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Ver logs de un servicio
docker-compose logs -f subscriber

# Detener servicios
docker-compose down

# Reiniciar
docker-compose restart

# Estado de servicios
docker-compose ps
```

## 📊 SQL Queries Útiles

```sql
-- Ver datos enteros recientes
SELECT * FROM lake_raw_data_int 
ORDER BY timestamp DESC LIMIT 10;

-- Ver datos flotantes recientes
SELECT * FROM lake_raw_data_float 
ORDER BY timestamp DESC LIMIT 10;

-- Contar registros
SELECT COUNT(*) FROM lake_raw_data_int;
SELECT COUNT(*) FROM lake_raw_data_float;

-- Estadísticas
SELECT 
  COUNT(*) as total,
  AVG(value) as promedio,
  MIN(value) as minimo,
  MAX(value) as maximo
FROM lake_raw_data_int;

-- Ver últimas 5 inserciones
SELECT * FROM events_log ORDER BY timestamp DESC LIMIT 5;
```

## 🔌 Acceder a PostgreSQL Directamente

```bash
# Desde Docker
docker-compose exec postgres_db psql -U user -d sensordata

# Desde tu computadora (si tienes psql instalado)
psql -h localhost -U user -d sensordata
# Contraseña: password
```

## 📈 Flujo de Datos

```
1. Publisher genera un dato aleatorio
2. Publica en MQTT Broker (Mosquitto)
3. Subscriber escucha el evento
4. Subscriber inserta en PostgreSQL
5. Streamlit lee de PostgreSQL
6. Dashboard muestra el dato en tiempo real
```

## 🐛 Solución de Problemas

### Error: "Connection refused"
```bash
# Verificar que los servicios están corriendo
docker-compose ps

# Si no están, iniciar
docker-compose up -d
```

### Error: "Cannot connect to MQTT"
```bash
# Verificar Mosquitto está corriendo
docker-compose logs mosquitto

# Reiniciar Mosquitto
docker-compose restart mosquitto
```

### Error: "Database does not exist"
```bash
# Las tablas se crean automáticamente con init.sql
# Si no, reinicia PostgreSQL
docker-compose restart postgres_db
```

### Datos no aparecen en Streamlit
```bash
# Verificar que subscriber está activo
docker-compose logs subscriber -f

# Verificar que hay datos en DB
docker-compose exec postgres_db psql -U user -d sensordata -c "SELECT COUNT(*) FROM lake_raw_data_int"
```

## 🚀 Expandir el Proyecto

### Agregar más tópicos MQTT
Edita `Project_Elements/publisher.ipynb` para publicar en nuevos tópicos.

### Agregar más gráficos
Edita `streamlit_app/app.py` para agregar visualizaciones.

### Cambiar credenciales de BD
Edita `docker-compose.yml` y `.env`.

## 📚 Documentación Adicional

- **QUICKSTART.md** - Guía de 5 pasos
- **CHANGELOG.md** - Qué cambió
- **COMPLETION_SUMMARY.md** - Resumen de trabajo completado
- **ElementosClaveParaLevantarTodo.md** - Instrucciones SQL detalladas

## 🎓 Para Aprender

Este proyecto demuestra:
- ✅ Arquitectura IoT moderna
- ✅ Brokers MQTT (Mosquitto)
- ✅ Bases de datos relacional (PostgreSQL)
- ✅ Docker y contenedores
- ✅ Python para backend
- ✅ Streamlit para dashboards
- ✅ Desarrollo ágil

## 📝 Notas Importantes

- **Desarrollo local**: Todo corre en tu computadora
- **Sin dependencias externas**: No necesitas internet
- **Fácil de expandir**: Agregar sensores es simple
- **Listo para clase**: Documentado y probado
- **Open Source**: Puedes modificar todo

---

**Estado**: ✅ Producción Ready (Escolar)
**Última actualización**: Febrero 2026
**Diseño**: Proyecto educativo

¡Listo para usar! 🎉

