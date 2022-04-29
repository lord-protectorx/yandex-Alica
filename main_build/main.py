from flask import Flask
from flask import request
import random
from main_build.functions import *


app = Flask(__name__)


class GameData:
    def __init__(self):
        # данные для игры
        self.spis_word = collecting_cities_and_countries()
        self.sims = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                     'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
        self.finish = True
        self.used_sims = []
        self.kolvo = 0
        self.sessionStorage = {}
        self.reg_flag = False
        self.user_id = 0


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


def first_name(reqst):
    for entity in reqst['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


def handle_dialog(resp, reqst):
    global default_game_data
    # проверка, что это не первое сообщение
    if reqst['request']['original_utterance'] and default_game_data.reg_flag == True:
        game_result = game()
        resp['response']['text'] = game_result[0]
        if game_result[1] is False:
            resp['response']['end_session'] = True
    else:
        # если сообщений до этого не было
        user_id = reqst['session']['user_id']
        # новый пользователь
        if reqst['session']['new']:
            default_game_data = GameData()
            default_game_data.user_id = user_id
            resp['response']['text'] = 'Привет! Как тебя зовут?'
            default_game_data.sessionStorage[user_id] = {
                'first_name': None
            }
            return
        # не новый пользователь
        if default_game_data.sessionStorage[user_id]['first_name'] is None:
            # в последнем его сообщение ищем имя.
            frs_name = first_name(reqst)
            # если не нашли, то сообщаем пользователю что не расслышали.
            if frs_name is None:
                resp['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
            # если нашли, то приветствуем пользователя.
            else:
                default_game_data.sessionStorage[user_id]['first_name'] = frs_name
                resp['response'][
                    'text'] = 'Приятно познакомиться, ' \
                              + frs_name.title() \
                              + '. Я - Алиса. Давай сыграем в виселицу с городами.' \
                                'Я загадал слово, можем начинать. Чтобы завершить, напишите "я сдаюсь"'
                default_game_data.word = choose_city(default_game_data.user_id)
                default_game_data.frm = "".ljust(len(default_game_data.word), "_")
                default_game_data.name = frs_name.title()
                default_game_data.reg_flag = True


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
            write_user(default_game_data.user_id, default_game_data.word)
            return f"Жаль...:( Я загадывала слово '{default_game_data.word}'", False

        elif sim.lower() == default_game_data.word.lower():
            default_game_data.finish = False
            write_user(default_game_data.user_id, default_game_data.word)
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
                    write_user(default_game_data.user_id, default_game_data.word)
                    return f"Поздравляю!! Я загадывала слово '{default_game_data.word}'", False

                else:
                    return default_game_data.frm, True
            else:
                if default_game_data.kolvo == 3:
                    default_game_data.finish = False
                    write_user(default_game_data.user_id, default_game_data.word)
                    return f"Вы пробовали слишком много раз :) Я загадывала слово '{default_game_data.word}'.", False

                else:
                    default_game_data.used_sims.append(sim.lower())
                    default_game_data.kolvo += 1
                    return "Этой буквы нет в слове :( Попробуйте еще раз ", True

        else:
            return 'ОШИБКА!! Введите ОДНУ букву на кирилице', True


if __name__ == '__main__':
    app.run()
