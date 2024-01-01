from strip import LedState

class LuminanceProvider:
    def __init__(self) -> None:
        self.lightness = 0.2
        self.delta = 0.02
        self.counter = 0

    def change_direction(self):
        self.delta *= -1
    
    def get_lightness(self, led: LedState):
        self.counter += 1
        if self.counter == 30:
            self.counter = 0
            self.lightness += self.delta
            if self.lightness <= 0.2 or self.lightness >= 0.75:
                self.change_direction()
            if not 0 <= self.lightness <= 1:
                raise ValueError(self.lightness)
        return self.lightness


