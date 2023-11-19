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

    r1, g1, b1 = color1.r, color1.g, color1.b
    r2, g2, b2 = color2.r, color2.g, color2.b

    # Calculate the intermediate color
    interpolated_color = (
        int(r1 + (r2 - r1) * fraction),
        int(g1 + (g2 - g1) * fraction),
        int(b1 + (b2 - b1) * fraction)
    )

    return Color(*interpolated_color, 255)

def lighten(rgb_tuple, factor):
    """
    Lightens the given RGB color tuple by the specified factor.

    Args:
    - rgb_tuple (tuple): A tuple containing three integers representing the RGB color values.
    - factor (float): The factor by which to lighten the color. Should be between 0 and 1.

    Returns:
    - tuple: The lightened RGB color tuple.
    """
    # Ensure the factor is within the valid range
    factor = max(0, min(1, factor))

    # Lighten each RGB component
    lightened_color = tuple(int(component + (255 - component) * factor) for component in rgb_tuple)

    return lightened_color


class Strip:
    def __init__(self, number_of_leds, pin_out, logger=None) -> None:
        self._number_of_leds = number_of_leds
        self.current_color = None
        self._strip = PixelStrip(number_of_leds, pin_out)
        self._strip.begin()
        self._logger = logger if logger else lambda x: None
        self._logger(
            f"Initializing with {number_of_leds} number of leds, pin_out = {pin_out}")

    def fill(self,color, speed_in_seconds=1.0):
        if color == self.current_color:
            return
        steps = 200 
        if self.current_color:
            for x in range(steps+1):
                intermediate = interpolate_color(self.current_color, color, x /
                        steps) 
                self._logger((intermediate.r,intermediate.g,intermediate.b))
                self.fill_direct(intermediate)
                time.sleep(speed_in_seconds / steps)
            self.current_color = color
        else:
            self.fill_direct(color)
            self.current_color = color

    def fill_direct(self, color):
        for x in range(self._number_of_leds):
            self._strip.setPixelColor(x, color)
            self._strip.show()
        self.current_color = color

    def fade_between(self, start_color, stop_color, speed=0.5):
        self.fill_direct(start_color)
        self.fill(stop_color, speed)
        time.sleep(1/speed)
        self.fill(start_color)
        time.sleep(1/speed)

    def clear(self):
        self.fill_direct((0, 0, 0))
