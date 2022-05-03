import json
import random


def collecting_cities_and_countries():
    dic = {}
    deleting_list = []

    with open("../Storehouse/raw list of cities and countries.txt", encoding='utf8') as file:
        text = file.readlines()
        text = [j.split('\t') for j in [i.split('\n')[0] for i in text]]

    for i in range(len(text)):
        dic[text[i][1]] = text[i][0]

    for key, value in dic.items():
        need_to_delete = False
        for i in key:
            if i == '-':
                need_to_delete = True
        for j in value:
            if j == '-':
                need_to_delete = True
        if need_to_delete is True:
            deleting_list.append(key)

    for i in deleting_list:
        del dic[i]

    return dic


def write_user(user_name, town):
    flag = False
    new_data = {'name': user_name, 'towns': [town]}
    try:
        data = json.load(open('users.json'))
    except:
        data = []
    for dict_ in data:
        if dict_['name'] == user_name:
            dict_['towns'].append(town)
            flag = True
    if not flag:
        data.append(new_data)
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def choose_city(user_id):
    find = False
    spis_word = collecting_cities_and_countries()
    try:
        data = json.load(open('users.json'))
        for dict_ in data:
            if dict_['name'] == user_id:
                used_towns = dict_['towns']
                flag = True
                while flag:
                    word = random.choice(list(spis_word.keys()))
                    if word not in used_towns:
                        flag = False
                        return word
    except:
        word = random.choice(list(spis_word.keys()))
        return word

def finding_photo_id(city_name):
    with open('../data/keys of photos.json', 'r', encoding='utf8') as file:
        id = json.load(file)
        return id[city_name]
