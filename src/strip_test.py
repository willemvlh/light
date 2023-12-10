#import RPi.GPIO as GPIO
from strip import Strip, to_pixel_color
from colour import Color
import time

strip = Strip(30,18)
print(to_pixel_color(Color("red")).r)
while True:
    strip.fill(Color("red"))
    time.sleep(1)
    strip.fill(Color("blue"))
    time.sleep(1)
