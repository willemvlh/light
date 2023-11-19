import time
from rpi_ws281x import Color
from weather import temp_to_color, Weather, get_weather
from strip import Strip, lighten 

weather_time = time.time()
weather = get_weather()

if __name__ == "__main__":
    strip = Strip(30,18)
    while True:
        if weather == None or time.time() - weather_time > 1000:
            weather_time = time.time()
            weather = get_weather()
        color = temp_to_color(weather.temp)
        color2 = lighten((color.r,color.g,color.b), 0.5)
        strip.fill(color)
        time.sleep(10)
        strip.fill(Color(*color2))
        time.sleep(10)
