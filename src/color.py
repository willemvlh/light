from colour import Color as BaseColor


class Color(BaseColor):
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.get_rgb().__eq__(other.get_rgb())

    def __hash__(self):
        return hash(self.get_rgb())

    def range_to(self, value, steps):
        step_size = 1.0 / (steps - 1)
        for step in range(steps):
            t = step * step_size
            red = self.red + t * (value.red - self.red)
            green = self.green + t * (value.green - self.green)
            blue = self.blue + t * (value.blue - self.blue)
            yield Color(rgb=(red, green, blue))
