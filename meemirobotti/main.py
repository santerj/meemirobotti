import sys; sys.path.insert(0, './')

import envtoml
import time

import requests

from model import telegram
from .command import misc

from loguru import logger
from flask import Flask, request, Response
app = Flask(__name__)
conf = envtoml.load(open('config/config.toml'))

TG_TOKEN = conf['telegram']['token']


def parse_command(update: telegram.Update) -> str:
    message = update.edited_message if update.edited_message else update.message
    print(message)

    if message.entities:
        for entity in message.entities:
            if entity.type == 'bot_command':
                offset = entity.offset
                length = entity.length
                command = message.text[offset : (offset+length)]  # extract command
                if (pos := command.find('@')) != -1:
                    command = command[:pos]  # remove trailing bot name
                return command
        else: return ''
    else: return ''

def send_message(update: telegram.Update, message: str) -> Response:
    logger.info(message)
    if message in ('', None):
        # return early when content ends up empty
        return Response('success', 200)

    url = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage'
    payload = {
        'chat_id': update.message.chat.id,
        'text': message
    }

    r = requests.post(url, json=payload, timeout=3)
    if r.status_code == 200:
        return Response('success', 200)
    else:
        return Response('error', 500)

@app.route('/', methods=['POST'])
def post():
    if request.method == 'POST':

        # deserialize payload to Pydantic
        update = telegram.Update(**request.get_json())
        now = time.time()
        # TODO: discard stale requests

        command = parse_command(update)
        logger.info(f'{command} from @{update.edited_message.from_.username
                                      if update.edited_message
                                      else update.message.from_.username}')

        # main "router"
        match command:
            case '/uwu':
                message = misc.uwu(update)
                return send_message(update, message)

            case '/help':
                message = misc.help(update)
                return send_message(update, message)
            
            case _:
                # unregistered command
                return send_message(update, None)
