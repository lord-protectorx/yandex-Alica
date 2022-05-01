import json
from functions import collecting_cities_and_countries

data = collecting_cities_and_countries()
sorted_data = {}
for key in list(reversed(sorted((list(data.keys()))))):
    print(key)
    sorted_data[key] = 1

with open(f"../data/keys of photos.json", 'w', encoding='utf8') as file:
    json.dump(sorted_data, file, ensure_ascii=False)