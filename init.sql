-- Script de inicialización de PostgreSQL
-- Este archivo se ejecuta automáticamente cuando PostgreSQL inicia por primera vez

-- Crear tabla para datos enteros
CREATE TABLE IF NOT EXISTS lake_raw_data_int (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    payload JSONB,
    value INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla para datos flotantes
CREATE TABLE IF NOT EXISTS lake_raw_data_float (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    payload JSONB,
    value FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Crear índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_topic_int ON lake_raw_data_int(topic);
CREATE INDEX IF NOT EXISTS idx_topic_float ON lake_raw_data_float(topic);
CREATE INDEX IF NOT EXISTS idx_timestamp_int ON lake_raw_data_int(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_timestamp_float ON lake_raw_data_float(timestamp DESC);

-- Crear tabla de log de eventos
CREATE TABLE IF NOT EXISTS events_log (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar un evento de bienvenida
INSERT INTO events_log (event_type, message) 
VALUES ('INIT', 'Database initialized successfully');

-- Mostrar tablas creadas
SELECT 'Tablas creadas:' as status;
\dt
