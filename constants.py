from random import Random

DAYS = 365                  #                                       STATIC DON'T TOUCH
SIM_TIME = 24 * DAYS        # Hours                                 STATIC DON'T TOUCH
CITIES = ["../weather/data/weather_copenhagen.csv", "../weather/data/weather_kolding.csv", "../weather/data/weather_odense.csv", "../weather/data/weather_aalborg.csv", "../weather/data/weather_aarhus.csv"]
NUMB_OF_CITIES = 5          #                                       STATIC DON'T TOUCH

NUMB_OF_WINDTURBINES = 5    # Number of windturbines in our grid.
START_YEAR = 2019           #                                       STATIC DON'T TOUCH
START_MONTH = 1             #                                       STATIC DON'T TOUCH
START_DAY = 1               #                                       STATIC DON'T TOUCH
START_HOUR = 1              #                                       STATIC DON'T TOUCH

WING_SIZE = [20, 80]        # Size span of wind turbines

CITY_POPULATION = [10, 20]

WIND_TURBINE_LIFESPAN_HOURS = 120000

BATTERY_ENERGY_EFFICIENCY = 0.75                                    # STATIC DON'T TOUCH
INTER_CITY_TRANSMISSION_EFFICIENCY = 0.94                           # 6% loss   STATIC DON'T TOUCH
WIND_TURBINE_TRANSMISSION_EFFICIENCY = 0.94                         # 6% loss   STATIC DON'T TOUCH

DAILY_USAGE = 4488          # Watt hours                              STATIC DON'T TOUCH
SOLAR_CELL_RATE = 0.75      # The rate houses have solar cells. 0.75 = 75% solar cells  STATIC DON'T TOUCH
SOLAR_CELL_SIZE = [15, 40]  # Defines minimum and maximum solar cell size

CITY_BATTERY_CAPACITY_PER_CONSUMER = 10000
WIND_TURBINE_BATTERY_CAPACITY = 50000
INITIAL_BATTERY_CHARGE_PERCENTAGE = 0.85

CRITICAL_CITY_PERCENTAGE = 0.25
SUPPORTIVE_CITY_PERCENTAGE = 0.50

random = Random()                                                   # STATIC DON'T TOUCH
random.seed(123)                                                    # STATIC DON'T TOUCH
