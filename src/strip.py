from rpi_ws281x import PixelStrip, Color as PixelColor
from colour import Color
import time

def to_pixel_color(color: Color):
    r = int(color.red * 255)
    g = int(color.green * 255)
    b = int(color.blue * 255)
    return PixelColor(r,g,b,255)

class Strip:
    def __init__(self, number_of_leds, pin_out, logger=None) -> None:
        self._number_of_leds = number_of_leds
        self.current_color = Color("black")
        self._strip = PixelStrip(number_of_leds, pin_out)
        self._strip.begin()
        self._logger = logger if logger else lambda x: None
        self._logger(
            f"Initializing with {number_of_leds} number of leds, pin_out = {pin_out}")

    def fill(self,color, speed_in_seconds=1.0):
        if color is None:
            raise ValueError("Color must not be None")
        if type(color) == str:
            color = Color(color)
        if color == self.current_color:
            return
        steps = 200 
        for x in self.current_color.range_to(color, steps):
            self.fill_direct(x)
            time.sleep(speed_in_seconds / steps)
        self.current_color = color

    def lighten(self, factor=0.5, speed_in_seconds=1.0):
        lightened = self.current_color.set_luminance(value=factor)
        self.fill(lightened, speed_in_seconds)
        
    def gradient(self, color1, color2):
        color_range = color1.range_to(color2, self._number_of_leds)
        for color, led_index in zip(color_range, range(self._number_of_leds)):
            self.set_led(led_index, color)
        self._strip.show()

    def carousel(self, color, speed_in_seconds=1.0, reverse=False):
        self.fill("black")
        for x in range(self._number_of_leds):
            led_index = self._number_of_leds - 1 - x if reverse else x 
            self.set_led(led_index, color)
            if x > 0:
                previous_led_index = led_index + (1 if reverse else -1)
                self.set_led(previous_led_index, Color("black"))
            self._strip.show()
            time.sleep(speed_in_seconds / self._number_of_leds)
        self.set_led(self._number_of_leds - 1, Color("black"))
        return

    def converge(self, color, speed_in_seconds=1.0):
        self.fill("black")
        for x in range(int(self._number_of_leds / 2)):
            self.set_led(x, color)
            self.set_led(self._number_of_leds - 1 - x, color)
            self._strip.show()
            time.sleep(speed_in_seconds / self._number_of_leds)

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        for j in range(256 * iterations):
            for i in range(self._strip.numPixels()):
                self.set_led(i, self.wheel((i + j) & 255))
            self._strip.show()
            time.sleep(wait_ms / 1000.0)

    def wheel(self, pos):
        if pos < 85:
            return Color(rgb=(pos * 3 / 255, (255 - pos * 3) / 255, 0))
        elif pos < 170:
            pos -= 85
            return Color(rgb=((255 - pos * 3) / 255, 0, (pos * 3) / 255))
        else:
            pos -= 170
            return Color(rgb=(0, (pos * 3) / 255, (255 - pos * 3) / 255))

    def set_led(self, number, color):
        if(number > self._number_of_leds):
            raise ValueError("I don't have that many leds")
        self._strip.setPixelColor(number, to_pixel_color(color))

        
    def fill_direct(self, color):
        for x in range(self._number_of_leds):
            self.set_led(x, color)
        self._strip.show()
        self.current_color = color

    def fade_between(self, start_color, stop_color, speed=0.5):
        self.fill_direct(start_color)
        self.fill(stop_color, speed)
        time.sleep(1/speed)
        self.fill(start_color)
        time.sleep(1/speed)

    def clear(self):
        self.fill_direct(Color("black")) 
