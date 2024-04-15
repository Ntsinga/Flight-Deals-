
from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData
from notification_manager import NotificationManager

CITY_IATA_CODE = "EBB"

# loading variables from .env file

flight_search = FlightSearch()
notification = NotificationManager()
google_sheet_manager = DataManager()
sheet_data = google_sheet_manager.retrieve_googlesheet_data()

# Flight Dates
today = datetime.now()
tomorrow = today + timedelta(days=1)
date_from = tomorrow.strftime("%d/%m/%Y")
date_in_6months = datetime(day=tomorrow.day, month=(tomorrow.month + 6) % 12,
                           year=tomorrow.year + (tomorrow.month + 6) // 12)
date_to = date_in_6months.strftime("%d/%m/%Y")

if sheet_data[0]["iataCode"] == "":
    for row in sheet_data:
        row['iataCode'] = flight_search.retrieve_iata_code(row['city'])
    google_sheet_manager.google_sheet = sheet_data
    google_sheet_manager.update_cityIATA_codes()

for city in sheet_data:

    available_flight = flight_search.flight_search(fly_from_code=CITY_IATA_CODE, fly_to_code=city['iataCode'],
                                                   date_from=date_from, date_to=date_to)
    print(f'h{available_flight}')
    if available_flight is not None:
        flight_data = FlightData(available_flight)
        print(flight_data.via_city)
        print(flight_data.stop_overs)
        if available_flight['price'] <= city['lowestPrice']:
            message = f"Low Price Alert!Only {flight_data.flight_price} to fly from Entebbe-{flight_data.departure_IATA_code} to {flight_data.destination_city}-{flight_data.destination_IATA_code} from {flight_data.out_date} to {flight_data.return_date}\n"
            if flight_data.stop_overs > 0:
                message += f"Flight has {flight_data.stop_overs} stop_overs via {flight_data.via_city}"
            # notification.send_notification(message)
            notification.send_emails(message)
