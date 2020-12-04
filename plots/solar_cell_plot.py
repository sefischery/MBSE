from matplotlib import pyplot as plt, patches as pa
import numpy as np
import datetime

from pathlib import Path
from weather import weather_history

from DistributedStructure.SolarCell import SolarCell

base_path = Path(__file__).parent
file_path = (base_path / "../weather/data/weather_copenhagen.csv").resolve()

log = weather_history.WeatherLog(file_path)

solar_cell = SolarCell(25)
days = list(map(lambda x: solar_cell.power(datetime.datetime(2019,1,1,0) + datetime.timedelta(hours=int(x))), np.arange(364*24)))

plt.figure(figsize=(20, 10))

plt.fill_between(np.arange(364*24), days, color='g')
plt.xlabel("Time of year [month]")
plt.ylabel("Power generated [Watt]")
plt.xticks(np.arange(15*24, 364*24, 30*24), (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
plt.show()
