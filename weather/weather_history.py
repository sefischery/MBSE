import pandas as pd
import datetime

class WeatherLog:
    def __init__(self, csv_path):
        self.dataFrame = pd.read_csv(csv_path, sep=';', index_col="timestamp_local")

    def get_solar_rad(self, time):
        return self.dataFrame.loc[self.__datetime_to_key_string(time), 'solar_rad']

    def get_wind_speed(self, time):
        return self.dataFrame.loc[self.__datetime_to_key_string(time), 'wind_spd']

    def __datetime_to_key_string(self, dt):
        return dt.strftime("%Y-%m-%dT%H:00:00")


log = WeatherLog("weather.csv")

date = datetime.datetime(2019, 1, 1, 11)
print(log.get_solar_rad(date))
print(log.get_wind_speed(date))
