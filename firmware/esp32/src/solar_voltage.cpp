#include "solar_voltage.h"
#include "pins.h"

SolarVoltageReading SolarVoltageSensor::read()
{
    SolarVoltageReading result;

    if (!initialized) {
        return result;
    }

    uint32_t total = 0;

    for (uint8_t i = 0; i < SOLAR_VOLTAGE_SAMPLES; ++i) {
        total += analogRead(SOLAR_VOLTAGE_ADC_PIN);
        delay(5);
    }

    result.rawAdc =
        static_cast<float>(total) / static_cast<float>(SOLAR_VOLTAGE_SAMPLES);

    result.voltage =
        (result.rawAdc * SOLAR_VOLTAGE_SLOPE) + SOLAR_VOLTAGE_OFFSET;

    return result;
}

void SolarVoltageSensor::begin()
{
    analogReadResolution(12);
    analogSetPinAttenuation(SOLAR_VOLTAGE_ADC_PIN, ADC_11db);
    initialized = true;
}
