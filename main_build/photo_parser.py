import requests
from functions import collecting_cities_and_countries

cities = list(collecting_cities_and_countries().keys())
api_server = "http://static-maps.yandex.ru/1.x/"
geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'

for city in cities:
    params = {
        'apikey': "40d1649f-0493-4b70-98ba-98533de7710b",
        'geocode': city,
        'format': 'json'
    }
    response = requests.get(geocoder_api_server, params=params).json()

    if not response:
        print('Ошибка в геокодере')
        break
    else:
        toponym = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']
        toponym_coordinates = toponym['Point']['pos'].split()


    lon, lat = toponym_coordinates
    params = {
        "ll": ",".join([lon, lat]),
        "z": 11,
        "l": "map",
        "size": '450,300'
    }

    response = requests.get(api_server, params=params)
    if not response:
        print("ошибка в фото")
        break
    with open(f"../data/photos/{city}.png", "wb") as file:
        file.write(response.content)



