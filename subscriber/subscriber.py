import ssl
import json
import time
import os
import logging
import paho.mqtt.client as mqtt
import psycopg2
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# MQTT Configuration - Local Mosquitto
BROKER = os.environ.get('MQTT_BROKER', 'mosquitto')
PORT = int(os.environ.get('MQTT_PORT', '1883'))
USERNAME = os.environ.get('MQTT_USER', '')
PASSWORD = os.environ.get('MQTT_PASS', '')
TOPIC = os.environ.get('MQTT_TOPIC', '#')

# PostgreSQL Configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'postgres_db'),
    'port': int(os.environ.get('DB_PORT', '5432')),
    'database': os.environ.get('DB_NAME', 'sensordata'),
    'user': os.environ.get('DB_USER', 'user'),
    'password': os.environ.get('DB_PASSWORD', 'password')
}

def get_db_connection():
    """Create and return a PostgreSQL connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        raise

def insert_int(topic: str, payload: dict, value: int):
    """Insert integer value into lake_raw_data_int table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO lake_raw_data_int (topic, payload, value, timestamp)
            VALUES (%s, %s, %s, %s)
            """,
            (topic, json.dumps(payload), value, datetime.now()),
        )
        conn.commit()
        logger.info(f'✅ INT inserted: topic={topic}, value={value}')
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f'❌ Error inserting INT: {e}')

def insert_float(topic: str, payload: dict, value: float):
    """Insert float value into lake_raw_data_float table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO lake_raw_data_float (topic, payload, value, timestamp)
            VALUES (%s, %s, %s, %s)
            """,
            (topic, json.dumps(payload), value, datetime.now()),
        )
        conn.commit()
        logger.info(f'✅ FLOAT inserted: topic={topic}, value={value}')
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f'❌ Error inserting FLOAT: {e}')

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects"""
    if rc == 0:
        logger.info('✅ Connected to MQTT Broker successfully')
        client.subscribe(TOPIC)
        logger.info(f'📡 Subscribed to topic: {TOPIC}')
    else:
        logger.error(f'❌ Connection failed with code {rc}')

def on_disconnect(client, userdata, rc):
    """Callback for when the client disconnects"""
    if rc != 0:
        logger.warning(f'⚠️ Unexpected disconnection: {rc}')
    else:
        logger.info('👋 Disconnected from MQTT Broker')

def on_message(client, userdata, msg):
    """Callback for when a message is received"""
    try:
        payload_str = msg.payload.decode('utf-8')
        payload = json.loads(payload_str)
        value = payload.get('value')
        
        if value is None:
            logger.warning(f"⚠️ No 'value' key in payload: {payload}")
            return
        
        # Route to appropriate table based on topic
        if msg.topic == "lake/raw/int":
            if isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
                insert_int(msg.topic, payload, int(value))
            else:
                logger.warning(f"⚠️ Expected INT but got {type(value).__name__}: {value}")
        
        elif msg.topic == "lake/raw/float":
            if isinstance(value, (int, float)):
                insert_float(msg.topic, payload, float(value))
            else:
                logger.warning(f"⚠️ Expected FLOAT but got {type(value).__name__}: {value}")
        else:
            logger.debug(f'📨 Message from {msg.topic}: {value}')
    
    except Exception as e:
        logger.error(f'❌ Error processing message: {e}')

def on_log(client, userdata, level, buf):
    """Callback for logging"""
    logger.debug(f'🔍 MQTT LOG: {buf}')

def main():
    """Main function to start MQTT subscriber"""
    logger.info("🚀 Starting MQTT Subscriber...")
    logger.info(f"📍 Broker: {BROKER}:{PORT}")
    logger.info(f"👤 Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}")
    
    client = mqtt.Client(protocol=mqtt.MQTTv311, client_id="iot_subscriber")
    
    # Set credentials if provided
    if USERNAME and PASSWORD:
        client.username_pw_set(USERNAME, PASSWORD)
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_log = on_log
    
    try:
        logger.info(f"🔗 Connecting to {BROKER}:{PORT}...")
        client.connect(BROKER, PORT, keepalive=60)
        logger.info("🔄 Starting network loop...")
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("⛔ Subscriber interrupted by user")
        client.disconnect()
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        client.disconnect()

