import sys; sys.path.insert(0, './')  # fix import issues

import time

import envtoml
import requests
from command import meme, misc
from dotenv import load_dotenv
from flask import Flask, Response, request
from flask_apscheduler import APScheduler
from loguru import logger
from model import telegram

load_dotenv()
conf = envtoml.load(open('config/config.toml'))

def create_app():
    c = conf['reddit']
    redditor = meme.Redditor(
        client_id=c['client_id'],
        secret=c['secret'],
        user_agent=c['user_agent'],
        queue_size=c['queue_size']
    )
    app = Flask(__name__, static_folder='static')
    app.config['redditor'] = redditor
    logger.success('🟢 App started!')
    return app

# setup flask and add reference to redditor object
app = create_app()
redditor: meme.Redditor = app.config['redditor']
if __name__ == "__main__":
    # run flask
    app.run()

# setup apscheduler
scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)
scheduler.start()
@scheduler.task('interval', id='refresh_meme_queue', minutes=5, misfire_grace_time=30)
def refresh_meme_queue():
    redditor.refresh_queue()


TG_TOKEN = conf['telegram']['token']


def parse_command(update: telegram.Update) -> str:
    message = update.edited_message if update.edited_message else update.message

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
    logger.debug(message)
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
        logger.info('Sent response')
        return Response('success', 200)
    else:
        logger.error('Failed sending response')
        return Response('error', 500)

def send_image() -> Response:
    # TODO...
    pass

@app.route('/', methods=['POST'])
def bot():
    if request.method == 'POST':

        # deserialize payload to Pydantic
        update = telegram.Update(**request.get_json())
        logger.debug(update.model_dump)
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
            
            case '/meme':
                message = redditor.get_meme()
                return send_message(update, message)
            
            case _:
                # unregistered command
                return send_message(update, None)
