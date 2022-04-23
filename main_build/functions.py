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
