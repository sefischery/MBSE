from pathlib import Path
from weather import weather_history
import numpy as np

base_path = Path(__file__).parent
file_path = (base_path / "../weather/data/2019/weather_copenhagen.csv").resolve()


class WindTurbine(object):
    def __init__(self, wing_size):
        self.A = pow(wing_size, 2) * np.pi
        self.log = weather_history.WeatherLog(file_path)
        self.online = True

        # Total amount produced by this wind turbine
        self.totalProduced = 0

    # https://www.ajdesigner.com/phpwindpower/wind_generator_power_performance_coefficient.php
    # Info about the below variables and their typical values

    # Air density in kg/m3
    p = 1.23
    # Rotor swept area in m3:
    # A = wing_size * 2 * pow(numpy.pi, 2)
    # Coefficient of performance:
    # Typical value is 0.35. The theoretical max is 0.56.
    Cp = 0.35
    # Wind speed in m/s:
    # V = self.log.get_wind_speed(datetime)

    # Generator efficiency:
    # Typically between 50 and 80 %
    Ng = 0.65
    # Gear box bearing efficiency:
    # Typically 95 %
    Nb = 0.95

    def power(self, datetime_utc):
        power = 0.5 * self.p * self.A * self.Cp * pow(
            self.log.get_wind_speed(weather_history.utc_to_danish_time(datetime_utc)), 3) * self.Ng * self.Nb
        power = power / 10000
        self.totalProduced += power
        return power
