class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self,flight):
        self.departure_IATA_code=flight['flyFrom']
        self.destination_IATA_code=flight['flyTo']
        self.departure_city=flight['cityFrom']
        self.destination_city=flight['cityTo']
        self.flight_price=flight['price']
        self.out_date=flight['local_departure'].split("T")[0]
        self.return_date=flight['route'][-1]['local_arrival'].split("T")[0]
        self.stop_overs=flight['technical_stops']
        self.via_city=flight['route'][1]['cityTo']


