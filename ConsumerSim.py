import itertools
import random

import simpy

TOTAL_BATTERY_CAPACITY = 5000  # In kwh
HOUR_AVERAGE_ENERGY_USAGE = 187  # kwh
HOUSEHOLDS_SIMULATED = 1  # Number of Houses used in simulation
SIM_TIME = 24  # Simulation time in Hours


def central_controller(env, battery, consumer_energy_container):
    while (True):
        print(f"Daily hour: {env.now}, with Energy Consumption of: {consumer_energy_container.level} kwh, with total battery capacity: {battery_container.level}")
        env.process(consumer(env, battery, consumer_energy_container))
        yield env.timeout(1)  # Standby 1 hour until next checkpoint


def battery(env, consumption): #,solarPnael, windTurbine):
    solarEnergy = random.randint(150, 200)    # Random energy generation at the moment.
    battery_container.put(solarEnergy)
    yield battery_container.get(consumption)
    # consumer_energy_container.capacity = battery_container.level  # Change grid capacity


def consumer(env, battery, consumer_energy_container):
    env.process(battery(env, HOUR_AVERAGE_ENERGY_USAGE))
    yield consumer_energy_container.put(HOUR_AVERAGE_ENERGY_USAGE)


# Setup and start the simulation
print('House')

# Create environment and start processes
env = simpy.Environment()

battery_container = simpy.Container(env, TOTAL_BATTERY_CAPACITY, init=2500)
consumer_energy_container = simpy.Container(env, 50000, init=0)

env.process(central_controller(env, battery, consumer_energy_container))

# Execute!
env.run(until=SIM_TIME)
