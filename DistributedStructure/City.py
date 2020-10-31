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
                self.env.process(consumer.ProcessCityEnergyGrid(self.cityNumber, self.battery))
            yield self.env.timeout(1)

    def ProcessIncomingEnergy(self, energy):
        self.battery.put(energy)

