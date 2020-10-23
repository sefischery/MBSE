import requests
from requests.exceptions import HTTPError

start_date = "2020-10-21"
end_date = "2020-10-22"

api_key = "3005becb7e874467b183c6d4158ad28b"
latitude = "55.784"
longitude = "12.519"
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


for item in jsonResponse["data"]:
    print("Time: " + str(item["timestamp_local"]))
    print("wind: " + str(item["wind_spd"]))
    print("solar radiation: " + str(item["solar_rad"]))
    print("\n")
