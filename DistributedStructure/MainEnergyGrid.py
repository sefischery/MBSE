import datetime
import simpy
import json
import os

from DistributedStructure.City import City
from DistributedStructure.Consumer import Consumer, select_random_consumer_type, \
    random_solar_cell
from DistributedStructure.WindTurbine import WindTurbine

from constants import *

WindTurbineEnergyGeneration = []

def is_critical_city(city_):
    return True if city_.battery.level / city_.battery.capacity < CRITICAL_CITY_PERCENTAGE else False


def is_supportive_city(city_):
    return True if city_.battery.level / city_.battery.capacity > SUPPORTIVE_CITY_PERCENTAGE else False


def find_critical_and_supportive_cities(city_list):
    criticalCities = []
    supportiveCities = []
    for city_ in city_list:
        if is_critical_city(city_):
            criticalCities.append(city_)
        elif is_supportive_city(city_):
            supportiveCities.append(city_)
    return criticalCities, supportiveCities


class EnergyGrid(object):
    def __init__(self, env):
        self.env = env

        # Dynamic Variables
        self.cities = []
        self.resources = []
        self.resourceGeneratedEnergy = 0
        self.totalEnergyGenerated = 0
        self.resourceBattery = None

        # Start Grid processes
        env.process(self.get_generated_energy())
        env.process(self.distribute_generated_energy())
        env.process(self.overwatch_cities())
        env.process(self.overwatch_resource_battery())

    def set_battery(self, battery):
        self.resourceBattery = battery

    def set_cities(self, cities):
        self.cities = cities

    def set_resources(self, resources):
        self.resources = resources

    def overwatch_cities(self):
        while True:
            criticalCities, supportiveCities = find_critical_and_supportive_cities(self.cities)
            if len(criticalCities) > 0 and len(supportiveCities) > 0:
                env.process(
                    self.perform_city_energy_distribution(criticalCities,
                                                          supportiveCities))

            # In case we still have critical cities, distribute energy from resource battery
            self.distribute_to_critical_city_from_resource_battery()

            yield self.env.timeout(1)

    def distribute_to_critical_city_from_resource_battery(self):
        for city in self.cities:
            if is_critical_city(city):
                neededEnergy = (
                        (city.battery.capacity * 0.30) - city.battery.level)
                if self.resourceBattery.level > neededEnergy:
                    city.battery.put(neededEnergy)
                    self.resourceBattery.get(neededEnergy)
                else:
                    if self.resourceBattery.level > 0:
                        city.battery.put(self.resourceBattery.level)
                        self.resourceBattery.get(self.resourceBattery.level)

    def overwatch_resource_battery(self):
        while True:
            current_resource_battery_procentage_level = \
                (self.resourceBattery.level / self.resourceBattery.capacity) * 100
            difficultyRating = 100
            for resource in self.resources:
                if resource.online:
                    difficultyRating -= 25 / NUMB_OF_WINDTURBINES

            if current_resource_battery_procentage_level > difficultyRating:
                resource = self.choose_random_resource(self.resources, True)
                if resource is not None:
                    resource.online = False
                    print("Turns off a Windturbine")

            if current_resource_battery_procentage_level < difficultyRating - 30:
                resource = self.choose_random_resource(self.resources, False)
                if resource is not None:
                    resource.online = True
                    print("Turns on a Windturbine")

            yield self.env.timeout(1)

    @staticmethod
    def choose_random_resource(resources, status):
        chooseBetween = []
        resource = None
        for _resource in resources:
            if _resource.online == status:
                chooseBetween.append(_resource)

        if len(chooseBetween) > 0:
            resource = random.choice(chooseBetween)

        return resource

    def perform_city_energy_distribution(self, criticalCities, supportiveCities):
        for criticalCity in criticalCities:
            neededEnergy = ((criticalCity.battery.capacity * 0.30) - criticalCity.battery.level)
            for supportiveCity in supportiveCities:
                if neededEnergy > 0:
                    surPlusEnergy = (supportiveCity.battery.level - (supportiveCity.battery.capacity * 0.50))
                    if surPlusEnergy > 0:
                        if surPlusEnergy < neededEnergy:
                            neededEnergy -= surPlusEnergy
                            supportiveCity.battery.get(surPlusEnergy)
                            criticalCity.battery.put(surPlusEnergy * INTER_CITY_TRANSMISSION_EFFICIENCY)
                            print(
                                f"City {supportiveCity.cityNumber}, sends energy level {surPlusEnergy}, to city {criticalCity.cityNumber}")
                        else:
                            supportiveCity.battery.get(neededEnergy)
                            criticalCity.battery.put(neededEnergy * INTER_CITY_TRANSMISSION_EFFICIENCY)
                            print(
                                f"City {supportiveCity.cityNumber}, sends energy level {neededEnergy}, to city {criticalCity.cityNumber}")
                            neededEnergy -= neededEnergy * INTER_CITY_TRANSMISSION_EFFICIENCY

        yield self.env.timeout(1)

    def get_generated_energy(self):
        date_utc = datetime.datetime(START_YEAR, START_MONTH, START_DAY, START_HOUR)

        while True:
            self.resourceGeneratedEnergy = 0

            for resource in self.resources:
                if resource.online:
                    self.resourceGeneratedEnergy += resource.power(date_utc)

            self.totalEnergyGenerated += self.resourceGeneratedEnergy
            WindTurbineEnergyGeneration.append(self.resourceGeneratedEnergy)

            date_utc += datetime.timedelta(hours=1)
            yield self.env.timeout(1)

    def distribute_generated_energy(self):
        while True:
            if self.resourceGeneratedEnergy > 0:
                criticalCities = []
                remainingCities = []
                #print(f"Total available resource generated energy: {self.resourceGeneratedEnergy}")
                for city in self.cities:
                    if is_critical_city(city):
                        criticalCities.append(city)
                    else:  # Rest of the cities
                        remainingCities.append(city)
                for city in criticalCities:  # Start with the critical cities
                    neededEnergy = ((city.battery.capacity * 0.30) - city.battery.level)  # The energy the city needs
                    if self.resourceGeneratedEnergy > neededEnergy:  # If there is enough generated energy to support the battery
                        city.process_incoming_energy(neededEnergy * WIND_TURBINE_TRANSMISSION_EFFICIENCY)
                        #print(f"Wind turbine sending {neededEnergy} to critical city {city.cityNumber}")
                        self.resourceGeneratedEnergy -= neededEnergy
                        #print(f"Reamining resource generated energy: {self.resourceGeneratedEnergy}")
                    else:  # Send alle the remaining energy to that city
                        city.process_incoming_energy(self.resourceGeneratedEnergy * WIND_TURBINE_TRANSMISSION_EFFICIENCY)
                        #print(f"Wind turbine sending {self.resourceGeneratedEnergy} to critical city {city.cityNumber}")
                        self.resourceGeneratedEnergy = 0
                        #print(f"Reamining resource generated energy: {self.resourceGeneratedEnergy}")
                        break

                for city in remainingCities:  # Continue with the remaining cities
                    neededEnergy = city.battery.capacity - city.battery.level
                    if self.resourceGeneratedEnergy > neededEnergy:  # If there is enough generated energy to support the battery
                        city.process_incoming_energy(neededEnergy * WIND_TURBINE_TRANSMISSION_EFFICIENCY)
                        #print(f"Wind turbine sending {neededEnergy} to city {city.cityNumber}")
                        self.resourceGeneratedEnergy -= neededEnergy
                        #print(f"Reamining resource generated energy: {self.resourceGeneratedEnergy}")
                    else:  # Send alle the remaining energy to that city
                        city.process_incoming_energy(self.resourceGeneratedEnergy * WIND_TURBINE_TRANSMISSION_EFFICIENCY)
                        #print(f"Wind turbine sending {self.resourceGeneratedEnergy} to city {city.cityNumber}")
                        self.resourceGeneratedEnergy = 0
                        #print(f"Reamining resource generated energy: {self.resourceGeneratedEnergy}")
                        break

                self.fill_resource_battery(self.resourceGeneratedEnergy)
            yield self.env.timeout(1)

    def fill_resource_battery(self, energy):
        if energy > 0:
            batteryCapacityDifferenceFromBatteryLevel = self.resourceBattery.capacity - self.resourceBattery.level
            if batteryCapacityDifferenceFromBatteryLevel != 0:
                if energy > batteryCapacityDifferenceFromBatteryLevel:
                    initialEnergy = energy
                    energy = batteryCapacityDifferenceFromBatteryLevel
                    print(f"Windturbines store: {energy}, energy wasted: {initialEnergy - energy}")

                self.resourceBattery.put(energy)
            else:
                print(f"Windturbines store: {0}, energy wasted: {energy}")


