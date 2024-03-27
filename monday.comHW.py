# -*- coding: utf-8 -*-
"""monday.comHW.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QqkNd51yuX-umHR1qxV8XxU6ve3MuzwJ
"""

import requests
import csv

url = "https://images-api.nasa.gov/search"

params = {
    'q': 'Ilan Ramon'
}

# Send GET request to the NASA API
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    results = []

    # Iterate over the items in the response
    for item in data['collection']['items']:
        # Check if the item is an image and its size is larger than 1000 KB
        if item['data'][0]['media_type'] == 'image':
            image_url = item['links'][0]['href'].replace("thumb", "orig")
            image_response = requests.get(image_url, stream=True)
            image_size_kb = int(image_response.headers.get('content-length', 0)) / 1024
            # print(image_size_kb)
            if image_size_kb > 1000:
                results.append({
                    'Nasa_id': item['data'][0]['nasa_id'],
                    'kb': image_size_kb
                })
    # print(str(results))
    # Write results to a CSV file
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = ['Nasa_id', 'kb']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for result in results:
            writer.writerow(result)
else:
    print(f"Failed to get data from NASA API. Status code: {response.status_code}")