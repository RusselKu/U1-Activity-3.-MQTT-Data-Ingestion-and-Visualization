import os
import json
import time
import paho.mqtt.client as mqtt
import psycopg2

# --- Configuration from Environment Variables ---
MQTT_BROKER = os.environ.get("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_TOPIC = os.environ.get("MQTT_TOPIC", "#") # Subscribe to all topics by default

DB_HOST = os.environ.get("DB_HOST", "postgres_db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "sensordata")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASS = os.environ.get("DB_PASS", "password")

# --- Database Functions ---

def get_db_connection():
    """Establishes a persistent connection to the database."""
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASS
            )
            print("Database connection successful.")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Database connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def insert_data(conn, topic, payload, value):
    """Inserts data into the appropriate table based on value type."""
    table_name = ""
    if isinstance(value, int):
        table_name = "lake_raw_data_int"
    elif isinstance(value, float):
        table_name = "lake_raw_data_float"
    else:
        # If the value is not int or float, we don't insert it.
        return

    try:
        with conn.cursor() as cur:
            sql = f"""
                INSERT INTO {table_name} (topic, payload, value)
                VALUES (%s, %s, %s)
            """
            cur.execute(sql, (topic, json.dumps(payload), value))
        conn.commit()
    except (psycopg2.Error, psycopg2.OperationalError) as e:
        print(f"Error inserting data: {e}")
        # In case of connection error, we can try to reconnect or handle it as needed.
        # For simplicity, we'll let the main loop handle reconnection if the script restarts.

# --- MQTT Callbacks ---

def on_connect(client, userdata, flags, rc, properties=None):
    """Callback for when the client connects to the broker."""
    if rc == 0:
        print(f"Connected to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_message(client, userdata, msg):
    """Callback for when a message is received from the broker."""
    db_conn = userdata['db_conn']
    print(f"Received message on topic: {msg.topic}")
    try:
        payload_str = msg.payload.decode("utf-8")
        payload_json = json.loads(payload_str)
        value = payload_json.get("value")

        if value is None:
            print("Discarding message: 'value' key not found in payload.")
            return

        if not isinstance(value, (int, float)):
            print(f"Discarding message: value '{value}' is not a number.")
            return

        print(f"  -> Parsed value: {value} (Type: {type(value).__name__})")
        insert_data(db_conn, msg.topic, payload_json, value)

    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        print(f"Discarding message: Invalid payload format. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main Execution ---

def connect_to_mqtt(client):
    """Establishes a persistent connection to the MQTT broker."""
    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            # loop_start() is non-blocking and handles reconnection automatically.
            client.loop_start()
            return
        except (ConnectionRefusedError, OSError) as e:
            print(f"MQTT connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    db_connection = get_db_connection()

    if db_connection:
        # Initialize client with the recommended V2 callback API to avoid DeprecationWarning
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.user_data_set({'db_conn': db_connection})
        client.on_connect = on_connect
        client.on_message = on_message

        connect_to_mqtt(client)

        # Keep the main thread alive, as loop_start() is in a background thread.
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Subscriber shutting down.")
        finally:
            client.loop_stop()
            db_connection.close()
            print("MQTT loop stopped and database connection closed.")
