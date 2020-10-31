import simpy
from DistributedStructure.Consumer import Consumer, SelectRandomConsumerType, SelectRandomResourceType

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
        env.process(self.OverwatchConsumer())

    def AddBattery(self, battery):
        self.battery = battery

    def AddConsumer(self, consumer):
        self.consumerList.append(consumer)

    def OverwatchConsumer(self):
        while True:
            for consumer in self.consumerList:
                env.process(consumer.ProcessCityEnergyGrid(self.cityNumber, self.battery))
            yield self.env.timeout(1)



# Setup
env = simpy.Environment()

# Initialize Cities
Cities = [City(env, i) for i in range(2)]

# Add Consumers & Battery to Cities
for city in Cities:
    consumers = [Consumer(env, SelectRandomConsumerType(), i) for i in range(10)]
    for consumer in consumers:
        resource = SelectRandomResourceType()
        consumer.SetResource(resource)
        city.AddConsumer(consumer)

    batteryContainer = simpy.Container(env, len(city.consumerList) * 5000, init=len(city.consumerList) * 5000)
    city.AddBattery(batteryContainer)

# Execute!
env.run(until=SIM_TIME)

# Printer functionality
for city in Cities:
    print(
        f"City: {city.cityNumber}, number of consumers in city: {len(city.consumerList)}, city battery level: {city.battery.level}, battery start level: {city.battery.capacity}")
    cityConsumption = 0
    for consumer in city.consumerList:
        cityConsumption += consumer.consumedEnergy
        print(f"    Consumertype: {consumer.type}, total energy consumed "
              f"{consumer.consumedEnergy}, total energy generated: {consumer.generatedEnergy}, "
              f"total energy used from battery: {consumer.cityBatteryUsage}")
    print(f"total city energy consumption: {cityConsumption}")
    print()
