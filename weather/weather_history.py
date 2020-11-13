import pandas as pd
import datetime


class WeatherLog:
    def __init__(self, csv_path):
        self.dataFrame = pd.read_csv(csv_path, sep=';',
                                     index_col="timestamp_utc")

    def get_solar_rad(self, time):
        solar_before = self.dataFrame.loc[
            self._datetime_to_key_string(time), 'solar_rad']
        solar_after = self.dataFrame.loc[self._datetime_to_key_string(
            time + datetime.timedelta(hours=1)), 'solar_rad']
        solar_change = solar_after - solar_before

        hour_completion = time.minute / 60.0

        return solar_before + (solar_change * hour_completion)

    def get_wind_speed(self, time):
        wind_before = self.dataFrame.loc[
            self._datetime_to_key_string(time), 'wind_spd']
        wind_after = self.dataFrame.loc[self._datetime_to_key_string(
            time + datetime.timedelta(hours=1)), 'wind_spd']
        wind_change = wind_after - wind_before

        hour_completion = time.minute / 60.0

        return wind_before + (wind_change * hour_completion)

    @staticmethod
    def _datetime_to_key_string(dt):
        return dt.strftime("%Y-%m-%dT%H:00:00")

# log = WeatherLog("weather_copenhagen.csv")

# date = datetime.datetime(2019, 1, 1, 11, 30)
# print(log.get_solar_rad(date))
# print(log.get_wind_speed(date))
# print(type(log.get_solar_rad(date)))
