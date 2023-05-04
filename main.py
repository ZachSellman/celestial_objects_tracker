"""Python app to track multiple "heavenly bodies" such as planets, the ISS, etc. and alert user when they are visible from their location."""

import requests
import sys
from obj_class import Object

MY_LAT = 44.97
MY_LONG = -93.26


def main():
    # weather = check_weather()
    # if weather is False:
    #     fail(0)

    # daylight = check_daylight()
    # if daylight is True:
    #     fail(1)

    locations = check_locations()
    visible_objects = check_visibility(locations)

    notify(visible_objects)


def notify(obj_list):
    """Will eventually notify user via text of visible objects, for now just prints them"""
    print(obj_list)


def check_locations():
    """Sends get requests to the API's to get current locations of various heavenly bodies"""
    locations = {}
    locations["ISS"] = get_iss()
    return locations


def get_iss():
    """gets current location of ISS"""
    response = requests.get(url="http://api.open-notify.org/iss-now.json", timeout=0.1)
    response.raise_for_status()
    data = response.json()

    iss_lat, iss_long = (
        data["iss_position"]["latitude"],
        data["iss_position"]["longitude"],
    )
    return iss_lat, iss_long


def check_weather():
    """Checks weather conditions at current location to determine visibility"""
    return True


def check_daylight():
    """Checks whether it is currently dark enough to visibly see heavenly bodies"""
    return False


def check_visibility(obj_dict):
    "Checks the visibility of objects by comparing to user's MY_LAT and MY_LONG coordinates"
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
        print("Exit status 0: Weather not permitting")
    if _x == 1:
        print("Exit status 1: currently dayligh")
    sys.exit()


if __name__ == "__main__":
    main()
