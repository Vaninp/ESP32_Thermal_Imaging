import re

import serial
from serial.tools import list_ports

from .frame_protocol import parse_binary_frames


class UsbReceiver:
    def __init__(self):
        self.serial = None
        self.buffer = b''
        self.text_buffer = b''
        self._solar_raw = None
        self._solar_voltage = None

    @staticmethod
    def ports():
        return [port.device for port in list_ports.comports()]

    def connect(self, port: str, baud: int = 921600):
        self.close()
        self.serial = serial.Serial(port, baudrate=baud, timeout=0)
        self.buffer = b''
        self.text_buffer = b''
        self._solar_raw = None
        self._solar_voltage = None

    def close(self):
        if self.serial:
            self.serial.close()
        self.serial = None
        self.text_buffer = b''

    def connected(self):
        return self.serial is not None and self.serial.is_open

    def _parse_solar_text(self, data: bytes):
        self.text_buffer += data

        if b'\n' not in self.text_buffer:
            # Keep the buffer bounded while waiting for a complete line.
            self.text_buffer = self.text_buffer[-4096:]
            return

        complete, self.text_buffer = self.text_buffer.rsplit(b'\n', 1)
        text = complete.decode('utf-8', errors='ignore')

        raw_match = re.findall(
            r'Raw ADC \(avg\)\s*:\s*([-+]?\d+(?:\.\d+)?)',
            text,
        )
        voltage_match = re.findall(
            r'Solar Voltage\s*:\s*([-+]?\d+(?:\.\d+)?)\s*V',
            text,
        )

        if raw_match:
            self._solar_raw = float(raw_match[-1])

        if voltage_match:
            self._solar_voltage = float(voltage_match[-1])

    def solar_data(self):
        if self._solar_raw is None and self._solar_voltage is None:
            return None

        return {
            'raw': self._solar_raw,
            'voltage': self._solar_voltage,
        }

    def poll(self):
        if not self.connected():
            return []

        waiting = self.serial.in_waiting
        if waiting:
            data = self.serial.read(waiting)
            self.buffer += data
            self._parse_solar_text(data)

        frames, self.buffer = parse_binary_frames(self.buffer)
        # Latest-frame-only keeps the UI live if the PC briefly falls behind.
        return frames[-1:] if frames else []
