from matplotlib import pyplot as plt
import matplotlib as mpl
import brewer2mpl
import numpy as np

# Meta data
labels = ['20-30', '30-40', '40-50', '50-60', '60-70', '70-80']
outages = [151231, 99140, 57064, 26274, 11661, 1897]
overloads = [54597, 54821, 54733, 55556, 55479, 55452]
x = np.arange(len(labels))
width = 0.35    # the width of the bars

print(outages)
print(overloads)

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
ax.bar(x - width/2, outages, width, label='Outages')
ax.bar(x + width/2, overloads, width, label='Overloads')
# Labels
ax.set_xlabel('Wing size [m]')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Number of overloads/outages')
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
plt.show()
fig.savefig('output/wing-size.pdf')