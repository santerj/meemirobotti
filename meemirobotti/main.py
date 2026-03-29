#import sys; sys.path.insert(0, './')  # fix import issues

import time
from contextlib import asynccontextmanager

import requests
import sentry_sdk
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from meemirobotti.preflight import CONFIG
from meemirobotti.command import bible, meme, misc
from meemirobotti.model import telegram

sentry_sdk.init(
    dsn=CONFIG.ROBOTTI_SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    environment=CONFIG.ROBOTTI_SENTRY_ENV
)

def create_reddit_app():
    redditor = meme.Redditor(
        client_id=CONFIG.ROBOTTI_REDDIT_CLIENT_ID,
        secret=CONFIG.ROBOTTI_REDDIT_SECRET,
        user_agent=CONFIG.ROBOTTI_REDDIT_USER_AGENT,
        queue_size=CONFIG.ROBOTTI_REDDIT_QUEUE_SIZE
    )
    logger.success('🟢 Redditor started!')
    return redditor

redditor = create_reddit_app()

def refresh_meme_queue():
    redditor.refresh_queue()


TG_TOKEN = CONFIG.ROBOTTI_TG_TOKEN


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

async def send_message(update: telegram.Update, message: str) -> Response:
    logger.debug(message)
    if message in ('', None):
        # return early when content ends up empty
        return Response('success', 200)

    url = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage'
    payload = {
        'chat_id': update.message.chat.id,
        'text': message
    }

    import asyncio
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, lambda: requests.post(url, json=payload, timeout=3))
    if r.status_code == 200:
        logger.info('Sent response')
        return Response('success', 200)
    else:
        logger.error('Failed sending response')
        return Response('error', 500)

async def send_image() -> Response:
    # TODO...
    pass

async def bot_handler(request: Request):
    if request.method == 'POST':
        # deserialize payload to Pydantic
        update_data = await request.json()
        update = telegram.Update(**update_data)
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
                return await send_message(update, message)

            case '/help':
                message = misc.help(update)
                return await send_message(update, message)
            
            case '/meme':
                message = redditor.get_meme()
                return await send_message(update, message)
            
            case '/bible':
                message = bible.bible(update)
                return await send_message(update, message)
            
            case '/raamattu':
                message = bible.raamattu(update)
                return await send_message(update, message)

            case _:
                # unregistered command
                return await send_message(update, None)

async def health_handler(request: Request):
    return Response('ok', 200)

routes = [
    Route('/bot', bot_handler, methods=['POST']),
    Route('/health', health_handler, methods=['GET']),
]

# setup apscheduler
scheduler = AsyncIOScheduler()
scheduler.add_job(refresh_meme_queue, 'interval', minutes=5, misfire_grace_time=30)

@asynccontextmanager
async def lifespan(app):
    # startup
    scheduler.start()
    yield
    # shutdown
    await scheduler.shutdown()

app = Starlette(routes=routes, lifespan=lifespan)
