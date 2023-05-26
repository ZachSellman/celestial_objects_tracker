"""Python app to track multiple "Celestial Bodies" such as planets, the ISS, etc. and alert user when they are visible from their location."""

from datetime import datetime as dt
from os import getenv
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import requests


load_dotenv()

MY_LAT = 44.97
MY_LONG = -93.26
LOCATION = getenv("LOCATION")
WEATHER_API_KEY = getenv("WEATHER_API_KEY")
MY_TIMEZONE = getenv("MY_TIMEZONE")
CURRENT_TIME = dt.now().strftime("%H:%M:%S")
SELENIUM_PATH = getenv("SELENIUM_PATH")


def main():
    cloud = check_weather()
    if cloud > 60:
        # fail(0)
        print("It's kinda cloudy")

    dusk, dawn = check_darkness()
    if not CURRENT_TIME < dawn or not CURRENT_TIME > dusk:
        # fail(1)
        print("It's currently too bright out!")

    objects = get_objects()
    print(f"These objects are currently visible: {objects}")


def get_objects():
    iss_status = get_iss()
    planets = get_planets()
    if iss_status is True:
        planets.append("International Space Station")

    return planets


def get_planets():
    service = Service(executable_path=SELENIUM_PATH)
    options = Options()
    web_url = "https://www.timeanddate.com/astronomy/night/"

    # comment this add_argument("--headless") to show browser window
    options.add_argument("--headless")
    options.add_argument("--disable-3d-apis")
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, service=service)
    driver.get(web_url)

    # via XPATH:
    planet_table = driver.find_element(
        by=By.XPATH,
        value="/html/body/div[5]/main/article/section[1]/div[2]/table/tbody",
    )

    planets_dict = {}

    for row in planet_table.find_elements(by=By.CSS_SELECTOR, value="tr"):
        planet = row.find_element(by=By.CSS_SELECTOR, value="th")
        time = row.find_element(by=By.CSS_SELECTOR, value="td")
        planets_dict[planet.text.strip().replace(":", "")] = time.text.strip()

    visible_planets = []
    for planet, time in planets_dict.items():
        hour = time[-8:-3].strip()

        # Need to add 12 to change format to 24 hr time for comparison
        if time[-2:] == "pm":
            hour = str(int(time[-8:-6].strip()) + 12) + time[-6:-3]

        if hour < CURRENT_TIME:
            visible_planets.append(planet)

    return visible_planets


def get_iss():
    """gets current location of ISS"""
    response = requests.get(url="http://api.open-notify.org/iss-now.json", timeout=1)
    response.raise_for_status()
    data = response.json()

    iss_lat, iss_long = (
        data["iss_position"]["latitude"],
        data["iss_position"]["longitude"],
    )

    return bool(MY_LAT - 5) < float(iss_lat) < (MY_LAT + 5) and (MY_LONG - 5) < float(
        iss_long
    ) < (MY_LONG + 5)


def check_darkness():
    """Checks when it will be dusk"""
    today = f"{str(dt.now().year)}-{str(dt.now().month)}-{str(dt.now().day)}"
    response = requests.get(
        url=f"https://api.sunrisesunset.io/json?lat={MY_LAT}&lng={MY_LONG}&date={today}&timezone={MY_TIMEZONE}",
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


# def check_field_of_view(obj_dict):
#     "Checks the visibility of fast-moving objects by comparing to user's MY_LAT and MY_LONG coordinates"
#     visible_objects = []
#     for obj in obj_dict:
#         obj_lat, obj_long = obj_dict[obj][0], obj_dict[obj][1]
#         if (MY_LAT - 5) <= float(obj_lat) <= (MY_LAT + 5) and (MY_LONG - 5) <= float(
#             obj_long
#         ) <= (MY_LONG + 5):
#             visible_objects.append(obj)

#     return visible_objects


def fail(_x):
    """Exits program and provides reason such as 'Weather not permitting'."""
    if _x == 0:
        print("Exit status 0: Weather not permitting; too cloudy!")
    if _x == 1:
        print("Exit status 1: Not currently dark enough!")
    sys.exit()


if __name__ == "__main__":
    main()
