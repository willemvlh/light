from light_meter import LightMeter
from strip import Strip
import weather
import time

meter = LightMeter()
strip = Strip(30, 18)
weather_time = None

def get_temp():
    global weather_time
    if not weather_time or (time.time() - weather_time > 1800):
        weather_time = time.time()
        return weather.get_weather().temp


def loop():
  lux = meter.measure()
  temp = get_temp()
  color = weather._temp_to_color(temp)
  
  if(lux < 100):
      strip.fill(color.r,color.g,color.b,0)


if __name__ == '__main__':
    print("Starting program...")
    while True:
        loop()
        time.sleep(1)

