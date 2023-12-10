import time
import random
from colour import Color
from weather import temp_to_color, Weather, get_weather
from strip import Strip  
from light_meter import LightMeter
from datetime import datetime
import traceback
import os

weather_time = time.time()
weather = get_weather()
light_meter = LightMeter()

def should_show():
    if os.environ.get('TESTING_LIGHTS'):
        return True
    if light_meter.measure() > 30:
        return False
    current_date = datetime.now()
    if 0 <= current_date.hour <= 6:
        return False
    if 9 <= current_date.hour <= 16 and not is_weekend():
        return False
    return True

def is_weekend():
    return datetime.today().weekday() in [5,6]

def rand_color(strip):
    return strip.wheel(pos=random.randrange(1,256))

if __name__ == "__main__":
    strip = Strip(30,18)
    is_paused = False
    try:
        while True:
            if not should_show():
                if not is_paused:
                    is_paused = True
                    strip.clear()
                    strip.fill(Color("black"), speed_in_seconds=0)
                time.sleep(10)
                continue
            elif weather == None or time.time() - weather_time > 1000:
                weather_time = time.time()
                weather = get_weather()
            color: Color = temp_to_color(weather.temp)
            strip.fill(color, speed_in_seconds=6)
            strip.fill(rand_color(strip), speed_in_seconds=9)
            color = rand_color(strip)
            strip.carousel(color=color)
            strip.carousel(color=color, reverse=True)
            strip.converge(color=color)
            time.sleep(10)
            if random.random() > 0.9:
               strip.rainbow_cycle(wait_ms=100, iterations=10)
    except Exception as e:
        print(e)
        traceback.print_exc()
        strip.fill(Color("red"))


