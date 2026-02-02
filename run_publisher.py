#!/usr/bin/env python3
"""
Publisher MQTT - Genera datos de prueba
Ejecutar: python run_publisher.py
"""

import json
import random
import ssl
import time
import os
import sys
import paho.mqtt.client as mqtt

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Local Mosquitto Configuration
BROKER = os.getenv("MQTT_BROKER", "localhost")
PORT = int(os.getenv("MQTT_PORT", 1883))
USERNAME = os.getenv("MQTT_USER", "")
PASSWORD = os.getenv("MQTT_PASS", "")

TOPIC_INT = "lake/raw/int"
TOPIC_FLOAT = "lake/raw/float"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[CONNECT] Connected successfully to {BROKER}:{PORT}")
    else:
        print(f"[CONNECT ERROR] Failed with code {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"[DISCONNECT WARNING] Unexpected disconnection: {rc}")
    else:
        print("[DISCONNECT] Disconnected successfully")

def on_publish(client, userdata, mid):
    print(f"[PUBLISH ACK] Message {mid} published")

client = mqtt.Client(protocol=mqtt.MQTTv311, client_id="iot_publisher")

# Set credentials if provided
if USERNAME and PASSWORD:
    client.username_pw_set(USERNAME, PASSWORD)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

print(f"[CONNECTING] to {BROKER}:{PORT}...")
client.connect(BROKER, PORT, 60)
client.loop_start()

# Wait for connection
time.sleep(1)

try:
    print("\n" + "="*70)
    print("[RUNNING] PUBLISHER - Generating data every 2 seconds")
    print("="*70 + "\n")
    
    count = 0
    while True:
        int_value = random.randint(0, 1000)
        float_value = round(random.uniform(0, 100), 4)

        payload_int = json.dumps({"value": int_value})
        payload_float = json.dumps({"value": float_value})

        client.publish(TOPIC_INT, payload_int, qos=1)
        client.publish(TOPIC_FLOAT, payload_float, qos=1)

        count += 1
        print(f"[{count}] [PUBLISH] {TOPIC_INT} -> {payload_int}")
        print(f"[{count}] [PUBLISH] {TOPIC_FLOAT} -> {payload_float}")
        print("-" * 70)

        time.sleep(2)

except KeyboardInterrupt:
    print("\n\n[STOP] Publisher stopped by user")
    client.loop_stop()
    client.disconnect()
    print("[OK] Disconnected cleanly")

