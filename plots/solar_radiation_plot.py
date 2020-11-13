from matplotlib import pyplot as plt, patches as pa
import seaborn as sns
import numpy as np
import datetime

from pathlib import Path
from weather import weather_history

base_path = Path(__file__).parent
file_path = (base_path / "../weather/data/2019/weather_copenhagen.csv").resolve()

log = weather_history.WeatherLog(file_path)

januar = datetime.datetime(2019, 1, 1, 0)
april = datetime.datetime(2019, 4, 1, 0)
july = datetime.datetime(2019, 7, 1, 0)
october = datetime.datetime(2019, 10, 1, 0)

sns.set_theme()

day_to_solar_rad_plot = lambda x: list(map(lambda y: sum(map(lambda day: log.get_solar_rad(y + datetime.timedelta(days=int(day))), np.arange(28)))/28,map(lambda z: x + datetime.timedelta(hours=int(z)), np.arange(24))))

plt.figure(figsize=(20, 10))

sns.set(font_scale=5)
plt.fill_between(np.arange(24),day_to_solar_rad_plot(july), color='g')
plt.fill_between(np.arange(24),day_to_solar_rad_plot(april), color='b')
plt.fill_between(np.arange(24),day_to_solar_rad_plot(october), color='y')
plt.fill_between(np.arange(24),day_to_solar_rad_plot(januar), color='r')
plt.xlabel("Time of day [hour]")
plt.ylabel("Solar radiation [W/sqm]")
plt.xticks(np.arange(0,24, 2))
redLabel = pa.Patch(color='r', label='January')
blueLabel = pa.Patch(color='b', label='April')
greenLabel = pa.Patch(color='g', label='July')
yellowLabel = pa.Patch(color='y', label='October')
plt.legend(handles=[redLabel, blueLabel, greenLabel, yellowLabel])
plt.show()
