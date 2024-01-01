from dataclasses import dataclass
from color import Color
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


def temp_to_color(temp) -> Color:
    if temp < -10:
        return Color("#b700ff")
    if temp < -5:
        return Color("#5d00ff")
    if temp <= 0:
        return Color("#3c00ff")
    if temp < 7:
        return Color("#0048ff")
    if temp < 12:
        return Color("#00aeff")
    if temp < 16:
        return Color("#55ff00")
    if temp < 22:
        return Color("#f2ff00")
    if temp < 27:
        return Color("#ffa200")
    return Color("#ff3700")


def get_weather() -> Weather:
    r = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API_KEY}"
    )
    result = r.json()
    temp = result["main"]["temp"]
    sunset = result["sys"]["sunset"]
    secs_til_sunset = max(0, sunset - time())
    return Weather(temp, secs_til_sunset)
