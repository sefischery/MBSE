from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import json

# Meta data
with open("../plots/output.json", "r") as f:
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

# Data
power_generation = []
power_consumption = []
for city in VirtualPowerGrid["cities"]:
    power_generated = 0
    power_consumed = 0
    for consumer in city["consumers"]:
        power_generated += consumer["generatedEnergyTotal"]
        power_consumed += consumer["consumedEnergyTotal"]
    power_generation.append(power_generated)
    power_consumption.append(power_consumed)

# Plot metrics
index = np.arange(len(VirtualPowerGrid["cities"]))
bar_width = 0.35
opacity = 1

# Plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
plt.bar(index, power_generation, bar_width, alpha=opacity, label='Power generated')
plt.bar(index + bar_width, power_consumption, bar_width, alpha=opacity, label='Power consumed')
plt.xlabel('Cities')
plt.ylabel('Power [kW]')
plt.title('Total power production/consumption for all cities', fontsize=16)
plt.xticks(index + bar_width / 2,
           ('City 1', 'City 2', 'City 3', 'City 4', 'City 5', 'City 6', 'City 7', 'City 8', 'City 9', 'City 10'),
           fontsize=10)
ax.set_yticklabels((0, 50, 100, 150, 200))
plt.grid(True, which='both', color="#93a1a1", alpha=0.3)
plt.legend(loc='best', fontsize=12)

plt.tight_layout()
plt.show()
