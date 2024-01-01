import smbus2
import time


class LightMeter:
    def __init__(self):
        self.bus = smbus2.SMBus(1)
        time.sleep(0.5)

    def measure(self):
        I2C_ADDRESS = 0x23
        self.bus.write_byte(I2C_ADDRESS, 0x10)
        time.sleep(0.5)
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x00, 2)
        result = int.from_bytes(data, byteorder="big") / 1.2
        print(f"Light measurement: {result}")
        return result

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.bus.close()
