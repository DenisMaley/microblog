import json
import requests
from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    if 'YA_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['YA_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate'
                     '?key={}&lang={}-{}&text={}'.format(
        current_app.config['YA_TRANSLATOR_KEY'], source_language, dest_language, text),
    )
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    response = json.loads(r.content.decode('utf-8-sig'))
    return response['text'][0]
