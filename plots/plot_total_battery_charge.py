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

battery_charge = []
for hour in range(sim_time):
    charge = 0
    for city in cities:
        charge += city["city_battery_level"][hour]
    charge += resource_battery_history[hour]
    battery_charge.append(charge)



print("Minimum charge measured: " + str(min(battery_charge)))
print("Maximum charge measured: " + str(max(battery_charge)))

print("Difference: " + str(max(battery_charge) - min(battery_charge)))

outages = np.zeros(sim_time)
overloads = np.zeros(sim_time)

total_cities = 0

#for city in VirtualPowerGrid["cities"]:
plt.plot(np.arange(0, sim_time), battery_charge, color='tab:red', label='Outages')

sns.set_theme()
sns.set(font_scale=2)

plt.show()