#import RPi.GPIO as GPIO
from strip import Strip
import time

strip = Strip(30,18)
while True:
    strip.fill((33,155,255))
    time.sleep(1)
    strip.fill((68,87,102))
    time.sleep(1)
