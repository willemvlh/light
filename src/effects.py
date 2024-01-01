from strip import Strip
from color import Color
import random
import time

class Effects:
    def __init__(self, strip: Strip) -> None:
        self.strip = strip

    @property
    def leds(self):
        return self.strip.leds
    
    @property
    def number_of_leds(self):
        return self.strip.number_of_leds

    def show(self):
        self.strip.show()

    def clear(self):
        self.strip.clear()

    def pulse(self, color, period=1, count=10):
        dark = Color(color)
        dark.set_luminance(0.02)
        for _ in range(count):
            self.strip.fill(color, speed_in_seconds=period / 2)
            self.strip.fill(dark, speed_in_seconds=period / 2)
    
    def gradient(self, color1, color2, speed_in_seconds=1.0):
        color_range = list(color1.range_to(color2, self.strip.number_of_leds))
        self.strip.fill_leds(color_range, speed_in_seconds, steps=30)

    def carousel(self, color, speed_in_seconds=1.0, reverse=False):
        self.strip.clear()
        for led in reversed(self.leds) if reverse else self.leds:
            self.strip.fill_direct(Color("black"))  # reset everything
            led.color = color
            self.show()
            time.sleep(speed_in_seconds / self.number_of_leds)
        self.clear()
        return

    def wheel(
        self,
        iterations=1,
        lightness_func = lambda _: 0.5,
        saturation_func = lambda _ : 1,
        reverse=False
    ):
        direction = -1 if reverse else 1
        for _ in range(iterations):
            for shift in range(self.number_of_leds):
                hsls = [
                        (
                    0.3 / len(self.leds) * ((led.index + shift * direction) % len(self.leds)),
                    saturation_func(led),
                    lightness_func(led))
                    for led in self.leds
                ]
                colors = [Color(hsl=hsl) for hsl in hsls] 
                self.strip.fill_leds(
                    colors,
                    speed_in_seconds=0.01,
                    steps=70,
                )

    def converge(self, color, speed_in_seconds=1.0):
        self.clear()
        for x in range(int(self.number_of_leds / 2)):
            self.strip.set_led(x, color)
            self.strip.set_led(self.number_of_leds - 1 - x, color)
            self.show()
            time.sleep(speed_in_seconds / self.number_of_leds)
    
    def fireflies(self, color, duration_in_seconds=15.0):
        end = time.time() + duration_in_seconds
        active_leds = []
        seen_colors = []
        colors = [Color(hsl=(x / 255, 0.8, 0.65)) for x in range(255) if x % 25 == 0]
        while time.time() < end:
            if len(seen_colors) == len(colors):
                seen_colors = []
            actual_color = random.choice([x for x in colors if x not in seen_colors])
            seen_colors.append(actual_color)
            led2 = random.choice([led for led in self.leds if led not in active_leds])
            active_leds.append(led2)
            self.strip.fill(actual_color, leds=[led2], speed_in_seconds=0.2)
            time.sleep(0.2)
            if len(active_leds) > 2:
                self.strip.fill("black", leds=[active_leds.pop(0)], speed_in_seconds=0.2)
