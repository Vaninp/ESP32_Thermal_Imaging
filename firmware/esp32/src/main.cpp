#include <Arduino.h>

#include "camera.h"
#include "solar_voltage.h"
#include "system_config.h"
#include "usb_transport.h"
#include "wifi_transport.h"

namespace {

UsbTransport usbTransport;
WifiTransport wifiTransport;
SolarVoltageSensor solarVoltageSensor;
uint32_t lastSolarSend = 0;

} // namespace

void setup()
{
    usbTransport.begin();
    delay(500);

    solarVoltageSensor.begin();

    if (!camera.begin()) {
        Serial.println("[SYSTEM][FATAL] MLX90640 initialization failed.");
        while (true) {
            delay(1000);
        }
    }

    if (wifiTransport.begin()) {
        Serial.print("[WIFI] SSID: ");
        Serial.println(ThermalConfig::WIFI_AP_SSID);
        Serial.print("[WIFI] IP: ");
        Serial.println(WiFi.softAPIP());
        Serial.print("[WIFI] TCP port: ");
        Serial.println(ThermalConfig::WIFI_PORT);
    } else {
        Serial.println("[WIFI][WARN] Access point startup failed.");
    }
}

void loop()
{
    const uint32_t captureStart = micros();

    if (camera.update()) {
        const ThermalFrame &frame = camera.getFrame();

        // Keep both transports on the same raw binary thermal frame.
        usbTransport.sendFrame(frame);
        wifiTransport.sendFrame(frame);
    }

    // Send the solar reading once per second over the same USB serial
    // connection used by the thermal application.
    if (millis() - lastSolarSend >= 1000) {
        const SolarVoltageReading solar = solarVoltageSensor.read();

        Serial.printf(
            "SOLAR,%.1f,%.2f\n",
            solar.rawAdc,
            solar.voltage
        );

        lastSolarSend = millis();
    }

    (void)captureStart;
}
