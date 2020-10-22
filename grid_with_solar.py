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
SIM_TIME = 60 * 60		# Time in seconds

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
import numpy as np

# Draw plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
ax.fill_between(np.arange(0, SIM_TIME), y1=grid_levels, y2=0, label="Grid levels", alpha=0.5, color='tab:red', linewidth=2)
plt.hlines(MAX_THRESHOLD, 0, SIM_TIME, label="Maximum levels", colors='black', linestyles='--')
plt.hlines(MIN_THRESHOLD, 0, SIM_TIME, label="Minimum levels", colors='black', linestyles='--')

# Decorations
ax.set_title('Simulation of Power Generated From Solar Panels (Random Values)', fontsize=16)
ax.set(ylim=[0, 2000])
ax.set_xlabel(r'Time [minutes]')
ax.set_ylabel(r'Grid levels')
ax.legend(loc='best', fontsize=12)
plt.xticks(np.arange(0, SIM_TIME + 1, 60), fontsize=10, horizontalalignment='center')
ax.set_xticklabels(np.arange(0, 60 + 1))
plt.xlim(0, 3600)

# Draw tick lines
for y in np.arange(0, 2000, 200):
    plt.hlines(y, xmin=0, xmax=len(np.arange(0, SIM_TIME)), colors='black', alpha=0.3, linestyles='--', lw=0.5)

# Ligten borders
plt.gca().spines["top"].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(.3)

# Show plot
fig.tight_layout()
plt.show()

# Plot results
#from matplotlib import pyplot as plt
#plt.plot(grid_levels, label="Grid levels")
plt.hlines(MAX_THRESHOLD, 0, SIM_TIME, label="Maximum levels")
plt.hlines(MIN_THRESHOLD, 0, SIM_TIME, label="Minimum levels")
#plt.xlabel("Time")
#plt.ylabel("Grid levels")
#plt.legend()
#plt.show()