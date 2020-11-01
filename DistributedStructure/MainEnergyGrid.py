import datetime
import random
import simpy

from DistributedStructure.City import City
from DistributedStructure.Consumer import Consumer, SelectRandomConsumerType, SelectRandomResourceType
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
        env.process(self.GetGeneratedEnergy())
        env.process(self.DistributeGeneratedEnergy())
        env.process(self.OverwatchCities())

    def SetCities(self, cities):
        self.cities = cities

    def SetResources(self, resources):
        self.resources = resources

    def OverwatchCities(self):
        while True:
            criticalCities = []
            supportiveCities = []
            for city in self.cities:
                if city.battery.level / city.battery.capacity < 0.1:
                    criticalCities.append(city) # Critical cities
                elif city.battery.level / city.battery.capacity > 0.20:
                    supportiveCities.append(city) # Balanced city energy level
            if len(criticalCities) > 0 and len(supportiveCities) > 0:
                env.process(self.PerformCityEnergyDistribution(criticalCities, supportiveCities))
            yield self.env.timeout(1)

    def PerformCityEnergyDistribution(self, criticalCities, supportiveCities):
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

    def GetGeneratedEnergy(self):
        while True:
            self.resourceGeneratedEnergy = 0
            for resource in self.resources:
                self.resourceGeneratedEnergy += resource.power(datetime.datetime(2019, 1, 1, self.env.now))

            self.totalEnergyGenerated += self.resourceGeneratedEnergy
            yield self.env.timeout(1)

    def DistributeGeneratedEnergy(self):
        while True:
            energyLevelToDistribute = self.resourceGeneratedEnergy / len(self.cities)
            for city in self.cities:
                city.ProcessIncomingEnergy(energyLevelToDistribute)
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
VirtualPowerGrid.SetCities(Cities)
VirtualPowerGrid.SetResources(Windturbines)

# Add Consumers & Battery to Cities
for city in VirtualPowerGrid.cities:
    consumers = [Consumer(env, SelectRandomConsumerType(), i) for i in range(random.randint(10, 20))]
    for consumer in consumers:
        resource = SelectRandomResourceType()
        consumer.SetResource(resource)  # Set generation resource
        consumer.setResourceSize(random.randint(10, 80))  # set size of resource
        city.AddConsumer(consumer)

    batteryCapacity = len(city.consumerList) * 5000
    cityBatteryContainer = simpy.Container(env, batteryCapacity, init=0.35 * batteryCapacity)
    city.AddBattery(cityBatteryContainer)

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
