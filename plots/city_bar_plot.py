from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import json

# TODO: Add plots for `power received' and `power transmitted'

# Meta data
with open("../plots/output.json", "r") as f:
    VirtualPowerGrid = json.load(f)

# Colors (to match DTU color palette)
colors = ['#030F4F',  # Navy blue
          '#2F3EEA',  # Blue
          '#79238E',  # Purple
          '#E83F48',  # Red
          '#FC7634',  # Orange
          '#F7BBB1',  # Pink
          '#F6D04D',  # Yellow
          '#1FD082',  # Bright Green
          '#008835',  # Green
          '#DADADA']  # Grey

mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors)

# Data
power_generation = []
power_consumption = []
power_receive = [100000, 100000, 100000, 100000, 100000, 100000]
power_transmit = [100000, 100000, 100000, 100000, 100000, 100000]
for city in VirtualPowerGrid["cities"]:
    power_generated = 0
    power_consumed = 0
    power_received = 0
    power_transmitted = 0
    for consumer in city["consumers"]:
        power_generated += consumer["generatedEnergyTotal"]
        power_consumed += consumer["consumedEnergyTotal"]
        power_received += consumer["receivedEnergyTotal"]
        power_transmitted += consumer["transmittedEnergyTotal"]
    power_generation.append(power_generated)
    power_consumption.append(power_consumed)

# Plot metrics
index = np.arange(len(VirtualPowerGrid["cities"]))
xtick_labels = [f'City {i + 1}' for i in index]
print(xtick_labels)
bar_width = 0.35
opacity = 1

# Plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
plt.bar(index, power_generation, bar_width, alpha=opacity, label='Power generated')
plt.bar(index + bar_width, power_consumption, bar_width, alpha=opacity, label='Power consumed')
plt.bar(index + bar_width * 2, power_receive, bar_width, alpha=opacity, label='Power received')
plt.bar(index + bar_width * 3, power_transmit, bar_width, alpha=opacity, label='Power transmitted')
plt.xlabel('Cities')
plt.ylabel('Power [kW]')
plt.title('Total power production/consumption for all cities', fontsize=16)
plt.xticks(index + bar_width * 1.5, xtick_labels, fontsize=10)
ax.set_yticklabels((0, 500, 1000, 1500, 2000, 2500, 3000))    # TODO: Make dynamic, i.e. not hardcoded
plt.grid(True, which='both', color="#93a1a1", alpha=0.3)
plt.legend(loc='best', fontsize=12)

plt.tight_layout()
plt.show()
