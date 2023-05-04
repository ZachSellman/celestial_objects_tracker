"""Module for the Objects class utilized by heavenly_items_tracker application"""


class Object:
    """Simple class to hold data for heavenly_items_tracker application."""

    def __init__(self, name, lat, longitude):
        self.name = name
        self.lat = lat
        self.long = longitude
