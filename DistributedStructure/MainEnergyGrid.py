import datetime
import random
import simpy

from DistributedStructure.City import City
from DistributedStructure.Consumer import Consumer, select_random_consumer_type, select_random_resource_type
from DistributedStructure.WindTurbine import WindTurbine


SIM_TIME = 24
NUMB_OF_CITIES = 10
NUMB_OF_WINDTURBINES = 10

WING_SIZE = [20, 80]


class EnergyGrid(object):
    def __init__(self, env):
        self.env = env

        # Dynamic Variables
        self.cities = []
        self.resources = []
        self.resourceGeneratedEnergy = 0
        self.totalEnergyGenerated = 0

        # Start Grid processes
        env.process(self.get_generated_energy())
        env.process(self.distribute_generated_energy())
        env.process(self.overwatch_cities())

    def set_cities(self, cities):
        self.cities = cities

    def set_resources(self, resources):
        self.resources = resources

    def overwatch_cities(self):
        while True:
            criticalCities = []
            supportiveCities = []
            for city in self.cities:
                if city.battery.level / city.battery.capacity < 0.1: # less than 10 % of battery's capacity, then it's a critical city
                    criticalCities.append(city) # Critical cities
                elif city.battery.level / city.battery.capacity > 0.20: # if city has 20% or more of battery's capacity then it's a supportivecity.
                    supportiveCities.append(city) # Balanced city energy level
            if len(criticalCities) > 0 and len(supportiveCities) > 0:
                env.process(self.perform_city_energy_distribution(criticalCities, supportiveCities))
            yield self.env.timeout(1)

    def perform_city_energy_distribution(self, criticalCities, supportiveCities):
        for criticalCity in criticalCities:
            neededEnergy = ((criticalCity.battery.capacity * 0.15)-criticalCity.battery.level)
            for supportiveCity in supportiveCities:
                if neededEnergy > 0:
                    surPlusEnergy = (supportiveCity.battery.level-(supportiveCity.battery.capacity * 0.20))
                    if surPlusEnergy > 0:
                        if surPlusEnergy < neededEnergy:
                            neededEnergy -= surPlusEnergy
                            supportiveCity.battery.get(surPlusEnergy)
                            criticalCity.battery.put(surPlusEnergy)
                            print(f"City {supportiveCity.cityNumber}, sends energy level {surPlusEnergy}, to city {criticalCity.cityNumber}")
                        else:
                            supportiveCity.battery.get(neededEnergy)
                            criticalCity.battery.put(neededEnergy)
                            print(f"City {supportiveCity.cityNumber}, sends energy level {neededEnergy}, to city {criticalCity.cityNumber}")
                            neededEnergy -= neededEnergy

        yield self.env.timeout(1)

    def get_generated_energy(self):
        while True:
            self.resourceGeneratedEnergy = 0
            for resource in self.resources:
                self.resourceGeneratedEnergy += resource.power(datetime.datetime(2019, 1, 1, self.env.now))

            self.totalEnergyGenerated += self.resourceGeneratedEnergy
            yield self.env.timeout(1)

    def distribute_generated_energy(self):
        while True:
            energyLevelToDistribute = self.resourceGeneratedEnergy / len(self.cities)
            for city in self.cities:
                city.process_incoming_energy(energyLevelToDistribute)
            yield self.env.timeout(1)


# Setup
env = simpy.Environment()

# Initialize Virtual Power Plant Grid
VirtualPowerGrid = EnergyGrid(env)

# Initialize windtubines
Windturbines = [WindTurbine(random.randint(*WING_SIZE)) for _ in range(NUMB_OF_WINDTURBINES)]

# Initialize Cities
Cities = [City(env, i) for i in range(NUMB_OF_CITIES)]

# Sets for Virtual Power Plant Grid
VirtualPowerGrid.set_cities(Cities)
VirtualPowerGrid.set_resources(Windturbines)

# Add Consumers & Battery to Cities
for city in VirtualPowerGrid.cities:
    consumers = [Consumer(env, select_random_consumer_type(), i) for i in range(random.randint(10, 20))]
    for consumer in consumers:
        resource = select_random_resource_type()
        consumer.set_resource(resource)  # Set generation resource
        consumer.set_resource_size(random.randint(10, 80))  # set size of resource
        city.add_consumer(consumer)

    batteryCapacity = len(city.consumerList) * 5000
    cityBatteryContainer = simpy.Container(env, batteryCapacity, init=0.35 * batteryCapacity)
    city.add_battery(cityBatteryContainer)

# Execute!
env.run(until=SIM_TIME)

# Printer functionality
for city in VirtualPowerGrid.cities:
    print()
    print(
        f"City: {city.cityNumber}, number of consumers in city: {len(city.consumerList)}, city battery level: {city.battery.level}, battery max capacity: {city.battery.capacity}")
    cityConsumption = 0
    for consumer in city.consumerList:
        cityConsumption += consumer.consumedEnergy
        print(f"    Consumertype: {consumer.type}, total energy consumed "
              f"{consumer.consumedEnergy}, total energy generated: {consumer.generatedEnergy}, "
              f"total energy used from battery: {consumer.cityBatteryUsage}")
    print(f"total city energy consumption: {cityConsumption}")
    print()
print(f"Total windturbine energy generate: {VirtualPowerGrid.totalEnergyGenerated}")

# Plots
# Plot results
from matplotlib import pyplot as plt
import numpy as np

for consumer in VirtualPowerGrid.cities[0].consumerList:
    # Draw plot
    if len(consumer.consumerGeneratedEnergyGraphPoints) > 0:

        #fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
        #ax.fill_between(np.arange(0, SIM_TIME), y1=consumer.consumerGeneratedEnergyGraphPoints, y2=0, label="", alpha=0.5,
        #                color='tab:red', linewidth=2)

        plt.plot(np.arange(0, SIM_TIME), consumer.consumerGeneratedEnergyGraphPoints, color='tab:red')
        plt.xlabel("Hour of day")
        plt.ylabel("Energy usage")
plt.show()
