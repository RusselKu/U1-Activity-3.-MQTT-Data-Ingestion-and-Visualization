-- This script will be executed when the PostgreSQL container starts for the first time.

-- Create the table for integer sensor data
CREATE TABLE IF NOT EXISTS lake_raw_data_int (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    payload JSONB,
    value BIGINT NOT NULL,
    ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create the table for float sensor data
CREATE TABLE IF NOT EXISTS lake_raw_data_float (
    id SERIAL PRIMARY KEY,
    topic VARCHAR(255) NOT NULL,
    payload JSONB,
    value DOUBLE PRECISION NOT NULL,
    ts TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Create indexes for faster queries on timestamp
CREATE INDEX IF NOT EXISTS idx_int_ts ON lake_raw_data_int(ts);
CREATE INDEX IF NOT EXISTS idx_float_ts ON lake_raw_data_float(ts);
