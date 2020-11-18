from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import json


# Auxiliary function
def convert_camel_case(string):
    switcher = {
        'HomeConsumer': 'Home consumer',
        'HighUsageConsumer': 'High usage consumer',
        'RegularConsumer': 'Regular consumer',
        'NightConsumer': 'Night consumer'
    }

    return switcher.get(string, 'error')

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
consumer_profiles = {}
for city in VirtualPowerGrid['cities']:
    for consumer in city['consumers']:
        if consumer['type'] in consumer_profiles:
            consumer_profiles[consumer['type']] += consumer['consumedEnergyTotal']
        else:
            consumer_profiles[consumer['type']] = consumer['consumedEnergyTotal']

# Plot metrics
index = np.arange(len(consumer_profiles))
bar_width = 0.175
opacity = 1

# Plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
plt.bar(index, consumer_profiles.values(), bar_width, alpha=opacity, label='Power consumed')
plt.xlabel('Consumer types')
plt.ylabel('Power [kW]')
plt.title('Consumer profiles', fontsize=16)
plt.xticks(index, [f'{convert_camel_case(k)}' for k in consumer_profiles.keys()], fontsize=10)
plt.yticks(plt.yticks()[0], [int(i/1000) for i in plt.yticks()[0]], fontsize=10)
plt.grid(True, which='both', color="#93a1a1", alpha=0.3)
plt.legend(loc='best', fontsize=12)

plt.tight_layout()
plt.show()


