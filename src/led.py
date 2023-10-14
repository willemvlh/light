from rpi_ws281x import PixelStrip, Color
import sys
import time
NUMBER_OF_LEDS = 30
PIN_OUT = 18

strip = PixelStrip(NUMBER_OF_LEDS, PIN_OUT)
strip.begin()

def fill(color):
  for x in range(30):
    strip.setPixelColor(x, color)
    strip.show()

def clear():
  fill(Color(0,0,0,0))

def parse_color(str):
  if len(str) != 6:
    raise ValueError
  else:
    num = int(str, 16)
    print(num)
    r = num >> 16
    g = num >> 8 & 0xff
    b = num & 0xff
    return Color(r,g,b,255)

def fade_in_out():
  alpha = 41
  direction = 1
  while True:
    if alpha in [40,255]:
      direction = direction * -1
    alpha += direction
    color = Color(alpha,alpha,alpha,alpha)
    fill(color)
    time.sleep(0.03)

try:
  color = parse_color(sys.argv[1]) if len(sys.argv) == 2 else Color(255,255,255,255)
  #fill(color)
  fade_in_out()
  while True:
    pass
except KeyboardInterrupt:
  clear()
  print("Goodbye!")
  sys.exit(0)
