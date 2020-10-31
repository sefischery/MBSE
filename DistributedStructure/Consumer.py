import datetime
import simpy
import numpy as np
import random

from DistributedStructure.SolarCell import SolarCell

SIM_TIME = 24
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

listOfResources = [None, SolarCell()]


class Consumer(object):
    def __init__(self, env, type, houseNumber):
        # Input parameter initialized
        self.env = env
        self.houseNumber = houseNumber
        self.type = type

        # Dynamic variables
        self.consumedEnergy = 0
        self.generatedEnergy = 0
        self.resource = None

        # Start processes
        env.process(self.ConsumeEnergy())
        env.process(self.GenerateResourceEnergy())

    def ConsumeEnergy(self):
        while True:
            typeList = listOfConsumers_dict.get(self.type)
            fluctuation = random.uniform(-0.0075, 0.0075)
            energyConsumption = DAILY_USAGE * (typeList[env.now] + fluctuation)
            self.consumedEnergy += energyConsumption
            yield consumerContainer.put(energyConsumption)
            yield self.env.timeout(1)

    def GenerateResourceEnergy(self):
        if self.resource is not None:
            while True:
                energy = self.resource.power(datetime.datetime(2019, 1, 1, 11)) * 2  # TODO: Make date variable
                self.generatedEnergy += energy
                yield env.timeout(1)

    def SetResource(self, resource):
        self.resource = resource

    def ProcessCityEnergy(self):
        print()


def SelectRandomConsumerType():
    return random.choice(list(listOfConsumers_dict.keys()))


def SelectRandomResourceType():
    return random.choice(listOfResources)


# Setup
env = simpy.Environment()

consumers = [Consumer(env, SelectRandomConsumerType(), i) for i in range(10)]

# Initialize all consumers
for consumer in consumers:
    resource = SelectRandomResourceType()
    consumer.SetResource(resource)

# Create consumer contrainer
consumerContainer = simpy.Container(env, 100000, init=0)

# Execute!
env.run(until=SIM_TIME)

for consumer in consumers:
    print(f"Consumertype: {consumer.type}, total energy consumed {consumer.consumedEnergy}, total energy generated: {consumer.generatedEnergy}")
