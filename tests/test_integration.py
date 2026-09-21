import time
import requests

from app.database import get_latest_event


API_URL = "http://127.0.0.1:8000/device/command"


def test_iot_integration():

    device_id = "ESP32_01"
    command = "ON"

    # 1. Gửi lệnh qua API
    response = requests.post(
        API_URL,
        json={
            "device_id": device_id,
            "command": command
        }
    )

    # 2. Kiểm tra API
    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["device_id"] == device_id
    assert data["command"] == command

    # 3. Chờ Device Simulator xử lý MQTT
    event = None

    for _ in range(20):

        event = get_latest_event(device_id)

        if event:
            break

        time.sleep(0.5)

    # 4. Kiểm tra Database
    assert event is not None

    assert event[0] == device_id
    assert event[1] == "OFF"
    assert event[2] == "received"

    print("\n================================")
    print("INTEGRATION TEST PASSED")
    print("API -> MQTT -> DEVICE -> DB")
    print("================================")