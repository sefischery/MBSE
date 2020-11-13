import datetime
import pytz
import random
import simpy
import json
import os

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
    city.set_battery(cityBatteryContainer)

# Execute!
env.run(until=SIM_TIME)

# Printer functionality
for city in VirtualPowerGrid.cities:
    print()
    print(
        f"City: {city.cityNumber}, number of consumers in city: {len(city.consumerList)}, city battery level: {city.battery.level}, battery max capacity: {city.battery.capacity}")
    cityConsumption = 0
    for consumer in city.consumerList:
        cityConsumption += consumer.consumedEnergyTotal
        print(f"    Consumertype: {consumer.type}, total energy consumed "
              f"{consumer.consumedEnergyTotal}, total energy generated: {consumer.generatedEnergyTotal}, "
              f"total energy used from battery: {consumer.cityBatteryUsage}")
    print(f"total city energy consumption: {cityConsumption}")
    print()
print(f"Total windturbine energy generate: {VirtualPowerGrid.totalEnergyGenerated}")

output = json.dumps({
    "cities": list(map(lambda x: x.getResults(),VirtualPowerGrid.cities)),
    "sim_time": SIM_TIME,
    "wind_turbine_generation_history": WindTurbineEnergyGeneration
})
#print (output)

if os.path.exists("../plots/output.json"):
    os.remove("../plots/output.json")
f = open("plots/output.json", "a")
f.write(output)
f.close()