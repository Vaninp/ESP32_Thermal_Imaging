#pragma once

#include <Arduino.h>

// MLX90640 I2C connection
constexpr uint8_t CAMERA_SDA_PIN = 21;
constexpr uint8_t CAMERA_SCL_PIN = 22;
constexpr uint8_t CAMERA_I2C_ADDRESS = 0x33;

// DCT Electronics voltage sensor
// Sensor signal / divider output -> ESP32 GPIO32 (ADC1_CH4)
constexpr uint8_t SOLAR_VOLTAGE_ADC_PIN = 32;
constexpr uint8_t SOLAR_VOLTAGE_SAMPLES = 10;

// Solar voltage calibration from the existing MicroPython test
constexpr float SOLAR_VOLTAGE_SLOPE = 0.000854f;
constexpr float SOLAR_VOLTAGE_OFFSET = 0.079f;
