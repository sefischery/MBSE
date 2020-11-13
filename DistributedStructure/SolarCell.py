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

        # Record total power produced by solar cell
        self.totalProduces = 0

        # Keep the efficiency of the individuel solar cell constant
        self.efficiency = random.uniform(0.175, 0.225)

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.id)

    def power(self, datetime):
        power_generated =  self.log.get_solar_rad(datetime) * self.efficiency * self.squaremeters
        self.totalProduces += power_generated
        return power_generated
