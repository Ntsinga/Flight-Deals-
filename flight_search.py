import os
from pprint import pprint
from dotenv import load_dotenv, dotenv_values
import requests

load_dotenv()
FS_API_KEY = os.getenv("FS_API_KEY")
FS_ENDPOINT = os.getenv("FS_ENDPOINT")
TEQUILA_API_KEY = os.getenv("TEQUILA_API_KEY")
TEQUILA_ENDPOINT = "https://api.tequila.kiwi.com"
TEQUILA_LOCATION_ENDPOINT = f"{TEQUILA_ENDPOINT}/locations/query"


class FlightSearch:

    def retrieve_iata_code(self,city_name):

        header = {
            "apikey": TEQUILA_API_KEY
        }

        tequila_get_parameters = {
            "term": city_name
        }
        # Retrieve city code using locations API
        response = requests.get(TEQUILA_LOCATION_ENDPOINT, params=tequila_get_parameters, headers=header)
        city_code = response.json()['locations'][0]['code']
        return city_code

    def flight_search(self, fly_from_code, fly_to_code, date_from, date_to):
        search_header = {
            "apikey": FS_API_KEY
        }

        search_parameters = {
            "fly_from": fly_from_code,
            "fly_to": fly_to_code,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "GBP"
        }
        response = requests.get(FS_ENDPOINT, params=search_parameters, headers=search_header)
        response.raise_for_status()
        try:
            return response.json()['data'][0]
        except IndexError:
            search_parameters["max_stopovers"]=1
            response = requests.get(FS_ENDPOINT, params=search_parameters, headers=search_header)
            pprint(response.json()['data'])
            try:
                return response.json()['data'][0]
            except IndexError:
                return None


