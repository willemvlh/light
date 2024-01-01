import json
import time
from color import Color
import requests


class IRailClient:
    def __init__(self) -> None:
        self.cache = {}
        self.cache_ts = 0
        self.number_of_connections_to_check = 1
        self.endpoint = "https://api.irail.be/connections/?from=Leuven&to=Brussels-Central&format=json&timesel=departure"

    def get_data(self):
        if time.time() - self.cache_ts > 60:
            res = requests.get(self.endpoint)
            if res.ok:
                self.cache = res.json()
                self.cache_ts = time.time()
            else:
                print(f"Invalid response code: {res.status_code}\n{res.raw}")
                return None
        return self.cache

    def get_avg_delay(self) -> float:
        try:
            res = self.get_data()
            if not res:
                return -1
            if "connection" in res:
                connections = res["connection"]
                current_time = time.time()
                relevant_connections = [
                    conn
                    for conn in connections
                    if int(conn["departure"]["time"]) - current_time < 1800
                ]
                return avg(
                    [
                        int(conn["departure"]["delay"])
                        for conn in relevant_connections[
                            0 : self.number_of_connections_to_check
                        ]
                    ]
                )
            else:
                print(f"Invalid response: {json.dumps(res)}")
                return -1
        except Exception as e:
            print(e)
            return -1

    def get_color(self):
        delay = self.get_avg_delay()
        if delay == -1:  # something went wrong
            return Color("#cccccc")
        if delay < 90:
            return Color("green")
        if delay < 240:
            return Color("yellow")
        if delay < 400:
            return Color("orange")
        return Color("#ff4d4d")


def avg(coll) -> float:
    if not coll:
        return 0
    return sum(coll) / len(coll)
