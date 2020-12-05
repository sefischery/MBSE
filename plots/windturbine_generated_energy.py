from matplotlib import pyplot as plt, patches as pa
import seaborn as sns
import numpy as np
import random
import json

with open("plots/output.json", "r") as f:
  VirtualPowerGrid = json.load(f)

sns.set_theme()

def pick_random_color():
    r = random.random()
    b = random.random()
    g = random.random()
    return r, g, b


plt.figure(figsize=(20, 10))
# Draw windturbine energy generation
plt.plot(np.arange(0, VirtualPowerGrid["sim_time"]), VirtualPowerGrid["wind_turbine_generation_history"], color='tab:red', label='Wind Turbine')
plt.xlabel("Hour of day")
plt.ylabel("Windturbine Energy Generation")
plt.legend()
plt.show()