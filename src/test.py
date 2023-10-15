import RPi.GPIO as GPIO
from light_meter import LightMeter
from strip import Strip
import time

strip = Strip(30,18)
while True:
    strip.fill_fade((33,155,255))
    time.sleep(1)
    strip.fill_fade((68,87,102))
    time.sleep(1)
