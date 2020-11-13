import datetime
import numpy as np
import random

from DistributedStructure.SolarCell import SolarCell

DAILY_USAGE = 4488  # Watt

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

batteryEnergyEfficiency = 0.75 # 25 % Loss

listOfConsumers = [RegularConsumerHourly, NightConsumerHourly, HomeConsumerHourly, HighUsageConsumerHourly]

# The rate houses have solar cells. 0.75 = 75% solar cells
SOLAR_CELL_RATE = 0.75
# Defines minimum and maximum solar cell size
SOLAR_CELL_SIZE = [15, 40]


class Consumer(object):
    def __init__(self, env, type, houseNumber):
        # Input parameter initialized
        self.env = env
        self.houseNumber = houseNumber
        self.type = type
        self.typeGenerationList = listOfConsumers_dict.get(self.type)

        # Dynamic variables
        self.consumedEnergyTotal = 0
        self.generatedEnergyTotal = 0

        # Plots
        self.consumedEnergyHistory = []
        self.generatedEnergyHistory = []

        self.consumedEnergyTick = 0
        self.generatedEnergyTick = 0

        self.resource = None

        self.cityBatteryUsage = 0

        # Start processes
        env.process(self.consume_energy())
        env.process(self.generate_resource_energy())

    def consume_energy(self):
        while True:
            fluctuation = random.uniform(-0.0075, 0.0075)

            hour_of_day = self.env.now % 24
            energyConsumed = DAILY_USAGE * (self.typeGenerationList[hour_of_day] + fluctuation)

            self.consumedEnergyTick = energyConsumed

            self.consumedEnergyTotal += energyConsumed
            self.consumedEnergyHistory.append([self.env.now, energyConsumed])

            yield self.env.timeout(1)

    def generate_resource_energy(self):
        date = datetime.datetime(2019, 1, 1, 0)
        if self.resource is not None:
            while True:
                energyGenerated = self.resource.power(date)
                self.generatedEnergyTick = energyGenerated

                self.generatedEnergyTotal += energyGenerated
                self.generatedEnergyHistory.append([self.env.now, energyGenerated])

                date += datetime.timedelta(hours=1)
                yield self.env.timeout(1)

    def set_resource(self, resource):
        self.resource = resource

    def process_city_energy_grid(self, cityNumber, battery):
        energy = self.generatedEnergyTick - self.consumedEnergyTick

        if energy > 0:
            battery.put(energy * batteryEnergyEfficiency) # Give energy to city battery

        elif energy < 0:
            energy = abs(energy)
            #if energy > battery.level: # House will experience power outage
                #print(f"Power outage in city: {cityNumber}; house: {self.houseNumber}")

            self.cityBatteryUsage += energy
            battery.get(energy) # Take energy from city battery
        yield self.env.timeout(1)


def select_random_consumer_type():
    return random.choice(list(listOfConsumers_dict.keys()))


def random_solar_cell():
    if random.random() < SOLAR_CELL_RATE:
        size = random.uniform(*SOLAR_CELL_SIZE)
        return SolarCell(size)

    return None
