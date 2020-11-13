from matplotlib import pyplot as plt, patches as pa
import seaborn as sns
import numpy as np
import random
import json

with open("../plots/output.json", "r") as f:
  VirtualPowerGrid = json.load(f)

sns.set_theme()

def pick_random_color():
    r = random.random()
    b = random.random()
    g = random.random()
    return r, g, b


plt.figure(figsize=(20, 10))
# Cities Bar plot
for city in VirtualPowerGrid["cities"]:
    cityEnergyGeneration = 0
    cityEnergyConsumption = 0
    for consumer in city["consumers"]:
        cityEnergyConsumption += np.sum(list(map(lambda x: x[1], consumer["consumedEnergyHistory"])))
        cityEnergyGeneration += np.sum(list(map(lambda x: x[1], consumer["generatedEnergyHistory"])))
    plt.bar(city["city_number"]-0.2, cityEnergyConsumption, width=0.4, color='r')
    plt.bar(city["city_number"]+0.2, cityEnergyGeneration, width=0.4, color='g')
plt.xlabel("Cities")
plt.ylabel("Energy")
plt.xticks(np.arange(0,len(VirtualPowerGrid["cities"])))
redLabel = pa.Patch(color='r', label='Energy consumption')
greenLabel = pa.Patch(color='g', label='Energy Generation')
plt.legend(handles=[redLabel, greenLabel])
plt.show()
