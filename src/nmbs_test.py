from color import Color
from nmbs import IRailClient

client = IRailClient()
delay = client.get_avg_delay()
assert delay >= 0
assert type(client.get_color()) == Color
print(delay)
print(client.get_color())
