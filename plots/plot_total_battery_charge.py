from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
import json

# Meta data
with open("plots/output.json", "r") as f:
    VirtualPowerGrid = json.load(f)

# Colors (to match DTU color palette)
colors = ['#2F3EEA',  # Navy blue
          '#030F4F',  # Blue
          '#79238E',  # Purple
          '#E83F48',  # Red
          '#FC7634',  # Orange
          '#F7BBB1',  # Pink
          '#F6D04D',  # Yellow
          '#1FD082',  # Bright Green
          '#008835',  # Green
          '#DADADA']  # Grey

mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors)

sim_time = VirtualPowerGrid["sim_time"]
cities = VirtualPowerGrid["cities"]
resource_battery_history = VirtualPowerGrid["resource_battery_history"]

city1History = []
city4History = []

battery_charge_sum = []
battery_charge_consumers = []
for hour in range(sim_time):
    charge = 0
    for city in cities:
        charge += city["city_battery_level"][hour]
        if city["city_number"] == 1:
            city1History.append(city["city_battery_level"][hour])
        if city["city_number"] == 4:
            city4History.append(city["city_battery_level"][hour])
    battery_charge_consumers.append(charge)
    charge += resource_battery_history[hour]
    battery_charge_sum.append(charge)



print("Minimum charge measured: " + str(min(battery_charge_sum)))
print("Maximum charge measured: " + str(max(battery_charge_sum)))

print("Difference: " + str(max(battery_charge_sum) - min(battery_charge_sum)))

outages = np.zeros(sim_time)
overloads = np.zeros(sim_time)

total_cities = 0

#for city in VirtualPowerGrid["cities"]:
plt.plot(np.arange(0, sim_time), battery_charge_sum, color='tab:red', label='Total battery charge')
plt.plot(np.arange(0, sim_time), battery_charge_consumers, color='tab:blue', label='City battery charge')
plt.plot(np.arange(0, sim_time), resource_battery_history, color='tab:green', label='Wind turbine battery charge')
plt.plot(np.arange(0, sim_time), city1History, color='tab:cyan', label='City 1')
plt.plot(np.arange(0, sim_time), city4History, color='tab:purple', label='City 4')


plt.xlabel("Time of year [hour]")
plt.ylabel("Energy stored [Wh]")

sns.set_theme()
sns.set(font_scale=2)

plt.legend(loc = 2, prop = {'size': 10})
plt.show()