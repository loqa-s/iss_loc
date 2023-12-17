import requests


class ISS:
    def __init__(self):
        self.longitude = float
        self.latitude = float

    def get_location(self):
        response = requests.get(url='http://api.open-notify.org/iss-now.json')
        response.raise_for_status()
        data_iss = response.json()
        self.longitude = float(data_iss['iss_position']['longitude'])
        self.latitude = float(data_iss['iss_position']['latitude'])

