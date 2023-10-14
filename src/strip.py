from rpi_ws281x import PixelStrip, Color


class Strip:
    def __init__(self, number_of_leds, pin_out, logger=None) -> None:
        self._number_of_leds = number_of_leds
        self._strip = PixelStrip(number_of_leds, pin_out)
        self._strip.begin()
        self._logger = logger if logger else lambda x: None
        self._logger(
            f"Initializing with {number_of_leds} number of leds, pin_out = {pin_out}")

    def fill(self,r,g,b,a):
        color = Color(r,g,b,a)
        for x in range(self._number_of_leds):
            self._strip.setPixelColor(x, color)
            self._strip.show()

    def clear(self):
        self.fill(0, 0, 0, 0)
