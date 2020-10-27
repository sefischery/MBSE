import requests
import pandas as pd
import datetime
from requests.exceptions import HTTPError

def gather_weather_json(start_datetime, end_datetime):
        
    date_format = "%Y-%m-%d"
    start_date = start_datetime.strftime(date_format)
    end_date = end_datetime.strftime(date_format)

    api_key = "3005becb7e874467b183c6d4158ad28b" 
    # api_key = "d3493c8dbeb448fbbe804c07a1b11a7b" #Adams key
    
    #Lyngby
    # latitude = "55.784"
    # longitude = "12.519"
    
    #Aarhus
    # latitude = "56.157"
    # longitude = "10.201"

    #Aalborg
    # latitude = "57.046"
    # longitude = "9.931"

    #Kolding
    # latitude = "55.491"
    # longitude = "9.474"

    #Odense
    latitude = "55.396"
    longitude = "10.382"


    frequency = "hourly"


    url = "https://api.weatherbit.io/v2.0/history/" + frequency \
        + "?lat=" + latitude \
        + "&lon=" + longitude \
        + "&start_date=" + start_date \
        + "&end_date=" + end_date \
        + "&tz=local&key=" + api_key \



    try:
        response = requests.get(url)
        response.raise_for_status()

        jsonResponse = response.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occured: {err}")

    return jsonResponse

start_datetime = datetime.datetime(2019, 1, 1)
#dataframe = pd.read_csv("weather.csv", sep=';')
dataframe = pd.DataFrame()

for i in range(365):
    weather = gather_weather_json(start_datetime, start_datetime + datetime.timedelta(days=1))

    new_data = pd.DataFrame(weather["data"])
    dataframe = dataframe.append(new_data, ignore_index = True)

    start_datetime += datetime.timedelta(days=1)
    print(i)



dataframe.to_csv('weather_odense.csv', sep=';')

















# print(weather)
# print()

# for item in weather["data"]:
#     print("Time: " + str(item["timestamp_local"]))
#     print("wind: " + str(item["wind_spd"]))
#     print("solar radiation: " + str(item["solar_rad"]))
#     print("\n")
