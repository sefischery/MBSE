from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import json
import brewer2mpl

# Load data
with open('../plots/output.json', 'r') as f:
    VirtualPowerGrid = json.load(f)
# Generate plot data
sim_time = VirtualPowerGrid['sim_time']
cities = VirtualPowerGrid['cities']
resource_battery_history = VirtualPowerGrid['resource_battery_history']
city1History = []
city4History = []
battery_charge_sum = []
battery_charge_consumers = []
for hour in range(sim_time):
    charge = 0
    for city in cities:
        charge += city['city_battery_level'][hour]
        if city['city_number'] == 1:
            city1History.append(city['city_battery_level'][hour])
        if city['city_number'] == 4:
            city4History.append(city['city_battery_level'][hour])
    battery_charge_consumers.append(charge)
    charge += resource_battery_history[hour]
    battery_charge_sum.append(charge)

print('Minimum charge measured: ' + str(min(battery_charge_sum)))
print('Maximum charge measured: ' + str(max(battery_charge_sum)))
print('Difference: ' + str(max(battery_charge_sum) - min(battery_charge_sum)))

outages = np.zeros(sim_time)
overloads = np.zeros(sim_time)
total_cities = 0

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
    'figure.figsize': [3.5, 3.5]
}
mpl.rcParams.update(params)
# Plot
fig = plt.figure()
ax = fig.add_subplot(111)

battery_charge_sum = np.divide(battery_charge_sum, 1000000)
battery_charge_consumers = np.divide(battery_charge_consumers, 1000000)
resource_battery_history = np.divide(resource_battery_history, 1000000)
city1History = np.divide(city1History, 1000000)
city4History = np.divide(city4History, 1000000)

# Data
plt.plot(np.arange(0, sim_time), battery_charge_sum, label='Total battery charge')
plt.plot(np.arange(0, sim_time), battery_charge_consumers, label='City battery charge')
plt.plot(np.arange(0, sim_time), resource_battery_history, label='Wind turbine battery charge')
plt.plot(np.arange(0, sim_time), city1History, label='City 1')
plt.plot(np.arange(0, sim_time), city4History, label='City 4')
# Labels
ax.set_xlabel('Time of year [hour]')
ax.set_ylabel('Power stored [MWh]')
# plt.xticks(np.arange(15 * 24, 364 * 24, 30 * 24), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
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

# plt.show()
fig.savefig('output/approximate-battery.pdf')
