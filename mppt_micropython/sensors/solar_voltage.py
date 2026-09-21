from machine import ADC, Pin
import time

from pins import SOLAR_VOLTAGE_ADC_PIN, SOLAR_VOLTAGE_SAMPLES


class SolarVoltageSensor:
    """Reads the solar-panel voltage through an ESP32 ADC input."""

    def __init__(self, slope, offset):
        self.adc = ADC(Pin(SOLAR_VOLTAGE_ADC_PIN))
        self.adc.atten(ADC.ATTN_11DB)
        self.slope = slope
        self.offset = offset

    def read_raw(self, samples=SOLAR_VOLTAGE_SAMPLES):
        """Read the ADC several times and return the average raw value."""
        total = 0
        for _ in range(samples):
            total += self.adc.read()
            time.sleep_ms(5)
        return total / samples

    def read_voltage(self):
        """Return (raw_adc_average, calibrated_voltage)."""
        raw_value = self.read_raw()
        voltage = (raw_value * self.slope) + self.offset
        return raw_value, voltage
