from rpi_ws281x import PixelStrip, Color as PixelColor
from color import Color
import time


def to_pixel_color(color: Color):
    r = int(color.red * 255)
    g = int(color.green * 255)
    b = int(color.blue * 255)
    return PixelColor(r, g, b, 255)


class LedState:
    def __init__(self, index: int, color: Color, strip: PixelStrip) -> None:
        self.index = index
        self._color = color
        self._current_color = Color("black")
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
        if res := self.cache.get((color1, color2, steps)):
            return res
        if res := self.cache.get((color2, color1, steps)):
            return list(reversed(res))
        self.cache[(color1, color2, steps)] = list(color1.range_to(color2, steps))
        return self.cache[(color1, color2, steps)]


class Strip:
    def __init__(self, number_of_leds, pin_out, logger=None) -> None:
        self._strip = PixelStrip(number_of_leds, pin_out)
        self._strip.begin()
        self.leds = [
            LedState(n, Color("black"), self._strip) for n in range(number_of_leds)
        ]
        self._logger = logger if logger else lambda _: None
        self._logger(
            f"Initializing with {number_of_leds} number of leds, pin_out = {pin_out}"
        )
        self.color_range_cache = ColorRangeCache()

    @property
    def number_of_leds(self):
        return len(self.leds)

    def _color_range(self, color1, color2, steps):
        return self.color_range_cache.color_range(color1, color2, steps)

    def fill(self, color, speed_in_seconds=1.0, steps=100, leds=None):
        """
        Fill leds with a single color
        """
        which_leds = self.leds if leds is None else leds
        self.fill_leds(
            colors=[color] * len(which_leds),
            which_leds=which_leds,
            speed_in_seconds=speed_in_seconds,
            steps=steps,
        )

    def fill_leds(self, colors, speed_in_seconds=1.0, steps=30, which_leds=None):
        """
        Fill leds with colors. Colors must be the same as the number of leds
        """
        if None in colors:
            raise ValueError("Color must not be None")
        leds = self.leds if which_leds is None else which_leds
        if len(colors) != len(leds):
            raise ValueError("Colors and leds must have the same size")
        colors = [Color(color) for color in colors]
        ranges_per_led = [
            list(self._color_range(led.color, colors[index], steps))
            for index, led in enumerate(leds)
        ]
        for step in range(steps):
            for index, led in enumerate(leds):
                led.color = ranges_per_led[index][step]
            self.show()
            time.sleep(speed_in_seconds / steps)

    def sync_leds(self):
        for led in self.leds:
            led.sync()


    def set_led(self, number, color):
        if number > self.number_of_leds:
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
