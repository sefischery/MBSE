from matplotlib import pyplot as plt
import matplotlib as mpl
import seaborn as sns
import numpy as np
import json

# Meta data
labels = ['20-30m', '30-40m', '40-50m', '50-60m', '60-70m', '70-80m']

outages = [151231, 99140, 57064, 26274, 11661, 1897]
overloads = [54597, 54821, 54733, 55556, 55479, 55452]

x = np.arange(len(labels))
width = 0.35  # the width of the bars

print(outages)
print(overloads)

sns.set_theme()
sns.set(font_scale=2)

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, outages, width, label='Outages')
rects2 = ax.bar(x + width/2, overloads, width, label='Overloads')

ax.set_ylabel("Number of outages and overloads")
ax.set_xticks(x)
ax.set_xticklabels(labels)
#plt.title("Wind turbine wing size: 20-30 m")

ax.set_title('Number of outages and overloads when changing wing size of wind turbines')
ax.set_xticklabels(labels)
ax.legend()

fig.tight_layout()
plt.show()