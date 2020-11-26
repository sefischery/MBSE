from matplotlib import pyplot as plt, patches as pa
import seaborn as sns
import numpy as np
import random
import json
import math

with open("plots/output.json", "r") as f:
  VirtualPowerGrid = json.load(f)

sns.set_theme()

def pick_random_color():
    r = random.random()
    b = random.random()
    g = random.random()
    return r, g, b

consumer_generation = VirtualPowerGrid["consumer_generation_history"]
wind_generation = VirtualPowerGrid["wind_turbine_generation_history"]

consumer_per_day = []
wind_per_day = []
hour = 0
consumer_today = 0
wind_today = 0
for consumer, wind in zip(consumer_generation, wind_generation):
  consumer_today += consumer
  wind_today += wind
  hour += 1
  if hour == 24:
    consumer_per_day.append(consumer_today)
    wind_per_day.append(wind_today)
    consumer_today = 0
    wind_today = 0
    hour = 0



consumer_share = []
for consumer, wind in zip(consumer_per_day, wind_per_day):
  if consumer == 0.0:
    consumer_share.append(0.0)
  else:
    consumer_share.append((consumer / (consumer+wind)))
  

sim_days = len(consumer_share)

plt.figure(figsize=(20, 10))

plt.plot(np.arange(0, sim_days), consumer_share, color='tab:red', label='Consumers')
plt.xlabel("Day of year")
plt.ylabel("Share of total power generation")
plt.legend()
plt.show()