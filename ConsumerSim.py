import itertools
import random
import numpy as np
import simpy

TOTAL_BATTERY_CAPACITY = 5000  # In Watt
HOUR_AVERAGE_ENERGY_USAGE = 187  # Watt
DAILY_USAGE = 4488  # Watt
HOUSEHOLDS_SIMULATED = 1  # Number of Houses used in simulation
SIM_TIME = 24  # Simulation time in Hours

RegularConsumerHourly = [0.03303964757709271, 0.022026431718061677, 0.02026431718061674, 0.022026431718061675,
                         0.02026431718061674, 0.03436123348017621, 0.04229074889867841, 0.04317180616740088,
                         0.04140969162995595, 0.04140969162995595, 0.04140969162995595, 0.04229074889867841,
                         0.04185022026431718, 0.03940969162995595, 0.03752863436123348, 0.04757709251101322,
                         0.05418502202643172, 0.06014977973568282, 0.06411453744493392, 0.06267400881057269,
                         0.05991189427312775, 0.051982378854625554, 0.039647577092511016, 0.03700440528634361]
NightConsumerHourly = RegularConsumerHourly[::-1]
HomeConsumerHourly = list(np.roll(RegularConsumerHourly, 3))
HighUsageConsumerHourly = [1.7 * x for x in RegularConsumerHourly]

listOfConsumers_dict = {
    "RegularConsumer": RegularConsumerHourly,
    "NightConsumer": NightConsumerHourly,
    "HomeConsumer": HomeConsumerHourly,
    "HighUsageConsumer": HighUsageConsumerHourly
}

listOfConsumers = [RegularConsumerHourly, NightConsumerHourly, HomeConsumerHourly, HighUsageConsumerHourly]

# Random værdi -0.0075 til 0.0075

Hourly_energy_consumer_consumption = []


def central_controller(env, battery, consumer_energy_container, consumerType):
    while (True):
        env.process(consumer(env, battery, consumer_energy_container, consumerType))
        print(
            f"Daily hour: {env.now}, with Energy Consumption of: {consumer_energy_container.level} kwh, with total "
            f"battery capacity: {battery_container.level}")
        yield env.timeout(1)  # Standby 1 hour until next checkpoint


# Regarding battery container, we assume that there is only one, in case we add more batteries to the system,
# this will simply change the one battery container capacity.
def battery(env, energy):
    if energy > 0:
        # Maybe check if battery container capacity is exceed, distribute to another "sub-grid" or sell the power.
        # This decision is up to the control unit.
        if energy + battery_container.level > battery_container.capacity:
            subEnergy = energy - (battery_container.capacity - battery_container.level)
            yield battery_container.put(subEnergy)
            print("Energy wasted: " + str(energy-subEnergy))
        else:
            yield battery_container.put(energy)

    elif energy < 0:
        if battery_container.level >= abs(energy):
            yield battery_container.get(abs(energy))


def consumer(env, battery, consumer_energy_container, consumerType):
    env.process(battery(env, HOUR_AVERAGE_ENERGY_USAGE))
    fluctuation = random.uniform(-0.0075, 0.0075)
    Hourly_energy_consumer_consumption.append(DAILY_USAGE * (consumerType[env.now] + fluctuation))
    yield consumer_energy_container.put(DAILY_USAGE * (consumerType[env.now] + fluctuation))


# Setup and start the simulation
# Create environment and start processes
env = simpy.Environment()

battery_container = simpy.Container(env, TOTAL_BATTERY_CAPACITY, init=0)
consumer_energy_container = simpy.Container(env, 50000, init=0)

consumerType = random.choice(list(listOfConsumers_dict.keys()))
print("Chosen consumer is: " + consumerType)

env.process(central_controller(env, battery, consumer_energy_container, listOfConsumers_dict.get(consumerType)))

# Execute!
env.run(until=SIM_TIME)

#############################################################################################

# Plot results
from matplotlib import pyplot as plt
import numpy as np

# Draw plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
ax.fill_between(np.arange(0, SIM_TIME), y1=Hourly_energy_consumer_consumption, y2=0, label="Grid levels", alpha=0.5,
                color='tab:red', linewidth=2)
plt.show()
