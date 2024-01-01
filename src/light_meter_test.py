from light_meter import LightMeter

lm = LightMeter()
print(lm.measure())
assert lm.measure() > 0
