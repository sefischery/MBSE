import itertools
import random

import simpy

CONSUMER_LEVEL = [130, 144]
WIND_SPEED = [1, 30]
RANDOM_SEED = 42

T_INTER = [30, 300]

GRID_START= 500
GRID_CAP = 10000
SIM_TIME = 1440            # Simulation time in seconds

class WindTurbine(object):
    #Air density in kg/m3
    p = 1.23
    #Rotor swept area:
    A = 12470
    #Coefficient of performance:
    Cp = 1      # ??
    #Wind speed:
    V = 14
    #Generator efficiency:
    Ng = 1      # ??
    #Gear box bearing efficiency:
    Nb = 1      # ??

    def __init__(self, V):
        self.V = V

    def power(self):
        return 0.5 * self.p * self.A * self.Cp * pow(self.V, 3) * self.Ng * self.Nb

grid_levels = []

def grid_controller(env, grid):
    while True:
        grid_levels.append(grid.level)
        yield env.timeout(1)

#How much energy is consumed
def consumer(env, grid):
    while True:
        power = random.randint(*CONSUMER_LEVEL)
        yield grid.get(power)
        yield env.timeout(1)

#How much energy does the wind turbine deliver to the grid
def wind(env, grid):
    while True:
        yield grid.put((WindTurbine(random.randint(*WIND_SPEED)).power())/100000)
        yield env.timeout(1)

# Simpy test...
random.seed(RANDOM_SEED)

env = simpy.Environment()
grid_res = simpy.Resource(env, 100000)
grid = simpy.Container(env, GRID_CAP, init=GRID_START)
env.process(grid_controller(env, grid))
env.process(consumer(env, grid))
env.process(wind(env, grid))

env.run(until=SIM_TIME)

# Plot results
from matplotlib import pyplot as plt
plt.plot(grid_levels, label="Grid levels")
plt.xlabel("Time")
plt.ylabel("Grid levels")
plt.legend()
plt.show()

#wt1 = WindTurbine(14)
#wt2 = WindTurbine(21)

#print(wt1.power())
#print(wt2.power())
