from flask import Flask
from flask import request
import json
import random


app = Flask(__name__)

# данные для игры
spis_word = ["Горилла", "Человек", "Время", "Жизнь", "Вопрос", "Ребенок", "Конец", "Система", "Начало"]
sims = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
        'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
word = random.choice(spis_word)
finish = True
used_sims = []
kolvo = 0


@app.route('/post', methods=['POST'])
def handler():

    with open('file.json', 'w') as file:
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

def handle_dialog(resp, reqst, context=True):
    # проверка, что это не первое сообщение
    if reqst['request']['original_utterance']:
        resp['response']['text'] = game()
        if context is False:
            resp['response']['end_session'] = True
    else:
        # если сообщений до этого не было
        resp['response']['text'] = 'Привет! Давай сыграем в виселицу с городами.' \
                                   'Я загадал слово, можем начинать. Чтобы завершить, напишите "я сдаюсь"'


def game():
    # долбаные глобалы
    global finish, kolvo

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

    frm = "".ljust(len(word), "_")
    while finish:
        sim = request.json["request"]["command"]
        if sim.lower() == 'я сдаюсь':
            finish = False
            return (f"Жаль...:( Я загадывала слово '{word}'", False)

        elif sim.lower() == word.lower():
            finish = False
            return ("Поздравляю!! Ты угадал слово. Получи подарок - 🎁", False)

        elif sim in used_sims:
            return "Вы уже использовали этот символ"
        elif sim.lower() in sims:
            if sim.lower() in word.lower():
                kolvo = 0
                spis = num_sims(word, sim.lower())
                frm = vis(frm, spis, sim)
                used_sims.append(sim.lower())
                if "_" not in frm:
                    finish = False
                    return (f"Поздравляю!! Я загадывала слово '{word}' Получи подарок - 🎁", False)

                else:
                    return (frm)
            else:
                if kolvo == 3:
                    finish = False
                    return (f"Вы пробовали слишком много раз :) Я загадывала слово '{word}'.", False)

                else:
                    used_sims.append(sim.lower())
                    kolvo += 1
                    return ("Этой буквы нет в слове :( Попробуйте еще раз ")

        else:
            return ('ОШИБКА!! Введите ОДНУ букву на кирилице')




if __name__ == '__main__':
    app.run()
