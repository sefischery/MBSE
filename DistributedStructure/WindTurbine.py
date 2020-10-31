from weather import weather_history
import numpy as np


class WindTurbine(object):
    def __init__(self, wing_size):
        self.A = pow(wing_size, 2) * np.pi
        self.log = weather_history.WeatherLog("C:\\Users\\s164156\\Documents\\MBSE-master\\weather_copenhagen.csv")

    # https://www.ajdesigner.com/phpwindpower/wind_generator_power_performance_coefficient.php
    # Info about the below variables and their typical values

    # Air density in kg/m3
    p = 1.23
    # Rotor swept area in m3:
    #A = wing_size * 2 * pow(numpy.pi, 2)
    # Coefficient of performance:
    # Typical value is 0.35. The theoretical max is 0.56.
    Cp = 0.35
    # Wind speed in m/s:
    #V = self.log.get_wind_speed(datetime)

    # Generator efficiency:
    # Typically between 50 and 80 %
    Ng = 0.65
    # Gear box bearing efficiency:
    # Typically 95 %
    Nb = 0.95

    def power(self, datetime):
        power = 0.5 * self.p * self.A * self.Cp * pow(self.log.get_wind_speed(datetime), 3) * self.Ng * self.Nb
        return power / 10000