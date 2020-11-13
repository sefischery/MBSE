import random
from pathlib import Path
from weather import weather_history

base_path = Path(__file__).parent
file_path = (base_path / "../weather_copenhagen.csv").resolve()


# SOLAR CELL
class SolarCell(object):
    
    def __init__(self, squaremeters_size):
        self.log = weather_history.WeatherLog(file_path)
        self.squaremeters = squaremeters_size
        self.online = True

    def power(self, datetime_utc):
        return self.log.get_solar_rad(weather_history.utc_to_danish_time(datetime_utc)) * random.uniform(0.175, 0.225) * self.squaremeters
