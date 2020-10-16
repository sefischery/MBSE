import itertools
import random

import simpy

RANDOM_SEED = 42
#GAS_STATION_SIZE = 200     # liters
#THRESHOLD = 10             # Threshold for calling the tank truck (in %)
#FUEL_TANK_SIZE = 50        # liters
#FUEL_TANK_LEVEL = [5, 25]  # Min/max levels of fuel tanks (in liters)
#REFUELING_SPEED = 2        # liters / second
#TANK_TRUCK_TIME = 300      # Seconds it takes the tank truck to arrive
#T_INTER = [30, 300]        # Create a car every [min, max] seconds
SIM_TIME = 1000            # Simulation time in seconds

class WindTurbine(object):
    p = 1.23
    A = 12470
    Cp = 1      # ??
    V = 14
    Ng = 1      # ??
    Nb = 1      # ??

    def __init__(self, V):
        self.V = V

    def power(self):
        return 0.5 * self.p * self.A * self.Cp * pow(self.V, 3) * self.Ng * self.Nb


# Simpy test...
random.seed(42)

wt1 = WindTurbine(14)
wt2 = WindTurbine(21)

print(wt1.power())
print(wt2.power())
