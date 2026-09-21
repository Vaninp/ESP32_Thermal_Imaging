from sensors.solar_voltage import SolarVoltageSensor
from utils.calibration import SOLAR_SLOPE, SOLAR_OFFSET
import time

solar = SolarVoltageSensor(
    slope=SOLAR_SLOPE,
    offset=SOLAR_OFFSET
)

while True:
    raw, voltage = solar.read_voltage()

    print("====================================")
    print("SOLAR PANEL")
    print("Raw ADC (avg)     :", round(raw, 1))
    print("Solar Voltage     :", round(voltage, 2), "V")
    print("====================================")

    time.sleep(1)
