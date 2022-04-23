from flask import Flask
from flask import request
import json
import random
from main_build.functions import *


app = Flask(__name__)


class GameData():
    def __init__(self):
        # данные для игры
        self.spis_word = collecting_cities_and_countries()
        self.sims = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                     'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
        self.word = random.choice(list(self.spis_word.keys()))
        self.finish = True
        self.used_sims = []
        self.kolvo = 0
        self.frm = "".ljust(len(self.word), "_")


@app.route('/post', methods=['POST'])
def handler():
    with open('../data/last request.json', 'w') as file:
        json.dump(request.json, file)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    return response


def handle_dialog(resp, reqst):
    global default_game_data
    # проверка, что это не первое сообщение
    if reqst['request']['original_utterance']:
        game_result = game()
        resp['response']['text'] = game_result[0]
        if game_result[1] is False:
            resp['response']['end_session'] = True

    else:
        # если сообщений до этого не было
        resp['response']['text'] = 'Привет! Давай сыграем в виселицу с городами.' \
                                   'Я загадал слово, можем начинать. Чтобы завершить, напишите "я сдаюсь"'

        # создаю объект класса с дефолтными данными в нем
        default_game_data = GameData()
        print(default_game_data.word)


def game():
    global default_game_data

    def num_sims(wordd, simm):
        wordd = wordd.lower()
        number = wordd.count(simm)
        res = []
        sp_word = [a for a in wordd]
        for i in range(number):
            indexx = sp_word.index(simm) + i
            res.append(indexx)
            del sp_word[indexx - i]
        return res

    def vis(form, lis_t, simv):
        form = [a for a in form]
        for i in range(len(lis_t)):
            form[lis_t[i]] = simv
        return ''.join(form)

    while default_game_data.finish:
        sim = request.json["request"]["command"]
        if sim.lower() == 'я сдаюсь':
            default_game_data.finish = False
            return f"Жаль...:( Я загадывала слово '{default_game_data.word}'", False

        elif sim.lower() == default_game_data.word.lower():
            default_game_data.finish = False
            return "Поздравляю!! Ты угадал слово. МОЛОДЕЦ", False

        elif sim in default_game_data.used_sims:
            return "Вы уже использовали этот символ", True
        elif sim.lower() in default_game_data.sims:
            if sim.lower() in default_game_data.word.lower():
                default_game_data.kolvo = 0
                spis = num_sims(default_game_data.word, sim.lower())
                default_game_data.frm = vis(default_game_data.frm, spis, sim)
                default_game_data.used_sims.append(sim.lower())
                if "_" not in default_game_data.frm:
                    default_game_data.finish = False
                    return f"Поздравляю!! Я загадывала слово '{default_game_data.word}'", False

                else:
                    return default_game_data.frm, True
            else:
                if default_game_data.kolvo == 3:
                    default_game_data.finish = False
                    return f"Вы пробовали слишком много раз :) Я загадывала слово '{default_game_data.word}'.", False

                else:
                    default_game_data.used_sims.append(sim.lower())
                    default_game_data.kolvo += 1
                    return "Этой буквы нет в слове :( Попробуйте еще раз ", True

        else:
            return 'ОШИБКА!! Введите ОДНУ букву на кирилице', True


if __name__ == '__main__':
    app.run()
