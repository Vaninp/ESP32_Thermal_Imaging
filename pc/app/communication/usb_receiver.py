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

        while True:
            start = self.text_buffer.find(b'SOLAR,')
            if start < 0:
                self.text_buffer = self.text_buffer[-6:]
                return

            end = self.text_buffer.find(b'\n', start)
            if end < 0:
                self.text_buffer = self.text_buffer[start:][-128:]
                return

            line = self.text_buffer[start:end].decode('ascii', errors='ignore')
            self.text_buffer = self.text_buffer[end + 1:]

            parts = line.strip().split(',')
            if len(parts) != 3 or parts[0] != 'SOLAR':
                continue

            try:
                self._solar_raw = float(parts[1])
                self._solar_voltage = float(parts[2])
            except ValueError:
                continue

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
        return frames[-1:] if frames else []
