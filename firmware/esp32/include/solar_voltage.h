#pragma once

#include <Arduino.h>

struct SolarVoltageReading {
    float rawAdc = 0.0f;
    float voltage = 0.0f;
};

class SolarVoltageSensor
{
public:
    void begin();
    SolarVoltageReading read();

private:
    bool initialized = false;
};
