import json
import typing
import requests

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from telegram import TelegramError, Update, Message, MessageEntity


def botCommand2ApiCall(message: Message) -> str:
    """
    Translation layer that turns TG bot commands to
    HTTP GET requests
    TODO: migrate to json payload by default
    """
    backendHost = "http://python-api:80"

    if message.entities:
        for entity in message.entities:
            if entity.type == MessageEntity.BOT_COMMAND:
                command = message.parse_entity(entity)
    else:
        return

    method = command[1:]  # remove leading slash /
    method = method.split("@", 1)[0]  # remove possible bot slug

    if message.reply_to_message:
        if message.reply_to_message.text:
            content = message.reply_to_message.text
            modifier = message.text[len(command)+1:]
        elif message.reply_to_message.caption:
            content = message.reply_to_message.caption
            modifier = message.text[len(command)+1:]
    elif message.text:
        content = message.text[len(command)+1:]  # remove command + space
        modifier = ""

    if modifier != "":
        call = f"{backendHost}/{method}?content={content}&modifier={modifier}"
    else:
        call = f"{backendHost}/{method}?content={content}"
    return call

def commandProcessor(update: Update, context: CallbackContext):
    call = botCommand2ApiCall(update.message)
    r = requests.get(call)
    if r.status_code != 200:
        resp = "Täh!"
    else:
        resp = r.text
    context.bot.send_message(chat_id=update.message.chat_id, text=resp)

def main() -> None:
    token = ""  # replace with env var
    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher
    handler = MessageHandler(filters=Filters.command & Filters.text | Filters.reply, callback=commandProcessor)  # filter out media etc
    dispatcher.add_handler(handler)
    
    # start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
