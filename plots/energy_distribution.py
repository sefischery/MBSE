from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import brewer2mpl

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
    'figure.figsize': [3.5, 2.5]
}
mpl.rcParams.update(params)
# Plot
fig = plt.figure()
ax = fig.add_subplot(111)
# Data
plt.axhline(y=50, color='0.4', linestyle=':')
plt.axhline(y=20, color='0.4', linestyle=':')
ax.plot([40, 50, 55, 55, 50, 45, 20, 10, 10, 20, 25, 30, 30], label='City 1', linewidth=2)
ax.plot([30, 20, 15, 15, 20, 25, 50, 60, 60, 50, 45, 40, 40], label='City 2', linewidth=2)
ax.plot([1, 4, 6, 10], [50, 50, 20, 25], 'x', color='0.4')
ax.plot([1, 5, 6, 9], [20, 25, 50, 50], 'x', color='0.4')
# Labels
ax.set_xlabel('Time')
ax.set_ylabel('Battery levels')
plt.xticks(np.arange(0, 13, 2), [f'' for i in np.arange(0, 13, 2)])
plt.yticks(np.arange(10, 70, 10), [s for s in ['', '20%', '', '', '50%', '']])
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
fig.savefig('output/energy-distribution.pdf')
