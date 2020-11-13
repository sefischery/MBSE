batteryEnergyEfficiency = 0.75 # Battery charging loss


class City(object):
    def __init__(self, env, cityNumber):
        # Input parameter initialized
        self.env = env
        self.cityNumber = cityNumber

        # Dynamic
        self.consumerList = []
        self.battery = None

        # Start process
        env.process(self.overwatch_consumer())

    def add_battery(self, battery):
        self.battery = battery

    def add_consumer(self, consumer):
        self.consumerList.append(consumer)

    def overwatch_consumer(self):
        while True:
            for consumer in self.consumerList:
                self.env.process(consumer.process_city_energy_grid(self.cityNumber, self.battery))
            yield self.env.timeout(1)

    def process_incoming_energy(self, energy):
        batteryDistance = self.battery.capacity - self.battery.level
        if batteryDistance > 0:
            if energy > batteryDistance:
                # This means too energy was sent to the city we might consider shutting down some systems or sell the energy
                energy -= batteryDistance
                self.battery.put(batteryDistance * batteryEnergyEfficiency)
            else:
                # All incoming energy was distributed to the battery
                self.battery.put(energy * batteryEnergyEfficiency)
