#! ./env/bin/python3

import os
import json
import csv

from geopy.geocoders import GoogleV3
from geopy.extra.rate_limiter import RateLimiter
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

os.chdir('./winco_foods')

store_latlon = []
errors = []

with open('store_data.json', 'r') as json_data:
    store_data = json.load(json_data)

geolocator = GoogleV3(user_agent='wincoGeocoder', api_key=api_key)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

for store in store_data['stores']:
    address = store['address']
    city = store['city']
    state = store['state']
    zip_code = store['zip']
    geo_addr = f'{address}, {city}, {state} {zip_code}'
    location = geocode(geo_addr)
    if location is not None:
        store_latlon.append((location.latitude, location.longitude))
        print(
            f'Found coordinates for: {geo_addr}, at latitude: {location.latitude} and longitude: {location.longitude}')
    else:
        print(
            f'Did not found coordinates for: {geo_addr}')
        errors.append(geo_addr + '\n')

with open('winco_locations.csv', 'w') as csv_file:
    location_file = csv.writer(csv_file)
    for store in store_latlon:
        csv_row = store
        location_file.writerow(csv_row)
    csv_file.close()

with open('error.txt', 'w') as txt_file:
    txt_file.writelines(errors)
    txt_file.close()
