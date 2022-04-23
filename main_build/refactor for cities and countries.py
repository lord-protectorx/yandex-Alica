import csv


with open("../Storehouse/raw list of cities and countries.txt", encoding='utf8') as file:
    text = file.readlines()
    text = [j.split('\t') for j in [i.split('\n')[0] for i in text]]
    print(text)

with open('../data/list of counties and capitals.csv', mode='w', newline='', encoding='utf8') as csvfile:
    writer = csv.writer(
        csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(text)):
        writer.writerow(text[i])