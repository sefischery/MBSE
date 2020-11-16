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
            for k, v in consumer['consumedEnergyHistory']:
                consumer_profiles[consumer['type']][k] += v
        else:
            consumer_profiles[consumer['type']] = [b for a, b in consumer['consumedEnergyHistory']]

# Plot metrics
opacity = 1

# Plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
for profile, data in consumer_profiles.items():
    plt.plot(data[:24 + 1], alpha=opacity, label=convert_camel_case(profile))
plt.xlabel('Time [hours]')
plt.ylabel('Power [kW]')
plt.title('Power usage of user profiles over time', fontsize=16)
plt.xticks(np.arange(0, 24 + 1), [f'{str(i).zfill(2)}:00' for i in np.pad(np.arange(24), (0, 1))], fontsize=10)
plt.yticks(plt.yticks()[0], [int(i/1000) for i in plt.yticks()[0]], fontsize=10)
plt.xlim([0, 24])
plt.grid(True, which='both', color="#93a1a1", alpha=0.3)
plt.legend(loc='best', fontsize=12)

plt.tight_layout()
plt.show()
#plt.savefig('consumer_profiles_over_time.pdf', format='pdf')   # (uncomment to save plot)