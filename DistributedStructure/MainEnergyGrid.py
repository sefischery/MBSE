import datetime
import pytz
import random
import simpy

from DistributedStructure.City import City
from DistributedStructure.Consumer import Consumer, select_random_consumer_type, random_solar_cell
from DistributedStructure.WindTurbine import WindTurbine

from constants import *


WindTurbineEnergyGeneration = []


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
                if city.battery.level / city.battery.capacity < 0.1:  # less than 10 % of battery's capacity, then it's a critical city
                    criticalCities.append(city)  # Critical cities
                elif city.battery.level / city.battery.capacity > 0.20:  # if city has 20% or more of battery's capacity then it's a supportivecity.
                    supportiveCities.append(city)  # Balanced city energy level
            if len(criticalCities) > 0 and len(supportiveCities) > 0:
                env.process(self.perform_city_energy_distribution(criticalCities, supportiveCities))
            yield self.env.timeout(1)

    def perform_city_energy_distribution(self, criticalCities, supportiveCities):
        for criticalCity in criticalCities:
            neededEnergy = ((criticalCity.battery.capacity * 0.15) - criticalCity.battery.level)
            for supportiveCity in supportiveCities:
                if neededEnergy > 0:
                    surPlusEnergy = (supportiveCity.battery.level - (supportiveCity.battery.capacity * 0.20))
                    if surPlusEnergy > 0:
                        if surPlusEnergy < neededEnergy:
                            neededEnergy -= surPlusEnergy
                            supportiveCity.battery.get(surPlusEnergy)
                            criticalCity.battery.put(surPlusEnergy)
                            print(
                                f"City {supportiveCity.cityNumber}, sends energy level {surPlusEnergy}, to city {criticalCity.cityNumber}")
                        else:
                            supportiveCity.battery.get(neededEnergy)
                            criticalCity.battery.put(neededEnergy)
                            print(
                                f"City {supportiveCity.cityNumber}, sends energy level {neededEnergy}, to city {criticalCity.cityNumber}")
                            neededEnergy -= neededEnergy

        yield self.env.timeout(1)

    def get_generated_energy(self):
        date_utc = datetime.datetime(START_YEAR, START_MONTH, START_DAY, START_HOUR)

        while True:
            self.resourceGeneratedEnergy = 0

            for resource in self.resources:
                self.resourceGeneratedEnergy += resource.power(date_utc)

            self.totalEnergyGenerated += self.resourceGeneratedEnergy
            WindTurbineEnergyGeneration.append(self.resourceGeneratedEnergy)

            date_utc += datetime.timedelta(hours=1)
            yield self.env.timeout(1)

    def distribute_generated_energy(self):
        while True:
            if self.resourceGeneratedEnergy > 0:
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
        consumer.set_resource(random_solar_cell())  # Set generation resource
        city.add_consumer(consumer)

    batteryCapacity = len(city.consumerList) * 5000
    cityBatteryContainer = simpy.Container(env, batteryCapacity, init=batteryCapacity) #0.35 * batteryCapacity)
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
from matplotlib import pyplot as plt, patches as pa
import seaborn as sns
import numpy as np

sns.set_theme()

def pick_random_color():
    r = random.random()
    b = random.random()
    g = random.random()
    return r, g, b


plt.figure(figsize=(20, 10))
# Consumer energy generation plot
for city in VirtualPowerGrid.cities:
    plt1 = []
    for consumer in city.consumerList:
        # Draw plot
        if len(consumer.consumerGeneratedEnergyGraphPoints) > 0:
            plt1 = plt.plot(np.arange(0, SIM_TIME), consumer.consumerGeneratedEnergyGraphPoints,
                            color=pick_random_color())
            plt.xlabel("Hour of day")
            plt.ylabel("Consumer Generation")
    plt1[0].set_label(f"city {city.cityNumber}")
plt.legend()
plt.show()

plt.figure(figsize=(20, 10))
# Draw windturbine energy generation
plt.plot(np.arange(0, SIM_TIME), WindTurbineEnergyGeneration, color='tab:red', label='Wind Turbine')
plt.xlabel("Hour of day")
plt.ylabel("Windturbine Generation")
plt.legend()
plt.show()

plt.figure(figsize=(20, 10))
# Cities Bar plot
for city in VirtualPowerGrid.cities:
    cityEnergyGeneration = 0
    cityEnergyConsumption = 0
    for consumer in city.consumerList:
        cityEnergyConsumption += np.sum(consumer.consumerConsumptionEnergyGraphPoints)
        cityEnergyGeneration += np.sum(consumer.consumerGeneratedEnergyGraphPoints)
    plt.bar(city.cityNumber, cityEnergyConsumption, 0.8, color='r', alpha=0.3)
    plt.bar(city.cityNumber, cityEnergyGeneration, 0.8, color='g', alpha=0.4)
plt.xlabel("Cities")
plt.ylabel("Energy Level")
redLabel = pa.Patch(color='r', label='Energy consumption')
greenLabel = pa.Patch(color='g', label='Energy Generation')
plt.legend(handles=[redLabel, greenLabel])
plt.show()
