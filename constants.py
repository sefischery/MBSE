DAYS = 365                  #                                       STATIC DON'T TOUCH
SIM_TIME = 24 * DAYS        # Hours                                 STATIC DON'T TOUCH
NUMB_OF_CITIES = 5          # Number of cities                      STATIC DON'T TOUCH
NUMB_OF_WINDTURBINES = 6    # Number of windturbines in our grid.
START_YEAR = 2019           #                                       STATIC DON'T TOUCH
START_MONTH = 1             #                                       STATIC DON'T TOUCH
START_DAY = 1               #                                       STATIC DON'T TOUCH
START_HOUR = 1              #                                       STATIC DON'T TOUCH

WING_SIZE = [20, 80]        # Size span of wind turbines

WIND_TURBINE_LIFESPAN_HOURS = 120000

BATTERY_ENERGY_EFFICIENCY = 0.75                                    # STATIC DON'T TOUCH
INTER_CITY_TRANSMISSION_EFFICIENCY = 0.94                           # 6% loss   STATIC DON'T TOUCH
WIND_TURBINE_TRANSMISSION_EFFICIENCY = 0.94                         # 6% loss   STATIC DON'T TOUCH

DAILY_USAGE = 4488          # Watt                                                      STATIC DON'T TOUCH
SOLAR_CELL_RATE = 0.75      # The rate houses have solar cells. 0.75 = 75% solar cells  STATIC DON'T TOUCH
SOLAR_CELL_SIZE = [15, 40]  # Defines minimum and maximum solar cell size

CRITICAL_CITY_PERCENTAGE = 0.25
SUPPORTIVE_CITY_PERCENTAGE = 0.50

RANDOM_SEED = 123                                                   # STATIC DON'T TOUCH