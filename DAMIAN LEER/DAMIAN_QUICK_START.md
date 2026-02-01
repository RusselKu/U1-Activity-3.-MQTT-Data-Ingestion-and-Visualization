# ⚡ INICIO RÁPIDO PARA DAMIÁN - Frontend Dashboard

> **Lee primero**: [DAMIAN_FRONTEND_GUIA.md](DAMIAN_FRONTEND_GUIA.md)

---

## 🎯 Lo que Necesitas Saber (en 2 minutos)

### El Backend está LISTO ✅

- Mosquitto publica datos cada 2 segundos
- PostgreSQL ya tiene 96+ registros almacenados
- Todo funciona en Docker

### Tu Tarea: Crear Dashboard Streamlit

**3 Archivos PRINCIPALES a crear:**

#### 1️⃣ `streamlit_app/.env`
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=sensordata
```

#### 2️⃣ `streamlit_app/utils/db_connection.py`
⬜ **Módulo para conectar a PostgreSQL**
- Función: `get_int_data(hours)` → Retorna datos enteros
- Función: `get_float_data(hours)` → Retorna datos flotantes
- Función: `get_stats_int(hours)` → Estadísticas enteros
- Función: `get_stats_float(hours)` → Estadísticas flotantes

👉 [Ver código completo en la guía](DAMIAN_FRONTEND_GUIA.md#paso-3-crear-el-módulo-de-conexión-a-base-de-datos)

#### 3️⃣ `streamlit_app/app.py`
⬜ **Aplicación principal Streamlit**
- 3 pestañas: Datos en Vivo | Estadísticas | Info
- Gráficas Plotly interactivas
- Filtro de tiempo (5min, 1h, 4h, 24h, 7d)
- Métricas: promedio, min, max, total

👉 [Ver código completo en la guía](DAMIAN_FRONTEND_GUIA.md#paso-4-crear-la-página-principal-apppy)

---

## 🚀 Verificación Rápida

```bash
# 1. Verifica que todo esté corriendo
docker-compose ps
# Deberías ver: mosquitto UP, postgres_db UP, subscriber UP

# 2. Instala dependencias (si no lo hiciste)
pip install streamlit plotly pandas psycopg2-binary python-dotenv

# 3. Ejecuta la app
cd streamlit_app
streamlit run app.py

# 4. Abre en tu navegador
# http://localhost:8501
```

---

## 📋 Checklist Mínimo (15 min)

- [ ] Crear `.env` en `streamlit_app/`
- [ ] Crear `utils/db_connection.py`
- [ ] Crear `utils/__init__.py` (vacío)
- [ ] Crear `app.py`
- [ ] Ejecutar: `streamlit run streamlit_app/app.py`
- [ ] Ver gráficas en el navegador ✅

---

## 🎨 Extras (si tienes tiempo)

- [ ] Crear `pages/page1_datos_en_vivo.py` (página adicional)
- [ ] Crear `pages/page2_estadisticas.py` (página adicional)
- [ ] Mejorar estilos CSS
- [ ] Agregar más filtros
- [ ] Agregar exportación a CSV

---

## 🆘 Si Algo No Funciona

1. **"No module named psycopg2"** → `pip install psycopg2-binary`
2. **"Could not connect to server"** → Verifica PostgreSQL: `docker-compose ps`
3. **"No data shown"** → Espera 30 segundos a que acumule datos
4. **"Module not found: utils"** → Verifica que exista `utils/__init__.py`

---

## 📞 Preguntas?

Revisa la **[GUÍA COMPLETA](DAMIAN_FRONTEND_GUIA.md)** para:
- Explicación detallada de cada paso
- Código completo para copiar/pegar
- Troubleshooting exhaustivo
- Instrucciones Docker

**¡Buena suerte! 🚀**
