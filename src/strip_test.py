from luminance import LuminanceProvider
from strip import  Strip 
from color import Color
import time
from effects import Effects


strip = Strip(30, 18)
while True:
    lightness_provider = LuminanceProvider()
    effects = Effects(strip)
    effects.wheel(lightness_func=lightness_provider.get_lightness) 
    effects.wheel(lightness_func=lightness_provider.get_lightness, reverse=True) 
    effects.carousel(color=(Color("pink")), speed_in_seconds=0.5)
    effects.carousel(color=(Color("aqua")), reverse=True, speed_in_seconds=0.5)
    effects.converge(color=Color("yellow"))
    time.sleep(2)
    effects.pulse(Color("green"))
    effects.gradient(Color("red"), Color("pink"))
    time.sleep(3)
    strip.clear()
    time.sleep(4)
