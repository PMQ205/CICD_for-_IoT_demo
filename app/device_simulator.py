import paho.mqtt.client as mqtt

from app.database import init_db, save_event


MQTT_BROKER = "localhost"
MQTT_PORT = 1883

TOPIC = "iot/device/ESP32_01/command"


def on_connect(client, userdata, flags, reason_code, properties):

    print("Device Simulator connected to MQTT")

    client.subscribe(TOPIC)

    print("Subscribed:", TOPIC)


def on_message(client, userdata, msg):

    command = msg.payload.decode()

    print("\nMQTT MESSAGE RECEIVED")
    print("Topic:", msg.topic)
    print("Command:", command)

    save_event(
        "ESP32_01",
        command,
        "received"
    )

    print("Event saved to database")


init_db()

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)

client.loop_forever()