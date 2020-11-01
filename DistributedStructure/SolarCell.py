import random
from pathlib import Path
from weather import weather_history

base_path = Path(__file__).parent
file_path = (base_path / "../weather_copenhagen.csv").resolve()


# SOLAR CELL
class SolarCell(object):
    SOLAR_OUTPUT_PER_SECOND = 137

    def __init__(self):
        self.log = weather_history.WeatherLog(file_path)
        self.squaremeters = 0

    def setSquaremeterSize(self, size):
        self.squaremeters = size

    def power(self, datetime):
        return self.log.get_solar_rad(datetime) * random.uniform(0.175, 0.225) * self.squaremeters
