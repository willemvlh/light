from dataclasses import dataclass
from rpi_ws281x import Color
import requests
from time import time
import os

API_KEY = os.environ["OPENWEATHERMAP_KEY"]
CITY = "Leuven"


@dataclass
class Weather:
    def __init__(self, temp: int, secs_til_sunset: int) -> None:
        self.temp = temp
        self.secs_til_sunset = secs_til_sunset

def _temp_to_color(self, temp: int) -> Color:
    if temp < -10:
        return Color(144, 0, 255)
    if temp < -5:
        return Color(72, 0, 255)
    if temp <= 0:
        return Color(0, 79, 255)
    if temp < 7:
        return Color(0, 195, 255)
    if temp < 12:
        return Color(66, 255, 98)
    if temp < 16:
        return Color(220, 234, 0)
    if temp < 22:
        return Color(255, 200, 0)
    if temp < 27:
        return Color(255, 128, 0)
    return Color(255, 51, 0)


def get_weather() -> Weather:
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API_KEY}")
    result = r.json()
    temp = result["main"]["temp"]
    sunset = result["sys"]["sunset"]
    secs_til_sunset = max(0, sunset - time())
    return Weather(temp, secs_til_sunset)
