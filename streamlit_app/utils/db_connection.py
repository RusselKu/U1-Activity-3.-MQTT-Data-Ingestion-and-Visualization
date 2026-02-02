import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
import streamlit as st

# Cargar variables de entorno desde .env
load_dotenv()

@st.cache_resource
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            dbname=os.getenv("DB_NAME"),
            connect_timeout=5,  # Agregado para evitar esperas largas
            client_encoding='UTF8'
        )
        return conn
    except Exception as e:
        st.error("❌ Error conectando a la base de datos (verifica Docker y credenciales).")
        st.code(str(e).encode('utf-8', errors='replace').decode('utf-8'))
        return None

def query_data(query, params=None):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        return pd.read_sql(query, conn, params=params)
    except Exception as e:
        st.error("❌ Error ejecutando consulta SQL")
        st.code(str(e).encode('utf-8', errors='replace').decode('utf-8'))
        return None

def get_int_data(hours=1):
    query = """
    SELECT id, topic, value, timestamp
    FROM lake_raw_data_int
    WHERE timestamp >= NOW() - INTERVAL %s
    ORDER BY timestamp ASC;
    """
    return query_data(query, (f"{hours} hours",))

def get_float_data(hours=1):
    query = """
    SELECT id, topic, value, timestamp
    FROM lake_raw_data_float
    WHERE timestamp >= NOW() - INTERVAL %s
    ORDER BY timestamp ASC;
    """
    return query_data(query, (f"{hours} hours",))

def get_stats_int(hours=1):
    query = """
    SELECT COUNT(*) AS total,
           AVG(value) AS promedio,
           MIN(value) AS minimo,
           MAX(value) AS maximo,
           STDDEV(value) AS desv_std
    FROM lake_raw_data_int
    WHERE timestamp >= NOW() - INTERVAL %s;
    """
    return query_data(query, (f"{hours} hours",))

def get_stats_float(hours=1):
    query = """
    SELECT COUNT(*) AS total,
           AVG(value) AS promedio,
           MIN(value) AS minimo,
           MAX(value) AS maximo,
           STDDEV(value) AS desv_std
    FROM lake_raw_data_float
    WHERE timestamp >= NOW() - INTERVAL %s;
    """
    return query_data(query, (f"{hours} hours",))