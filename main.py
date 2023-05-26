"""Python app to track multiple "Celestial Bodies" such as planets, the ISS, etc. and alert user when they are visible from their location."""

import requests
import sys
from os import getenv
from dotenv import load_dotenv
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

load_dotenv()

MY_LAT = 44.97
MY_LONG = -93.26
LOCATION = "Minneapolis"
WEATHER_API_KEY = getenv("WEATHER_API_KEY")
MY_TIMEZONE = "CST"
CURRENT_TIME = dt.time.now()


def main():
    cloud = check_weather()
    if cloud > 60:
        fail(0)

    dusk, dawn = check_darkness()
    if not CURRENT_TIME < dawn or not CURRENT_TIME > dusk:
        fail(1)

    objects = get_objects()


def get_objects():
    iss_status = get_iss()
    planets = get_planets()


def get_planets():
    "Will utilize selenium to scrape which planets should be visible at night"


def get_iss():
    """gets current location of ISS"""
    response = requests.get(url="http://api.open-notify.org/iss-now.json", timeout=1)
    response.raise_for_status()
    data = response.json()

    iss_lat, iss_long = (
        data["iss_position"]["latitude"],
        data["iss_position"]["longitude"],
    )

    if iss_lat in range((MY_LAT - 5), (MY_LAT + 5)) and iss_long in range(
        (MY_LONG - 5), (MY_LONG + 5)
    ):
        return True
    else:
        return False


def check_darkness():
    """Checks when it will be dusk"""
    today = f"{str(dt.now().year)}-{str(dt.now().month)}-{str(dt.now().day)}"
    params = {"lat": MY_LAT, "lng": MY_LONG, "date": today, "timezone": MY_TIMEZONE}
    response = requests.get(
        url="https://api.sunrisesunset.io/json",
        params=params,
        timeout=1,
    )

    dusk = response.json()["results"]["dusk"]
    dawn = response.json()["results"]["dawn"]
    return dusk, dawn


def check_weather():
    """Checks weather conditions at current location to determine visibility"""

    params = {"key": WEATHER_API_KEY, "q": LOCATION, "aqi": "no"}
    response = requests.get(
        url="http://api.weatherapi.com/v1/current.json?",
        params=params,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()["current"]["cloud"]


def check_field_of_view(obj_dict):
    "Checks the visibility of fast-moving objects by comparing to user's MY_LAT and MY_LONG coordinates"
    visible_objects = []
    for obj in obj_dict:
        obj_lat, obj_long = obj_dict[obj][0], obj_dict[obj][1]
        if (MY_LAT - 5) <= float(obj_lat) <= (MY_LAT + 5) and (MY_LONG - 5) <= float(
            obj_long
        ) <= (MY_LONG + 5):
            visible_objects.append(obj)

    return visible_objects


def fail(_x):
    """Exits program and provides reason such as 'Weather not permitting'."""
    if _x == 0:
        print("Exit status 0: Weather not permitting; too cloudy!")
    if _x == 1:
        print("Exit status 1: Not currently dark enough!")
    sys.exit()


if __name__ == "__main__":
    main()
