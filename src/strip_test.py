#import RPi.GPIO as GPIO
from strip import Strip, to_pixel_color
from color import Color
import time

strip = Strip(30,18)
while True:
    strip.wheel(iterations=2, speed_in_seconds=3, end_lightness=0.8)
    strip.carousel(color=(Color("pink")), speed_in_seconds=0.5)
    strip.carousel(color=(Color("aqua")), reverse=True, speed_in_seconds=0.5)
    strip.converge(color=Color("yellow"))
    time.sleep(2)
    strip.pulse(Color("green"))
    strip.gradient(Color("red"), Color("pink"))
    time.sleep(3)
    strip.clear()
    time.sleep(4)
