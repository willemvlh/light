import RPi.GPIO as GPIO
from light_meter import LightMeter
import time

with LightMeter() as meter:
  with open("log.txt", "w") as f:
    while True:
      lux = meter.measure()
      t = time.strftime("%H:%M")
      f.write(f"{t} - {lux}")
      print(f"{t} - {lux}")
      time.sleep(3)
