from matplotlib import pyplot as plt, patches as pa
import matplotlib as mpl
import numpy as np
import datetime
import brewer2mpl

from pathlib import Path
from weather import weather_history

# Load data
base_path = Path(__file__).parent
file_path = (base_path / "../weather/data/weather_copenhagen.csv").resolve()
log = weather_history.WeatherLog(file_path)
# Fetch plot data
januar = datetime.datetime(2019, 1, 1, 0)
april = datetime.datetime(2019, 4, 1, 0)
july = datetime.datetime(2019, 7, 1, 0)
october = datetime.datetime(2019, 10, 1, 0)

# Generate plot data
day_to_solar_rad_plot = lambda x: list(map(lambda y: sum(map(lambda day: log.get_solar_rad_from_utc(y + datetime.timedelta(days=int(day))), np.arange(28)))/28, map(lambda z: x + datetime.timedelta(hours=int(z)), np.arange(24))))

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
plt.fill_between(np.arange(24), day_to_solar_rad_plot(july), label='July')
plt.fill_between(np.arange(24), day_to_solar_rad_plot(april), label='April')
october_data = day_to_solar_rad_plot(october)
october_data[0] = 0.0
october_data[-1] = 0.0
plt.fill_between(np.arange(24), october_data, label='October')
plt.fill_between(np.arange(24), day_to_solar_rad_plot(januar), label='January')
# Labels
ax.set_xlabel('Time of day')
ax.set_ylabel('Solar radiation [W/m²]')
plt.xticks(np.arange(0, 25, 6), [f'{str(i).zfill(1)}:00' for i in np.arange(0, 25, 6)])
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
handles, labels = ax.get_legend_handles_labels()
# Change order of handles and labels
order = [3, 1, 0, 2]
legend = ax.legend([handles[i] for i in order], [labels[i] for i in order], loc='best');
frame = legend.get_frame()
frame.set_facecolor('1.0')
frame.set_edgecolor('1.0')
fig.tight_layout()

#plt.show()
fig.savefig('solar-radiation-non-utc.pdf')