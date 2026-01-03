import json
import time
import random
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "sensor/temperature"

client = mqtt.Client()
client.connect(BROKER_HOST, BROKER_PORT, 60)

print("Sensor simulator started...")

try:
    while True:
        data = {
            "temperature": round(random.uniform(25.0, 30.0), 2)
        }
        payload = json.dumps(data)
        client.publish(TOPIC, payload)
        print(f"Published: {payload}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Sensor stopped.")
    client.disconnect()
