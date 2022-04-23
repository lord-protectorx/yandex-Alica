import random

spis_word = ["Горилла", "Человек", "Время", "Жизнь", "Вопрос", "Ребенок", "Конец", "Система", "Начало"]
sims = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф',
        'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
word = random.choice(spis_word)
finish = True
used_sims = []
kolvo = 0


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


print('Я загадала слово, можем начинать. Чтобы завершить, напишите "я сдаюсь"')
frm = "".ljust(len(word), "_")
while finish:
    sim = input()
    if sim.lower() == 'я сдаюсь':
        print(f"Жаль...:( Я загадывала слово '{word}'")
        finish = False
    elif sim.lower() == word.lower():
        print("Поздравляю!! Ты угадал слово. Получи подарок - 🎁")
        finish = False

    elif sim in used_sims:
        print("Вы уже использовали этот символ")
    elif sim.lower() in sims:
        if sim.lower() in word.lower():
            kolvo = 0
            spis = num_sims(word, sim.lower())
            frm = vis(frm, spis, sim)
            used_sims.append(sim.lower())
            if "_" not in frm:
                print(f"Поздравляю!! Я загадывала слово '{word}' Получи подарок - 🎁")
                finish = False
            else:
                print(frm)
        else:
            if kolvo == 3:
                print(f"Вы пробовали слишком много раз :) Я загадывала слово '{word}'.")
                finish = False
            else:
                used_sims.append(sim.lower())
                kolvo += 1
                print("Этой буквы нет в слове :( Попробуйте еще раз ")

    else:
        print('ОШИБКА!! Введите ОДНУ букву на кирилице')
