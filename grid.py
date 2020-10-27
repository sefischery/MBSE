import itertools
import random
# import importlib
# importlib.import_module("weather/weather_history.py")
from weather import weather_history
import datetime

import simpy

# GRID
MIN_THRESHOLD = 100
MAX_THRESHOLD = 1000
T_INTER = [30, 300]

GRID_START= 500
GRID_CAP = 10000
RANDOM_SEED = 42
SIM_TIME = 60 * 60 * 24		# Time in seconds

# SOLAR CELL
class SolarCell(object):
    SOLAR_OUTPUT_PER_SECOND = 137

    def __init__(self):
       self.log = weather_history.WeatherLog("weather_copenhagen.csv")
	
    def power(self, datetime):
        return self.log.get_solar_rad(datetime) *  0.2   #20% efficiency

# CONSUMER
class Consumer(object):
	DAILY_USAGE = 4488 # Wh
	
	HourProcentageMultiplier = [0.03303964757709271,0.022026431718061677,0.02026431718061674,0.022026431718061675,0.02026431718061674,0.03436123348017621,0.04229074889867841,0.04317180616740088,0.04140969162995595,0.04140969162995595,0.04140969162995595,0.04229074889867841,0.04185022026431718,0.03940969162995595,0.03752863436123348,0.04757709251101322,0.05418502202643172,0.06014977973568282,0.06411453744493392,0.06267400881057269,0.05991189427312775,0.051982378854625554,0.039647577092511016,0.03700440528634361]
	
	def power(self, hour_of_day):
		return self.DAILY_USAGE * self.HourProcentageMultiplier[hour_of_day]

# WIND TURBINE
class WindTurbine(object):
    WIND_SPEED = [1, 30]
	
    #https://www.ajdesigner.com/phpwindpower/wind_generator_power_performance_coefficient.php
    # Info about the below variables and their typical values

    # Air density in kg/m3
    p = 1.23
    # Rotor swept area in m3:
    A = 12470
    # Coefficient of performance:
    #Typical value is 0.35. The theoretical max is 0.56.
    Cp = 0.35
    # Wind speed in m/s:
    V = 14
    # Generator efficiency:
    # Typically between 50 and 80 %
    Ng = 0.65
    # Gear box bearing efficiency:
    # Typically 95 %
    Nb = 0.95

    def power(self):
        self.V = random.randint(*self.WIND_SPEED)
        power = 0.5 * self.p * self.A * self.Cp * pow(self.V, 3) * self.Ng * self.Nb
        return power / 100000


grid_levels = []
def grid_controller(env, grid):
	while True:
		grid_levels.append(grid.level)
		yield env.timeout(1)

consumer_consumption = []
def consumer(env, grid):
	consumer = Consumer()
	while True:
		hour_of_day = int(env.now / (60 * 60))
		power = consumer.power(hour_of_day)
		consumer_consumption.append(power)
		yield grid.get(power)
		yield env.timeout(1)

solar_production = []
def solar(env, grid):
	solar_cell = SolarCell()
	while True:
		power = solar_cell.power(datetime.datetime(2019, 1, 1, 11)) #TODO: Make date variable
		solar_production.append(power)
		yield grid.put(power)
		yield env.timeout(1)
		
wind_production = []
def wind(env, grid):
    windturbine = WindTurbine()
    while True:
        power = windturbine.power()
        wind_production.append(power)
        yield grid.put(power)
        yield env.timeout(1)

print("Grid startup")
random.seed(RANDOM_SEED)

env = simpy.Environment()
grid_res = simpy.Resource(env, 1000000)
grid = simpy.Container(env, GRID_CAP, init=GRID_START)
env.process(grid_controller(env, grid))
env.process(consumer(env, grid))
env.process(solar(env, grid))
env.process(wind(env, grid))

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
# ax.set_xticklabels(np.arange(0, 60 + 1)) #TODO fix
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







# Plot results
from matplotlib import pyplot as plt
import numpy as np

# Draw plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
ax.fill_between(np.arange(0, SIM_TIME), y1=consumer_consumption, y2=0, label="Grid levels", alpha=0.5, color='tab:red', linewidth=2)
plt.show()