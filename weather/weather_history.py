import pandas as pd
import datetime
import pytz


class WeatherLog:
    def __init__(self, csv_path):
        self.dataFrame = pd.read_csv(csv_path, sep=';',
                                     index_col="timestamp_utc")

    def get_solar_rad_from_utc(self, date_now):
        date_later = date_now + datetime.timedelta(hours=1)

        solar_before = self.dataFrame.loc[self._datetime_to_key_string(date_now), 'solar_rad']
        solar_after  = self.dataFrame.loc[self._datetime_to_key_string(date_later), 'solar_rad']
        solar_change = solar_after - solar_before

        hour_completion = date_now.minute / 60.0

        return solar_before + (solar_change * hour_completion)

    def get_wind_speed_from_utc(self, date_now):
        date_later = date_now + datetime.timedelta(hours=1)

        wind_before = self.dataFrame.loc[self._datetime_to_key_string(date_now), 'wind_spd']
        wind_after  = self.dataFrame.loc[self._datetime_to_key_string(date_later), 'wind_spd']
        wind_change = wind_after - wind_before

        hour_completion = date_now.minute / 60.0

        return wind_before + (wind_change * hour_completion)

    @staticmethod
    def _datetime_to_key_string(dt):
        return dt.strftime("%Y-%m-%dT%H:00:00")

danish_timezone = pytz.timezone('Europe/Copenhagen')
def utc_to_danish_time(date):
    return date.replace(tzinfo=pytz.utc).astimezone(danish_timezone)


#2019-03-31T02:00:00

# log = WeatherLog("weather/data/2019/weather_copenhagen.csv")

# date = datetime.datetime(2019, 3, 31, 1, 0)

# for i in range (5):
#     print(date)
#     print(log.get_wind_speed_from_utc(date))
#     date += datetime.timedelta(hours=1)

