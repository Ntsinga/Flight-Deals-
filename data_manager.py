import requests

SHEETY_ENDPOINT = "https://api.sheety.co/5c5c46a3644c128e7dea666704bb56cc/flightDeals/prices"


class DataManager:
    def __init__(self):
        # This class is responsible for talking to the Google Sheet.
        self.google_sheet={}

    def retrieve_googlesheet_data(self):
        # Retrieve names of cities from Google sheets
        response2 = requests.get(SHEETY_ENDPOINT)
        self.google_sheet = response2.json()['prices']
        return self.google_sheet

    def update_cityIATA_codes(self):
        for row in self.google_sheet:
            # Modify sheety put endpoint with the appropriate city index
            sheety_put_endpoint=f"{SHEETY_ENDPOINT}/{row['id']}"
            # Set sheety put parameters
            sheety_parameters={
                "price":{
                    "iataCode":row['iataCode']
                }
            }
            # Update google sheet with the IATA Code for that city
            response1=requests.put(sheety_put_endpoint,json=sheety_parameters)