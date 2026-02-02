# 📝 CHANGELOG - Cambios Realizados

Registro de cambios realizados en el proyecto IoT MQTT Data Ingestion.

## ✅ Cambios Completados (Febrero 2026)

### 🧹 Limpieza del Repositorio

#### docker-compose.yml
- ✅ **Removido**: Servicios Airflow (webserver, scheduler)
- ✅ **Removido**: Servicio MongoDB
- ✅ **Actualizado**: Servicio PostgreSQL renombrado de `postgres` a `db`
- ✅ **Actualizado**: Configuración de PostgreSQL para usar credenciales IoT
- ✅ **Actualizado**: Servicio Streamlit para conectarse a `db` en lugar de MongoDB
- ✅ **Resultado**: Archivo más limpio, enfocado en IoT

#### Dockerfile
- ✅ **Verificado**: Ya usa `python:3.11-slim-buster` (imagen apropiada)
- ✅ **Verificado**: No contiene referencias a Airflow
- ✅ **Estado**: Listo para usar

#### requirements.txt
- ✅ **Agregado**: `paho-mqtt` (para cliente MQTT)
- ✅ **Agregado**: `psycopg2-binary` (para PostgreSQL)
- ✅ **Agregado**: `sqlalchemy` (ORM opcional)
- ✅ **Agregado**: `requests` (para APIs)
- ✅ **Removido**: Dependencias de Airflow
- ✅ **Removido**: Dependencias de MongoDB (pymongo)

#### .gitignore
- ✅ **Verificado**: No contiene referencias explícitas a Airflow (mejor práctica)
- ✅ **Estado**: OK - sigue patrones estándar de Python

### 📥 Adaptación del Subscriber

#### Project_Elements/suscriber.ipynb
- ✅ **Celda 1**: Actualizada configuración MQTT y PostgreSQL
  - Agregadas variables de entorno con valores por defecto
  - Explicaciones mejoradas
  - Configuración para Docker y local

- ✅ **Celda 2**: Refactorización de funciones de inserción
  - Nueva función `get_db_connection()`
  - Manejo robusto de errores
  - Mejor logging
  - Agregado timestamp automático

- ✅ **Celda 3**: Actualización de manejador de mensajes
  - Lógica mejorada de enrutamiento de datos
  - Validación de tipos correcta
  - Mensajes de estado en emojis

- ✅ **Celda 4**: Función principal mejorada
  - Agregada función `main()` con mejor estructura
  - Logging informativos
  - Manejo de desconexión

#### subscriber/subscriber.py
- ✅ **Completamente refactorizado**:
  - Removida dependencia de SQLite
  - Configuración consistente con docker-compose
  - Mejor logging
  - Variables de entorno con valores por defecto
  - Funciones de inserción mejoradas

### 📡 Verificación del Publisher

#### Project_Elements/publisher.ipynb
- ✅ **Verificado**: Publica correctamente en:
  - `lake/raw/int` - valores enteros
  - `lake/raw/float` - valores flotantes
- ✅ **Estado**: Funcional - sin cambios requeridos

### 📚 Documentación

#### Archivos Nuevos Creados

1. **README.md**
   - Arquitectura del sistema con diagrama ASCII
   - Componentes principales descritos
   - Guía de inicio rápido
   - Estructura del proyecto
   - Configuración explicada
   - SQL queries útiles
   - Solución de problemas

2. **ElementosClaveParaLevantarTodo.md** (Renovado)
   - Instrucciones paso a paso
   - Comandos SQL para crear tablas
   - Docker Compose instructions
   - Verificación del sistema
   - Solución de problemas
   - Notas importantes

3. **.env.example**
   - Template para variables de entorno
   - Todas las configuraciones documentadas

4. **subscriber/requirements.txt**
   - Dependencias específicas para subscriber
   - Versiones fijadas

5. **verify_setup.py**
   - Script de verificación del sistema
   - Chequea archivos, Docker, Python
   - Guía de próximos pasos

6. **init_db.py**
   - Script para inicializar base de datos
   - Crea tablas automáticamente
   - Manejo de errores mejorado

