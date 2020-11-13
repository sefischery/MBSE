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

listOfConsumers = [RegularConsumerHourly, NightConsumerHourly, HomeConsumerHourly, HighUsageConsumerHourly]

listOfResources = [None, 'solarCell', 'solarCell', 'solarCell']


class Consumer(object):
    def __init__(self, env, type, houseNumber):
        # Input parameter initialized
        self.env = env
        self.houseNumber = houseNumber
        self.type = type

        # Dynamic variables
        self.consumedEnergy = 0
        self.generatedEnergy = 0

        # Plots
        self.consumerGeneratedEnergyGraphPoints = []
        self.consumerConsumptionEnergyGraphPoints = []

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

            typeList = listOfConsumers_dict.get(self.type)
            energyConsumption = DAILY_USAGE * (typeList[self.env.now] + fluctuation)

            self.consumedEnergy += energyConsumption
            self.consumedEnergyTick = energyConsumption
            self.consumerConsumptionEnergyGraphPoints.append(energyConsumption)
            yield self.env.timeout(1)

    def generate_resource_energy(self):
        if self.resource is not None:
            while True:
                energyGenerated = self.resource.power(datetime.datetime(2019, 1, 1, self.env.now))
                self.generatedEnergy += energyGenerated
                self.generatedEnergyTick = energyGenerated
                self.consumerGeneratedEnergyGraphPoints.append(energyGenerated)
                yield self.env.timeout(1)

    def set_resource(self, resource):
        self.resource = resource

    def set_resource_size(self, size):
        if self.resource is not None:
            print(size)
            self.resource.set_squaremeter_size(size)

    def process_city_energy_grid(self, cityNumber, battery):
        energy = self.generatedEnergyTick - self.consumedEnergyTick
        if energy > 0:
            battery.put(energy) # Give energy to city battery

        elif energy < 0:
            energy = abs(energy)
            if energy > battery.level: # House will experience power outage
                print(f"Power outage in city: {cityNumber}; house: {self.houseNumber}")

            self.cityBatteryUsage += energy
            battery.get(energy) # Take energy from city battery
        yield self.env.timeout(1)


def select_random_consumer_type():
    return random.choice(list(listOfConsumers_dict.keys()))


def select_random_resource_type():
    resource = random.choice(listOfResources)
    if resource == 'solarCell':
        return SolarCell()

    return None
