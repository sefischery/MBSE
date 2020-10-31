import random

from weather import weather_history


# SOLAR CELL
class SolarCell(object):
    SOLAR_OUTPUT_PER_SECOND = 137

    def __init__(self, squaremeters):
        self.log = weather_history.WeatherLog("C:\\Users\\s164156\\Documents\\MBSE-master\\weather_copenhagen.csv")
        self.squaremeters = squaremeters

    def power(self, datetime):
        return self.log.get_solar_rad(datetime) * random.uniform(0.175, 0.225) * self.squaremeters
