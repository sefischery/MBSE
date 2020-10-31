import simpy

from DistributedStructure.Consumer import Consumer, SelectRandomConsumerType

SIM_TIME = 24


class City(object):
    def __init__(self, env, cityNumber):
        # Input parameter initialized
        self.env = env
        self.cityNumber = cityNumber

        # Dynamic
        self.consumerList = []
        self.battery = None

        # Start process

    def AddBattery(self, battery):
        self.battery = battery

    def AddConsumer(self, consumer):
        self.consumerList.append(consumer)

    def OverwatchConsumer(self):
        while True:
            for consumer in self.consumerList:
                if consumer.consumedEnergy - consumer.generatedEnergy < 200:
                    self.SendEnergyToConsumer(consumer)
            self.env.timeout(1)

    def SendEnergyToConsumer(self, consumer):
        consumer.ProcessCityEnergy()


# Setup
env = simpy.Environment()

# Initialize Cities
Cities = [City(env, i) for i in range(10)]

# Add Consumers & Battery to Cities
for city in Cities:
    consumers = [Consumer(env, SelectRandomConsumerType(), i) for i in range(10)]
    for consumer in consumers:
        city.AddConsumer(consumer)

    batteryContainer = simpy.Container(env, len(city.consumerList) * 500, init=0)
    city.AddBattery(batteryContainer)
