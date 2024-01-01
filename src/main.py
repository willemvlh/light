import time
import sys
import random
from am_i_home import am_i_home
from color import Color
from luminance import LuminanceProvider
from nmbs import IRailClient
from weather import temp_to_color, Weather, get_weather
from effects import Effects
from strip import Strip
from light_meter import LightMeter
from datetime import datetime
import traceback
import os

weather_time = time.time()
weather = get_weather()
light_meter = LightMeter()
nmbs_client = IRailClient()
luminance_provider = LuminanceProvider()

def should_show():
    if os.environ.get("TESTING_LIGHTS"):
        return True
    if light_meter.measure() > 30:
        return False
    current_date = datetime.now()
    if 0 <= current_date.hour <= 6:
        return False
    if 9 <= current_date.hour <= 16 and not is_weekend() and not am_i_home():
        return False
    return True


def is_weekend():
    return datetime.today().weekday() in [5, 6]


def rand_color():
    return Color(hsl=(random.randrange(1, 256) / 255, 0.8, 0.62))


use_weather = True


def get_weather_color():
    global weather, weather_time
    if time.time() - weather_time > 1000:
        weather_time = time.time()
        weather = get_weather()
    return temp_to_color(weather.temp)


def get_train_color():
    return nmbs_client.get_color()


def get_context_color():
    if use_weather:
        return get_weather_color()
    else:
        return get_train_color()


if __name__ == "__main__":
    strip = Strip(30,18)
    effects = Effects(strip)
    print("Start up")
    is_paused = False
    try:
        while True:
            if not should_show():
                if not is_paused:
                    is_paused = True
                    print("Going dark")
                    effects.clear()
                time.sleep(10)
                continue
            else:
                if is_paused:
                    print("Going light")
                    is_paused = False
            color = get_context_color()
            use_weather = not use_weather
            strip.fill(color, speed_in_seconds=3)
            time.sleep(2)
            strip.fill(rand_color(), speed_in_seconds=3)
            time.sleep(5)
            secondary_hue = color.get_hue() + (0.5 if color.get_hue() <= 0.5 else -0.5)
            secondary_color = Color(color)
            secondary_color.set_hue(secondary_hue)
            effects.gradient(color, Color("#ff5555"))
            time.sleep(3)
            effects.gradient(Color("#ff5555"), color)
            time.sleep(3)
            effects.wheel(iterations=3, lightness_func=luminance_provider.get_lightness)
            time.sleep(2)
    except Exception as e:
        print(e, file=sys.stderr)
        traceback.print_exc()
        effects.pulse(Color("red"))

