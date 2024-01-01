import requests
import sys

ENDPOINT = "http://192.168.0.126:3000"


def am_i_home():
    try:
        print("am I home?")
        return requests.get(ENDPOINT).json()["amIHome"] == True
    except Exception as e:
        print(e, file=sys.stderr)
        return False
