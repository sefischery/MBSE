from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns
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

sim_time = VirtualPowerGrid["sim_time"]

outages = np.zeros(sim_time)
overloads = np.zeros(sim_time)

totalConsumers = 0

for city in VirtualPowerGrid["cities"]:
    totalConsumers += len(city["consumers"])
    for consumer in city["consumers"]:
        for x in consumer["outages"]:
            outages[x] += 1
        for x in consumer["overloads"]:
            overloads[x] += 1

sns.set_theme()
sns.set(font_scale=2)

plt.figure(figsize=(20, 10))
# Draw windturbine energy generation
plt.plot(np.arange(0, sim_time), outages, color='tab:red', label='Outages')
plt.plot(np.arange(0, sim_time), overloads, color="tab:green", label="Overloads")
plt.xlabel("Time of year [start of month]")
plt.ylabel("Consumers experiencing outages / overloads (total " + str(totalConsumers) + ")")

days = sim_time / 24
months = days / 30
plt.xticks(np.arange(0,sim_time, step=30*24), np.arange(0, months, dtype=np.int32))
plt.legend()
plt.show()