from flask import Flask
from flask import request
import json

app = Flask(__name__)


@app.route('/post', methods=['POST'])
# в учебнике есть эта часть
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(resp, reqst):
    # проверка что это не первое сообщение
    if reqst['request']['original_utterance']:
        resp['response']['text'] = reqst['request']['original_utterance']
    else:
        # если сообщений до этого не было
        resp['response']['text'] = "Привет! Я эхо-bot"


if __name__ == '__main__':
    app.run()
