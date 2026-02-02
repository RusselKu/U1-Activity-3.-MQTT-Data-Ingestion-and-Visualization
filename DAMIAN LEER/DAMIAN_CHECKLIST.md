# 📋 Checklist Visual para Damián - Dashboard Streamlit

## 📌 Estado del Proyecto

```
✅ RIVALDO - Backend (COMPLETADO)
├── ✅ Mosquitto MQTT local
├── ✅ PostgreSQL 13
├── ✅ Subscriber corriendo
├── ✅ 96+ registros en lake_raw_data_int
├── ✅ 98+ registros en lake_raw_data_float
└── ✅ Publisher en ejecución

🚀 DAMIÁN - Frontend (POR HACER)
├── 🔲 Crear .env
├── 🔲 Crear utils/db_connection.py
├── 🔲 Crear app.py
├── 🔲 Probar localmente
└── 🔲 Validar gráficas
```

---

## 🎯 Tu Misión - 3 Fases

### FASE 1: PREPARACIÓN (5 min)

- [ ] Leer [DAMIAN_QUICK_START.md](DAMIAN_QUICK_START.md)
- [ ] Verificar que Docker esté corriendo:
  ```bash
  docker-compose ps
  ```
  Deberías ver:
  ```
  mosquitto    UP
  postgres_db  UP
  subscriber   UP
  ```

### FASE 2: CREACIÓN (15 min)

#### Archivo 1: `streamlit_app/.env`
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=user
DB_PASSWORD=password
DB_NAME=sensordata
```
- [ ] Copiar este contenido exactamente

#### Archivo 2: `streamlit_app/utils/__init__.py`
```python
# Archivo vacío - solo marca utils como módulo Python
```
- [ ] Crear archivo vacío

#### Archivo 3: `streamlit_app/utils/db_connection.py`
Contiene 6 funciones principales:
```python
@st.cache_resource
def get_db_connection()
    # Conexión a PostgreSQL

def query_data(query, params=None)
    # Ejecuta consultas SQL

def get_int_data(hours=1)
    # Obtiene datos enteros

def get_float_data(hours=1)
    # Obtiene datos flotantes

def get_stats_int(hours=1)
    # Estadísticas de enteros

def get_stats_float(hours=1)
    # Estadísticas de flotantes
```
- [ ] Copiar código de la guía (sección 3)
- [ ] Crear archivo

#### Archivo 4: `streamlit_app/app.py`
Estructura principal:
```
Página Principal
├── Barra Lateral
│   ├── Selector de rango (5min, 1h, 4h, 24h, 7d)
│   └── Botón Refrescar
└── Pestañas
    ├── Tab 1: Datos en Vivo
    │   ├── Gráfica Enteros
    │   └── Gráfica Flotantes
    ├── Tab 2: Estadísticas
    │   ├── Métricas Enteros
    │   └── Métricas Flotantes
    └── Tab 3: Información
        └── Documentación
