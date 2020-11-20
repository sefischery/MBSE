from constants import *


class City(object):
    def __init__(self, env, cityNumber, weather_path):
        # Input parameter initialized
        self.env = env
        self.cityNumber = cityNumber
        self.weather_path = weather_path
        # plot variable
        self.city_battery_level_history = []
        # Dynamic
        self.consumerList = []
        self.battery = None

        # Start process
        env.process(self.overwatch_consumer())

    def set_battery(self, battery):
        self.battery = battery

    def add_consumer(self, consumer):
        self.consumerList.append(consumer)

    def overwatch_consumer(self):
        while True:
            self.city_battery_level_history.append(self.battery.level)

            for consumer in self.consumerList:
                self.env.process(consumer.process_city_energy_grid(self.cityNumber, self.battery))
            yield self.env.timeout(1)

    def process_incoming_energy(self, energy):
        batteryDistance = self.battery.capacity - self.battery.level
        if batteryDistance > 0 and energy > 0:
            if energy > batteryDistance:
                # This means too energy was sent to the city we might consider shutting down some systems or sell the energy
                energy -= batteryDistance
                self.battery.put(batteryDistance * BATTERY_ENERGY_EFFICIENCY)
            else:
                # All incoming energy was distributed to the battery
                self.battery.put(energy * BATTERY_ENERGY_EFFICIENCY)
                return 0

        return energy

    def getResults(self):
        return {
            "city_number": self.cityNumber,
            "consumers": list(map(lambda x: x.getResults(), self.consumerList)),
            "city_battery_level": self.city_battery_level_history,
        }
