from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np
import json

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


# Plot

plt.tight_layout()
plt.show()
