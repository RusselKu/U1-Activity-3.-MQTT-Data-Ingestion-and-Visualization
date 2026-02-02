#!/usr/bin/env python3
"""
Script para inicializar la base de datos PostgreSQL con las tablas necesarias.
Ejecutar después de que PostgreSQL esté corriendo en Docker.
"""

import psycopg2
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'database': os.getenv('DB_NAME', 'iot_course'),
    'user': os.getenv('DB_USER', 'iot_usr'),
    'password': os.getenv('DB_PASSWORD', 'upy_student_Admin1')
}

SQL_SCRIPT = """
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
CREATE INDEX IF NOT EXISTS idx_topic_int ON lake_raw_data_int(topic);
CREATE INDEX IF NOT EXISTS idx_topic_float ON lake_raw_data_float(topic);
CREATE INDEX IF NOT EXISTS idx_timestamp_int ON lake_raw_data_int(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_timestamp_float ON lake_raw_data_float(timestamp DESC);
"""

def main():
    print("🔧 Inicializando base de datos PostgreSQL...\n")
    print(f"📍 Conectando a: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    
    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("✅ Conexión exitosa\n")
        
        # Ejecutar script SQL
        print("📝 Creando tablas...")
        cur.execute(SQL_SCRIPT)
        conn.commit()
        print("✅ Tablas creadas exitosamente\n")
        
        # Verificar tablas creadas
        print("📋 Verificando tablas...")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_name IN ('lake_raw_data_int', 'lake_raw_data_float')
        """)
        
        tables = cur.fetchall()
        for table in tables:
            print(f"   ✅ {table[0]}")
        
        print("\n" + "="*50)
        print("✅ INICIALIZACIÓN COMPLETADA")
        print("="*50)
        print("\nLa base de datos está lista para recibir datos.")
        print("\nPróximos pasos:")
        print("1. Ejecutar: python subscriber/subscriber.py")
        print("2. Ejecutar: jupyter notebook Project_Elements/publisher.ipynb")
        print("3. Ver datos en Streamlit: http://localhost:8501")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nSolución de problemas:")
        print("1. Verificar que PostgreSQL está corriendo: docker-compose ps")
        print("2. Verificar credenciales en .env")
        print("3. Reintentar: docker-compose restart db")
        sys.exit(1)

if __name__ == "__main__":
    main()
