from weather import weather_history


# SOLAR CELL
class SolarCell(object):
    SOLAR_OUTPUT_PER_SECOND = 137

    def __init__(self):
        self.log = weather_history.WeatherLog("C:\\Users\\s164156\\Documents\\MBSE-master\\weather_copenhagen.csv")

    def power(self, datetime):
        return self.log.get_solar_rad(datetime) * 0.2  # 20% efficiency
