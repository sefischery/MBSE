from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import json
import brewer2mpl

# Auxiliary function
def convert_camel_case(string):
    switcher = {
        'HomeConsumer': 'Home consumer',
        'HighUsageConsumer': 'High usage consumer',
        'RegularConsumer': 'Regular consumer',
        'NightConsumer': 'Night consumer'
    }

    return switcher.get(string, 'error')


# Load data
with open("plots/output.json", "r") as f:
    VirtualPowerGrid = json.load(f)

# Generate plot data
amount_of_consumers = {}
consumer_profiles = {}
for city in VirtualPowerGrid['cities']:
    for consumer in city['consumers']:
        if consumer['type'] in amount_of_consumers:
            amount_of_consumers[consumer['type']] += 1
        else:
            amount_of_consumers[consumer['type']] = 0
        if consumer['type'] in consumer_profiles:
            for k, v in consumer['consumedEnergyHistory']:
                consumer_profiles[consumer['type']][k] += v
        else:
            consumer_profiles[consumer['type']] = [b for a, b in consumer['consumedEnergyHistory']]
# Divide sum of power with amount of each consumer type
for k, vs in consumer_profiles.items():
    consumer_profiles[k] = [v / amount_of_consumers[k] for v in vs]

# Plot design metrics
bmap = brewer2mpl.get_map('Set2', 'qualitative', 7)
colors = bmap.mpl_colors
params = {
    'axes.prop_cycle': mpl.cycler(color=colors),
    'axes.labelsize': 8,
    'text.usetex': False,
    'font.size': 8,
    'font.family': 'serif',
    'legend.fontsize': 8,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.figsize': [3.5, 3]
}
mpl.rcParams.update(params)
# Plot
fig = plt.figure()
ax = fig.add_subplot(111)
# Data
for profile, data in consumer_profiles.items():
    ax.plot(data, alpha=1, label=convert_camel_case(profile), linewidth=2)
# Labels
ax.set_xlabel('Time of day')
ax.set_ylabel('Power [W]')
plt.xticks(np.arange(0, 25, 6), [f'{str(i).zfill(1)}:00' for i in np.arange(0, 25, 6)])
#plt.yticks(np.arange(1000, 10000, 2000), [int(i / 1000) for i in np.arange(1000, 10000, 2000)])
#plt.yticks(plt.yticks()[0], [int(i / 1000) for i in plt.yticks()[0]])
plt.xlim([0, 24])
# Plot layout
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()
ax.tick_params(axis='x', direction='out')
ax.tick_params(axis='y', length=0)
# Offset the spines
for spine in ax.spines.values():
  spine.set_position(('outward', 5))
# Put the grid behind
ax.grid(axis='y', color="0.9", linestyle='-', linewidth=1)
ax.set_axisbelow(True)
# Edit legend
legend = ax.legend(loc='best');
frame = legend.get_frame()
frame.set_facecolor('1.0')
frame.set_edgecolor('1.0')

fig.tight_layout()
#plt.show()
fig.savefig('consumer-profiles.pdf')