```
- [ ] Copiar código de la guía (sección 4)
- [ ] Crear archivo

### FASE 3: PRUEBAS (5 min)

#### Prueba Local
- [ ] Abre terminal en `streamlit_app`
- [ ] Ejecuta:
  ```bash
  streamlit run app.py
  ```
- [ ] Abre http://localhost:8501 en navegador
- [ ] Verifica:
  - [ ] Dashboard carga sin errores
  - [ ] Tab "Datos en Vivo" muestra gráficas
  - [ ] Hay datos en ambas gráficas
  - [ ] Selector de tiempo funciona
  - [ ] Botón "Refrescar" actualiza datos
  - [ ] Tab "Estadísticas" muestra métricas

#### Prueba con Docker (Opcional)
- [ ] Ejecuta: `docker-compose up -d streamlit`
- [ ] Accede a http://localhost:8501
- [ ] Verifica todo funciona igual

---

## 🎨 Validación Visual

### Gráfica de Datos Enteros debe mostrar:
```
Serie de Tiempo - Valores Enteros
┌─────────────────────────────────┐
│                                 │
│  Línea azul con puntos         │
│  (subiendo/bajando en tiempo)   │
│                                 │
└─────────────────────────────────┘
Registros: 96+
```

### Gráfica de Datos Flotantes debe mostrar:
```
Serie de Tiempo - Valores Flotantes
┌─────────────────────────────────┐
│                                 │
│  Línea naranja con puntos      │
│  (subiendo/bajando en tiempo)   │
│                                 │
└─────────────────────────────────┘
Registros: 98+
```

### Tab Estadísticas debe mostrar:
```
┌─ DATOS ENTEROS ──┬─ DATOS FLOTANTES ─┐
│ Total: 96        │ Total: 98         │
│ Promedio: 500.5  │ Promedio: 50.2    │
│ Mínimo: 70       │ Mínimo: 0.45      │
│ Máximo: 995      │ Máximo: 95.66     │
│ Desv. Est: 288   │ Desv. Est: 29.1   │
└──────────────────┴───────────────────┘
```

---

## 📁 Estructura Final Esperada

```
✅ streamlit_app/
   ├── .env                         ← CREAR
   ├── app.py                       ← CREAR
   ├── Dockerfile                   ✅ Existe
   ├── requirements.txt             ✅ Existe
   ├── requirement.txt              ⚠️  Renombrar a requirements.txt
   ├── utils/
   │   ├── __init__.py             ← CREAR
   │   └── db_connection.py        ← CREAR
   ├── pages/
   │   ├── __init__.py             (opcional)
   │   └── (archivos adicionales)   (opcional)
   └── styles/
       └── (archivos opcionales)    (opcional)
```

---

## 🚨 Problemas Comunes y Soluciones

### ❌ "ModuleNotFoundError: No module named 'streamlit'"
```bash
pip install streamlit plotly pandas psycopg2-binary python-dotenv
```

### ❌ "could not connect to server: Connection refused"
Verifica:
1. Docker está corriendo: `docker-compose ps`
2. PostgreSQL está UP
3. `.env` tiene `DB_HOST=localhost`

### ❌ "No data appearing in charts"
1. Espera 30 segundos (el publisher publica cada 2 seg)
2. Haz clic en "Refrescar"
3. Verifica logs: `docker-compose logs subscriber`

### ❌ "ModuleNotFoundError: No module named 'utils'"
Verifica que exista `streamlit_app/utils/__init__.py`

### ❌ "AttributeError: 'NoneType' object..."
Verifica conexión a base de datos:
- `.env` con credenciales correctas
- PostgreSQL corriendo: `docker-compose ps`

---

## 🎯 Orden Recomendado de Creación

1. **Primero**: `.env` (30 seg)
2. **Segundo**: `utils/__init__.py` (10 seg)
3. **Tercero**: `utils/db_connection.py` (5 min)
4. **Cuarto**: `app.py` (5 min)
5. **Quinto**: Pruebas (5 min)

**Tiempo total: 15-20 minutos** ⏱️

---

## 📚 Recursos

- **Guía Rápida**: [DAMIAN_QUICK_START.md](DAMIAN_QUICK_START.md)
- **Guía Completa**: [DAMIAN_FRONTEND_GUIA.md](DAMIAN_FRONTEND_GUIA.md)
- **Documentación Streamlit**: https://docs.streamlit.io/
- **Plotly Gráficas**: https://plotly.com/python/

---

## ✨ Desafíos Extras (si terminas rápido)

- [ ] Agregar tema oscuro/claro
- [ ] Exportar datos a CSV
- [ ] Agregar gráfica de distribución (histograma)
- [ ] Mostrar última actualización con timestamp
- [ ] Agregar predicción simple de tendencia
- [ ] Email con alertas si valores salen de rango

---

## 📞 Estado de Tareas

| Tarea | Estado | Responsable |
|-------|--------|-------------|
| Backend MQTT+PostgreSQL | ✅ Done | Rivaldo |
| Publisher Verification | ✅ Done | Rivaldo |
| Frontend Dashboard | 🔄 In Progress | **Damián** |
| Estadísticas Avanzadas | ⏳ Backlog | - |

---

**¡Vamos Damián! Tú puedes hacerlo! 🚀**

Cualquier duda, revisa la guía completa o el código proporcionado.
