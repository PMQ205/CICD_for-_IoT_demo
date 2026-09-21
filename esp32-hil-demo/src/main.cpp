#include <Arduino.h>

void setup() {
    Serial.begin(115200);
    delay(1000);

    Serial.println("ESP32 HIL READY");
}

void loop() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command.startsWith("TEMP=")) {
            float temperature = command.substring(5).toFloat();

            Serial.print("TEMP=");
            Serial.println(temperature);

            if (temperature > 30) {
                Serial.println("FAN=ON");
            } else {
                Serial.println("FAN=OFF");
            }
        }
    }
}