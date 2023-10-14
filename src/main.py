from light_meter import LightMeter
from strip import Strip
import time

meter = LightMeter()
strip = Strip(30, 18)
def loop():
  lux = meter.measure()
  blue = min(255, int(lux / 1000 * 255))
  if(lux < 100):
      strip.fill(255,blue,255,255)


if __name__ == '__main__':
    print("Starting program...")
    while True:
        loop()
        time.sleep(1)