### 🔄 Cambios de Configuración

#### Variables de Entorno
- `DB_HOST` → `db` (para Docker) o `localhost` (local)
- `DB_PASSWORD` → `upy_student_Admin1`
- `DB_USER` → `iot_usr`
- `MQTT_BROKER` → `bird.lmq.cloudamqp.com`
- `MQTT_PORT` → `8883`

## 📊 Resumen de Cambios

| Área | Antes | Después |
|------|-------|---------|
| BD | MongoDB | PostgreSQL |
| Orquestación | Apache Airflow | Docker Compose simple |
| Subscriber | MongoDB SDK | psycopg2 |
| Documentación | Mínima | Completa |
| Scripts de Setup | Ninguno | verify_setup.py, init_db.py |

## 🎯 Estado de las Tareas de Rivaldo

### ✅ Completadas

1. **Limpieza del Repositorio**
   - ✅ Eliminar referencias a Airflow en docker-compose.yml
   - ✅ Actualizar requirements.txt (quitar pymongo, airflow)
   - ✅ Actualizar Dockerfile (verificado OK)
   - ✅ Limpiar ElementosClaveParaLevantarTodo.md

2. **Subscriber MQTT + PostgreSQL**
   - ✅ Adaptar suscriber.ipynb para psycopg2
   - ✅ Conectar a PostgreSQL usando servicio `db`
   - ✅ Insertar en `lake_raw_data_int` y `lake_raw_data_float`
   - ✅ Actualizar subscriber.py

3. **Verificación del Publisher**
   - ✅ Revisar que publisher.ipynb funciona
   - ✅ Asegurar publicación en `lake/raw/int` y `lake/raw/float`
   - ✅ Documentación agregada

## 🚀 Próximos Pasos

### Para Suncho (Documentación con Screenshots)
1. Ejecutar publisher.ipynb
2. Capturar:
   - Salida del publisher (tópicos y valores)
   - Logs de conexión
   - Datos en pgAdmin o CLI de PostgreSQL
3. Documentar en archivo separado

### Para el Equipo
1. Ejecutar `python verify_setup.py`
2. Ejecutar `python init_db.py`
3. Probar Publisher → Subscriber → Streamlit
4. Validar datos en PostgreSQL

### Mejoras Futuras
- [ ] Agregar pgAdmin a docker-compose.yml
- [ ] Crear Dockerfile para subscriber
- [ ] Agregar tests unitarios
- [ ] Implementar CI/CD
- [ ] Agregar autenticación a Streamlit

## 📝 Notas Importantes

- El proyecto ahora es completamente independiente de Airflow y MongoDB
- PostgreSQL es la única BD, con datos persistentes
- MQTT usa CloudAMQP (credenciales en variables de entorno)
- Todos los servicios se pueden ejecutar con Docker Compose
- Se pueden ejecutar Publisher/Subscriber localmente o en Docker

## 🔗 Archivos Modificados

```
U1-Activity-3.-MQTT-Data-Ingestion-and-Visualization/
├── ✏️ docker-compose.yml (Refactorizado)
├── ✅ Dockerfile (Verificado)
├── ✏️ requirements.txt (Actualizado)
├── ✏️ .gitignore (Verificado)
├── 🆕 ElementosClaveParaLevantarTodo.md (Reescrito)
├── 🆕 README.md (Creado)
├── 🆕 .env.example (Creado)
├── 🆕 verify_setup.py (Creado)
├── 🆕 init_db.py (Creado)
├── 🆕 CHANGELOG.md (Este archivo)
├── Project_Elements/
│   ├── ✏️ suscriber.ipynb (Refactorizado)
│   └── ✅ publisher.ipynb (Verificado)
├── subscriber/
│   ├── ✏️ subscriber.py (Refactorizado)
│   └── 🆕 requirements.txt (Creado)
└── streamlit_app/
    └── ✏️ Dockerfile (Actualizado)
```

---

**Última actualización:** 01 de Febrero de 2026
**Autor:** GitHub Copilot
**Estado:** ✅ Completado
