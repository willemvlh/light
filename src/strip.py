from rpi_ws281x import PixelStrip, Color
import time

def interpolate_color(color1, color2, fraction):
    """
    Interpolate between two RGB colors.

    :param color1: A tuple (R, G, B) representing the first color.
    :param color2: A tuple (R, G, B) representing the second color.
    :param fraction: A float between 0 and 1 indicating the progress of the interpolation.
    :return: A tuple (R, G, B) representing the interpolated color.
    """
    if not (0 <= fraction <= 1):
        raise ValueError("Fraction must be between 0 and 1")

    r1, g1, b1 = color1
    r2, g2, b2 = color2

    # Calculate the intermediate color
    interpolated_color = (
        int(r1 + (r2 - r1) * fraction),
        int(g1 + (g2 - g1) * fraction),
        int(b1 + (b2 - b1) * fraction)
    )

    return interpolated_color


class Strip:
    def __init__(self, number_of_leds, pin_out, logger=None) -> None:
        self._number_of_leds = number_of_leds
        self.current_color = None
        self._strip = PixelStrip(number_of_leds, pin_out)
        self._strip.begin()
        self._logger = logger if logger else lambda x: None
        self._logger(
            f"Initializing with {number_of_leds} number of leds, pin_out = {pin_out}")

    def fill(self,rgb):
        if self.current_color:
            for x in range(21):
                intermediate = interpolate_color(self.current_color, rgb, x /
                        20) 
                self.fill_direct(intermediate)
                time.sleep(0.05)
            self.current_color = rgb
        else:
            self.fill_direct(rgb)
            self.current_color = rgb

    def fill_direct(self, rgb):
        color = Color(*rgb)
        for x in range(self._number_of_leds):
            self._strip.setPixelColor(x, color)
            self._strip.show()
        self.current_color = rgb

    def clear(self):
        self.fill_direct((0, 0, 0))
