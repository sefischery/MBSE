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
# Consumer energy generation plot
for city in VirtualPowerGrid["cities"]:
    history_sum = np.arange(VirtualPowerGrid["sim_time"])
    for consumer in city["consumers"]:
        history = list(consumer["generatedEnergyHistory"])
        for point in history:
            history_sum[point[0]] += point[1]

    plt1 = plt.plot(history_sum, color=pick_random_color())
    plt.xlabel("Hour of day")
    plt.ylabel("Consumer Energy Generation")
    plt1[0].set_label(f"city {city['city_number']}")
plt.legend()
plt.show()
