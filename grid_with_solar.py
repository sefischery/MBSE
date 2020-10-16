import itertools
import random

import simpy

CONSUMER_LEVEL = [130, 144]

MIN_THRESHOLD = 100
MAX_THRESHOLD = 1000
T_INTER = [30, 300]

SOLAR_OUTPUT_PER_SECOND = 137
SOLAR_COUNT = 1

GRID_START= 500
GRID_CAP = 10000
RANDOM_SEED = 42
SIM_TIME = 1440

def consumer(env, grid):
	while True:
		power = random.randint(*CONSUMER_LEVEL)
		yield grid.get(power)
		yield env.timeout(1)
		
grid_levels = []

def grid_controller(env, grid):
	while True:
		grid_levels.append(grid.level)
		yield env.timeout(1)

def solar(env, grid):
	while True:
		yield grid.put(SOLAR_OUTPUT_PER_SECOND)
		yield env.timeout(1)

print("Grid startup")
random.seed(RANDOM_SEED)

env = simpy.Environment()
grid_res = simpy.Resource(env, 100000)
grid = simpy.Container(env, GRID_CAP, init=GRID_START)
env.process(grid_controller(env, grid))
env.process(consumer(env, grid))
env.process(solar(env, grid))

env.run(until=SIM_TIME)

# Plot results
from matplotlib import pyplot as plt
plt.plot(grid_levels, label="Grid levels")
plt.hlines(MAX_THRESHOLD, 0, SIM_TIME, label="Maximum levels")
plt.hlines(MIN_THRESHOLD, 0, SIM_TIME, label="Minimum levels")
plt.xlabel("Time")
plt.ylabel("Grid levels")
plt.legend()
plt.show()