# Setup
env = simpy.Environment()

# Initialize Virtual Power Plant Grid
VirtualPowerGrid = EnergyGrid(env)

# Initialize windtubines
Windturbines = []
for i in range(NUMB_OF_WINDTURBINES):
    wing_size = random.randint(*WING_SIZE)
    city_weather = CITIES[i % len(CITIES)]
    wt = WindTurbine(wing_size, city_weather)
    Windturbines.append(wt)


# Initialize Cities
Cities = [City(env, i, CITIES[i % len(CITIES)]) for i in range(NUMB_OF_CITIES)]

# Sets for Virtual Power Plant Grid
VirtualPowerGrid.set_cities(Cities)
VirtualPowerGrid.set_resources(Windturbines)

# Add resource battery
capatity = NUMB_OF_WINDTURBINES * 50000
windturbineBatteryContainer = simpy.Container(env, capatity, init=capatity * 0.85)
VirtualPowerGrid.set_battery(windturbineBatteryContainer)

# Add Consumers & Battery to Cities
for city in VirtualPowerGrid.cities:
    consumers = [Consumer(env, select_random_consumer_type(), i, city.weather_path) for i in range(random.randint(10, 20))]
    for consumer in consumers:
        consumer.set_resource(random_solar_cell(city.weather_path))  # Set generation resource
        city.add_consumer(consumer)

    batteryCapacity = len(city.consumerList) * 10000
    cityBatteryContainer = simpy.Container(env, batteryCapacity, init=batteryCapacity * 0.7)  # 0.35 * batteryCapacity)
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

cityGeneration = []
for hour in range(SIM_TIME):
    generation = 0
    for city in Cities:
        for consumer in city.consumerList:
            if consumer.generatedEnergyHistory != []:
                generation += consumer.generatedEnergyHistory[hour][1]
    cityGeneration.append(generation)
            

print(
    f"End Windturbine battery level: {VirtualPowerGrid.resourceBattery.level}, max capacity: {VirtualPowerGrid.resourceBattery.capacity}")
output = json.dumps({
    "cities": list(map(lambda x: x.getResults(), VirtualPowerGrid.cities)),
    "sim_time": SIM_TIME,
    "wind_turbine_generation_history": WindTurbineEnergyGeneration,
    "consumer_generation_history": cityGeneration
})

if os.path.exists("plots/output.json"):
    os.remove("plots/output.json")
f = open("plots/output.json", "a")
f.write(output)
f.close()