if __name__ == '__main__':
    # Wait for PostgreSQL to be ready
    logger.info("⏳ Waiting for database to be ready...")
    time.sleep(5)
    main()


def get_db_connection():
    """Create and return a PostgreSQL connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

def insert_int(topic: str, payload: dict, value: int):
    """Insert integer value into lake_raw_data_int table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO lake_raw_data_int (topic, payload, value, timestamp)
            VALUES (%s, %s, %s, %s)
            """,
            (topic, json.dumps(payload), value, datetime.now()),
        )
        conn.commit()
        logger.info(f'✅ INT inserted: topic={topic}, value={value}')
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f'Error inserting INT: {e}')

def insert_float(topic: str, payload: dict, value: float):
    """Insert float value into lake_raw_data_float table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO lake_raw_data_float (topic, payload, value, timestamp)
            VALUES (%s, %s, %s, %s)
            """,
            (topic, json.dumps(payload), value, datetime.now()),
        )
        conn.commit()
        logger.info(f'✅ FLOAT inserted: topic={topic}, value={value}')
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f'Error inserting FLOAT: {e}')

def on_connect(client, userdata, flags, rc):
    """Callback for when the client connects"""
    if rc == 0:
        logger.info('✅ Connected to MQTT Broker successfully')
        client.subscribe(TOPIC)
        logger.info(f'📡 Subscribed to topic: {TOPIC}')
    else:
        logger.error(f'❌ Connection failed with code {rc}')

def on_disconnect(client, userdata, rc):
    """Callback for when the client disconnects"""
    if rc != 0:
        logger.warning(f'⚠️ Unexpected disconnection: {rc}')
    else:
        logger.info('👋 Disconnected from MQTT Broker')

def on_message(client, userdata, msg):
    """Callback for when a message is received"""
    try:
        payload_str = msg.payload.decode('utf-8')
        payload = json.loads(payload_str)
        value = payload.get('value')
        
        if value is None:
            logger.warning(f"⚠️ No 'value' key in payload: {payload}")
            return
        
        # Route to appropriate table based on topic
        if msg.topic == "lake/raw/int":
            if isinstance(value, int) or (isinstance(value, float) and value.is_integer()):
                insert_int(msg.topic, payload, int(value))
            else:
                logger.warning(f"⚠️ Expected INT but got {type(value).__name__}: {value}")
        
        elif msg.topic == "lake/raw/float":
            if isinstance(value, (int, float)):
                insert_float(msg.topic, payload, float(value))
            else:
                logger.warning(f"⚠️ Expected FLOAT but got {type(value).__name__}: {value}")
        else:
            logger.debug(f'Message from {msg.topic}: {value}')
    
    except Exception as e:
        logger.error(f'Error processing message: {e}')

def on_log(client, userdata, level, buf):
    """Callback for logging"""
    logger.debug(f'MQTT LOG: {buf}')

def main():
    """Main function to start MQTT subscriber"""
    logger.info("🚀 Starting MQTT Subscriber...")
    logger.info(f"📍 Broker: {BROKER}:{PORT}")
    logger.info(f"👤 Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}")
    
    client = mqtt.Client(protocol=mqtt.MQTTv311, client_id="iot_subscriber")
    
    # Set credentials
    if USERNAME and PASSWORD:
        client.username_pw_set(USERNAME, PASSWORD)
    
    # Configure TLS/SSL for CloudAMQP
    if int(PORT) == 8883:
        client.tls_set(
            tls_version=ssl.PROTOCOL_TLSv1_2,
            cert_reqs=ssl.CERT_NONE
        )
        client.tls_insecure_set(True)
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_log = on_log
    
    try:
        client.connect(BROKER, PORT, keepalive=60)
        logger.info("🔄 Starting network loop...")
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("⛔ Subscriber interrupted by user")
        client.disconnect()
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        client.disconnect()

if __name__ == '__main__':
    main()

