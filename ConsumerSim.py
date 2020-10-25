import itertools
import random

import simpy

TOTAL_BATTERY_CAPACITY = 5000  # In Watt
HOUR_AVERAGE_ENERGY_USAGE = 187  # Watt
DAILY_USAGE = 4488 # Watt
HOUSEHOLDS_SIMULATED = 1  # Number of Houses used in simulation
SIM_TIME = 24  # Simulation time in Hours

HourProcentageMultiplier = [0.03303964757709271,0.022026431718061677,0.02026431718061674,0.022026431718061675,0.02026431718061674,0.03436123348017621,0.04229074889867841,0.04317180616740088,0.04140969162995595,0.04140969162995595,0.04140969162995595,0.04229074889867841,0.04185022026431718,0.03940969162995595,0.03752863436123348,0.04757709251101322,0.05418502202643172,0.06014977973568282,0.06411453744493392,0.06267400881057269,0.05991189427312775,0.051982378854625554,0.039647577092511016,0.03700440528634361]

Hourly_energy_consumer_consumption = []

def central_controller(env, battery, consumer_energy_container):
    while (True):
        env.process(consumer(env, battery, consumer_energy_container))
        print(f"Daily hour: {env.now}, with Energy Consumption of: {consumer_energy_container.level} kwh, with total battery capacity: {battery_container.level}")
        yield env.timeout(1)  # Standby 1 hour until next checkpoint


def battery(env, consumption): #,solarPnael, windTurbine):
    solarEnergy = random.randint(150, 200)    # Random energy generation at the moment.
    battery_container.put(solarEnergy)
    yield battery_container.get(consumption)


def consumer(env, battery, consumer_energy_container):
    env.process(battery(env, HOUR_AVERAGE_ENERGY_USAGE))
    Hourly_energy_consumer_consumption.append(DAILY_USAGE * HourProcentageMultiplier[env.now])  # Only done to manage plot
    yield consumer_energy_container.put(DAILY_USAGE * HourProcentageMultiplier[env.now])


# Setup and start the simulation
print('House')

# Create environment and start processes
env = simpy.Environment()

battery_container = simpy.Container(env, TOTAL_BATTERY_CAPACITY, init=2500)
consumer_energy_container = simpy.Container(env, 50000, init=0)

env.process(central_controller(env, battery, consumer_energy_container))

# Execute!
env.run(until=SIM_TIME)


#############################################################################################

# Plot results
from matplotlib import pyplot as plt
import numpy as np

# Draw plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
ax.fill_between(np.arange(0, SIM_TIME), y1=Hourly_energy_consumer_consumption, y2=0, label="Grid levels", alpha=0.5, color='tab:red', linewidth=2)
plt.show()
