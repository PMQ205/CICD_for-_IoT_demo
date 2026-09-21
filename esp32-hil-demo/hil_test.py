import serial
import time

PORT = "COM3"
BAUDRATE = 115200

ser = serial.Serial(PORT, BAUDRATE, timeout=2)

time.sleep(2)

def test_temperature(temp, expected_fan):
    ser.reset_input_buffer()

    command = f"TEMP={temp}\n"
    print(f"Sending: {command.strip()}")

    ser.write(command.encode())

    lines = []

    start = time.time()

    while time.time() - start < 3:
        line = ser.readline().decode(errors="ignore").strip()

        if line:
            print("ESP32:", line)
            lines.append(line)

        if f"FAN={expected_fan}" in lines:
            break

    assert f"FAN={expected_fan}" in lines, (
        f"Expected FAN={expected_fan}, but received: {lines}"
    )

    print("PASS\n")


try:
    test_temperature(35, "ON")
    test_temperature(25, "OFF")

    print("==============================")
    print("HIL TEST PASSED")
    print("==============================")

finally:
    ser.close()