from rpi_ws281x import PixelStrip, Color as PixelColor
from color import Color
import time
import random

def to_pixel_color(color: Color):
    r = int(color.red * 255)
    g = int(color.green * 255)
    b = int(color.blue * 255)
    return PixelColor(r,g,b,255)


class LedState:
    def __init__(self, index: int, color: Color, strip: PixelStrip) -> None:
        self.index = index
        self._color = color
        self._current_color = Color('black')
        self._strip = strip
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, new_color: Color):
        self._color = new_color

    def sync(self):
        if self._color == self._current_color:
            return
        self._strip.setPixelColor(self.index, to_pixel_color(self._color))
        self._current_color = self._color


class ColorRangeCache:
    def __init__(self) -> None:
        self.cache = {}
    
    def color_range(self, color1, color2, steps):
        if res := self.cache.get((color1,color2,steps)):
            return res
        if res := self.cache.get((color2,color1,steps)):
            return list(reversed(res))
        self.cache[(color1,color2,steps)] = list(color1.range_to(color2, steps))
        return self.cache[(color1, color2,steps)]


class Strip:
    def __init__(self, number_of_leds, pin_out, logger=None) -> None:
        self._strip = PixelStrip(number_of_leds, pin_out)
        self._strip.begin()
        self.leds = [LedState(n, Color("black"), self._strip) for n in range(number_of_leds)]
        self._logger = logger if logger else lambda _: None
        self._logger(
            f"Initializing with {number_of_leds} number of leds, pin_out = {pin_out}")
        self.color_range_cache = ColorRangeCache()
    @property
    def _number_of_leds(self):
        return len(self.leds)
    
    def _color_range(self, color1, color2, steps):
        return self.color_range_cache.color_range(color1, color2, steps)

    def fill(self,color, speed_in_seconds=1.0, steps=100,leds=None):
        which_leds = self.leds if leds is None else leds
        if color is None:
            raise ValueError("Color must not be None")
        if type(color) == str:
            color = Color(color)
        self.fill_leds(colors=[color for _ in range(len(which_leds))], which_leds=which_leds, speed_in_seconds=speed_in_seconds, steps=steps)
    
    def sync_leds(self):
        for led in self.leds:
            led.sync()

    def pulse(self, color, period=1, count=10):
        dark = Color(color)
        dark.set_luminance(0.02)
        for _ in range(count):
            self.fill(color, speed_in_seconds=period/2)
            self.fill(dark, speed_in_seconds=period/2)
 
    def fill_leds(self, colors, speed_in_seconds=1.0, steps=30, which_leds=None):
        leds = self.leds if which_leds is None else which_leds
        ranges_per_led = [list(self._color_range(led.color, colors[index], steps)) for index,led in enumerate(leds)]
        for step in range(steps):
            for index,led in enumerate(leds):
                led.color = ranges_per_led[index][step]
            self.show()
            time.sleep(speed_in_seconds / steps)    


    def gradient(self, color1, color2, speed_in_seconds=1.0):
        color_range = list(color1.range_to(color2, self._number_of_leds))
        self.fill_leds(color_range, speed_in_seconds, steps = 30)

    def carousel(self, color, speed_in_seconds=1.0, reverse=False):
        self.clear()
        for led in reversed(self.leds) if reverse else self.leds:
            self.fill_direct(Color("black")) #reset everything
            led.color = color
            self.show()
            time.sleep(speed_in_seconds / self._number_of_leds)
        self.clear()
        return

    def wheel(self, speed_in_seconds=10.0, iterations=1, start_lightness=0.5, end_lightness=0.5):
        for _ in range(iterations):  
            for shift in range(self._number_of_leds):
                hues = [1 / len(self.leds) * ((led.index + shift) % len(self.leds)) for led in self.leds]
                self.fill_leds([Color(hsl=(hue,1,0.5)) for hue in hues], speed_in_seconds=0.05, steps=50)

    def converge(self, color, speed_in_seconds=1.0):
        self.clear()
        for x in range(int(self._number_of_leds / 2)):
            self.set_led(x, color)
            self.set_led(self._number_of_leds - 1 - x, color)
            self.show()
            time.sleep(speed_in_seconds / self._number_of_leds)


    def fireflies(self, color, duration_in_seconds=15.0):
        end = time.time() + duration_in_seconds
        active_leds = []
        seen_colors = []
        colors = [Color(hsl=(x/255, 0.8, 0.65)) for x in range(255) if x % 25 == 0]
        while time.time() < end:
            if len(seen_colors) == len(colors):
                seen_colors = []
            actual_color = random.choice([x for x in colors if x not in seen_colors]) 
            seen_colors.append(actual_color)
            led2 = random.choice([led for led in self.leds if led not in active_leds])
            active_leds.append(led2)
            self.fill(actual_color, leds=[led2], speed_in_seconds=0.2)
            time.sleep(0.2)
            if len(active_leds) > 2:
                self.fill("black", leds=[active_leds.pop(0)], speed_in_seconds=0.2)

    def set_led(self, number, color):
        if(number > self._number_of_leds):
            raise ValueError("I don't have that many leds")
        self.leds[number].color = color
     
    def fill_direct(self, color):
        for led in self.leds:
            led.color = color
        self.show()

    def show(self):
        self.sync_leds()
        self._strip.show()

    def clear(self):
        self.fill_direct(Color("black")) 
