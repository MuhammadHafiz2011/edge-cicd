import json
import time
import requests
import paho.mqtt.client as mqtt

BROKER_HOST = "mqtt-broker"
BROKER_PORT = 1883
TOPIC = "sensor/temperature"

def on_connect(client, userdata, flags, rc):
    print("Receiver connected with result code:", rc)
    client.subscribe(TOPIC)
    print("Subscribed to topic:", TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print("Received data:", data)

        response = requests.post(
            "http://gateway:5000/ingest",
            json=data,
            timeout=3
        )
        print("Forwarded to gateway:", response.status_code)

    except Exception as e:
        print("Error:", e)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("Receiver starting, connecting to broker:", BROKER_HOST)

while True:
    try:
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        break
    except Exception as e:
        print("Connection failed, retrying...", e)
        time.sleep(3)

client.loop_forever()
