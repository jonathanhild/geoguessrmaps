#! ./env/bin/python3

import os
import json
import csv

import requests


os.chdir('./benson_bubblers')

r = requests.get(
    'https://opendata.arcgis.com/datasets/070f61b58ac646b0aaf2a223b2dd16fa_84.geojson')
bubblers_json = r.json()
with open('bubbler_data.json', 'w') as file:
    json.dump(bubblers_json, file)
    file.close()


bubbler_list = []
for bubbler in bubblers_json['features']:
    bubbler_list.append(
        (bubbler['geometry']['coordinates'][1],
         bubbler['geometry']['coordinates'][0]))

with open('bubbler_locations.csv', 'w') as csv_file:
    location_file = csv.writer(csv_file)
    location_file.writerows(bubbler_list)
    csv_file.close()
