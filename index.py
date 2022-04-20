def handler(req, context):
    response = {
        'session': req['session'],
        'version': req['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, req)
    return response


def handle_dialog(resp, reqst):
    # проверка что это не первое сообщение
    if reqst['request']['original_utterance']:
        resp['response']['text'] = reqst['request']['original_utterance']
    else:
        # если сообщений до этого не было
        resp['response']['text'] = "Привет! Я эхо-bot"

