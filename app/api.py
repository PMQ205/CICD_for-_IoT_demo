from fastapi import FastAPI
from pydantic import BaseModel
import paho.mqtt.client as mqtt

from app.database import init_db


app = FastAPI()

MQTT_BROKER = "localhost"
MQTT_PORT = 1883


class Command(BaseModel):
    device_id: str
    command: str


mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

mqtt_client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)

mqtt_client.loop_start()

init_db()


@app.get("/")
def home():
    return {
        "status": "IoT API is running"
    }


@app.post("/device/command")
def send_command(data: Command):

    topic = f"iot/device/{data.device_id}/command"

    result = mqtt_client.publish(
        topic,
        data.command
    )

    result.wait_for_publish()

    return {
        "status": "success",
        "device_id": data.device_id,
        "command": data.command,
        "mqtt_topic": topic
    }