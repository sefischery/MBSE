from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime
import brewer2mpl

from pathlib import Path
from weather import weather_history

from DistributedStructure.SolarCell import SolarCell

# Load data
base_path = Path(__file__).parent
file_path = (base_path / "../weather/data/weather_copenhagen.csv").resolve()
log = weather_history.WeatherLog(file_path)
# Generate plot data
solar_cell = SolarCell(25, '../weather/data/weather_copenhagen.csv')
days = list(map(lambda x: solar_cell.power(datetime.datetime(2019, 1, 1, 0) + datetime.timedelta(hours=int(x))),
                np.arange(364 * 24)))
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
plt.fill_between(np.arange(364 * 24), days, alpha=1)
# Labels
ax.set_xlabel('Time of year [month]')
ax.set_ylabel('Power generated [W]')
plt.xticks(np.arange(15 * 24, 364 * 24, 30 * 24), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
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
fig.tight_layout()

# plt.show()
fig.savefig('output/solar-power.pdf')
