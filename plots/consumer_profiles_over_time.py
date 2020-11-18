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
colors = ['#2F3EEA',  # Blue
          '#FC7634',  # Orange
          '#008835',  # Green
          '#E83F48',  # Red
          '#79238E',  # Purple
          '#F7BBB1',  # Pink
          '#F6D04D',  # Yellow
          '#1FD082',  # Bright Green
          '#030F4F',  # Navy blue
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

# Create cumulative data
data_cumsum = np.cumsum([values for values in consumer_profiles.values()], axis=0)

# Assign
for i, (profile, _) in enumerate(consumer_profiles.items()):
    consumer_profiles[profile] = data_cumsum[i][:]

# Plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)

# Plot in reverse order from largest cumulative values to lowest
for profile, data in reversed(consumer_profiles.items()):
    plt.plot(data[:24 + 1], alpha=1, label=convert_camel_case(profile), linewidth=2)
    ax.fill_between(np.arange(24 + 1), y1=data[:24 + 1], y2=0, alpha=0.8)
plt.xlabel('Time of day')
plt.ylabel('Power [kW]')
plt.title('Daily power usage pattern for the four user profiles', fontsize=16)
plt.xticks(np.arange(0, 24 + 1), [f'{str(i).zfill(2)}:00' for i in np.pad(np.arange(24), (0, 1))], fontsize=10)
plt.yticks(plt.yticks()[0], [int(i / 1000) for i in plt.yticks()[0]], fontsize=10)
plt.xlim([0, 24])
plt.ylim([0, plt.yticks()[0][-1]])
plt.grid(True, which='both', color="#93a1a1", alpha=0.3)
plt.legend(loc='best', fontsize=12)

plt.tight_layout()
plt.show()
# plt.savefig('consumer_profiles_over_time.pdf', format='pdf')   # (uncomment to save plot)
