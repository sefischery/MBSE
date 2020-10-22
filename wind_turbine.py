import itertools
import random

import simpy

CONSUMER_LEVEL = [130, 144]
WIND_SPEED = [1, 30]
RANDOM_SEED = 42

T_INTER = [30, 300]

GRID_START= 500
GRID_CAP = 10000
SIM_TIME = 60 * 60     # Simulation time in seconds

class WindTurbine(object):
    # Air density in kg/m3
    p = 1.23
    # Rotor swept area in m3:
    A = 12470
    # Coefficient of performance:
    Cp = 1      # ??
    # Wind speed in m/s:
    V = 14
    # Generator efficiency:
    Ng = 1      # ??
    # Gear box bearing efficiency:
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

# How much energy is consumed
def consumer(env, grid):
    while True:
        power = random.randint(*CONSUMER_LEVEL)
        yield grid.get(power)
        yield env.timeout(1)

# How much energy does the wind turbine deliver to the grid
def wind(env, grid):
    while True:
        yield grid.put((WindTurbine(random.randint(*WIND_SPEED)).power()) / 100000)
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
import numpy as np

# Draw plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
ax.fill_between(np.arange(0, SIM_TIME), y1=grid_levels, y2=0, label="Power usage", alpha=0.5, color='tab:blue', linewidth=2)

# Decorations
ax.set_title('Simulation of Power Generated From Wind Turbines (Random Values)', fontsize=16)
ax.set(ylim=[0, 10000])
ax.set_xlabel(r'Time [minutes]')
ax.set_ylabel(r'Grid levels')
ax.legend(loc='best', fontsize=12)
plt.xticks(np.arange(0, SIM_TIME + 1, 60), fontsize=10, horizontalalignment='center')
ax.set_xticklabels(np.arange(0, 60 + 1))
plt.xlim(0, 3600)

# Draw tick lines
for y in np.arange(0, 10000, 1000):
    plt.hlines(y, xmin=0, xmax=len(np.arange(0, SIM_TIME)), colors='black', alpha=0.3, linestyles="--", lw=0.5)

# Ligten borders
plt.gca().spines["top"].set_alpha(0)
plt.gca().spines["bottom"].set_alpha(.3)
plt.gca().spines["right"].set_alpha(0)
plt.gca().spines["left"].set_alpha(.3)

# Show plot
fig.tight_layout()
plt.show()
#plt.savefig('<name>', papertype='a4', format='pdf')   (uncomment to save plot)


#ax.plot(grid_levels, label="Power usage")
#ax.axis([0, 3600, 0, 10000])
#ax.set_xticks(np.arange(0, SIM_TIME + 1, 60))
#ax.set_xticklabels(np.arange(0, 60 + 1))
#ax.set_xlabel(r'Time [minutes]')
#ax.set_ylabel(r'Grid levels')


#plt.plot(grid_levels, label="Grid levels")
#plt.xlabel("Time [minutes]")
#plt.ylabel("Grid levels")
#plt.xticks(np.arange(1, SIM_TIME + 1, 60), np.arange(1, 60 + 1))
#plt.legend()
#plt.show()