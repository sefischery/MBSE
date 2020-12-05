from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import json
import brewer2mpl


# Auxiliary function
def compute_monthly_data(data):
    return np.sum(np.resize(data, (12, 730)), axis=1)


# Load JSON
with open("plots/output.json", "r") as f:
    VirtualPowerGrid = json.load(f)

# Generate plot data
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

# Compute cumulative values pr. month
outages_monthly = compute_monthly_data(outages)
overloads_monthly = compute_monthly_data(overloads)

# Plot design metrics
bmap = brewer2mpl.get_map('Set2', 'qualitative', 7)
colors = bmap.mpl_colors
params = {
    'axes.prop_cycle': mpl.cycler(color=colors),
    'axes.labelsize': 8,
    'text.usetex': False,
    'font.size': 8,
    'font.family': 'serif',
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.figsize': [3.5, 2.5]
}
mpl.rcParams.update(params)

index = np.arange(12)
xtick_labels = np.arange(12)
bar_width = 0.175
opacity = 1

# Plot
fig = plt.figure()
ax = fig.add_subplot(111)
# Data
ax.bar(index, overloads_monthly, bar_width, alpha=opacity, label='Overloads')
ax.bar(index + bar_width, outages_monthly, bar_width, alpha=opacity, label='Outages')
# Labels
ax.set_xlabel('Month')
ax.set_ylabel('Number of overloads/outages')
plt.xticks(index + bar_width / 2, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
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
legend = ax.legend(['Overloads', 'Outages'], loc='best');
frame = legend.get_frame()
frame.set_facecolor('1.0')
frame.set_edgecolor('1.0')

fig.tight_layout()
#plt.show()
fig.savefig('high-power.pdf')