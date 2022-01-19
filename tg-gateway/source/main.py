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

    for entity in message.entities:
        if entity.type == MessageEntity.BOT_COMMAND:
            command = message.parse_entity(entity)

    method = command[1:]  # remove leading slash /
    method = method.split("@", 1)[0]  # remove possible bot slug

    if message.reply_to_message:
        # message is reply, try to get payload
        if message.reply_to_message.text:
            content = message.reply_to_message.text
            modifier = message.text[len(command)+1:]
        elif message.reply_to_message.caption:
            content = message.reply_to_message.caption
            modifier = message.text[len(command)+1:]
        else:
            content = ""
            modifier = ""
    
    elif message.text:
        # regular message
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
        sendError(update=update, context=context, errorCode=r.status_code)
    else:
        resp = r.text
        context.bot.send_message(chat_id=update.message.chat_id, text=resp)

def sendError(update: Update, context: CallbackContext, errorCode: int = 500):
    errorImageLinks = {
        404: "https://imgur.com/TkThb0y",
        500: "https://imgur.com/lozVeMH"
    }
    if errorCode not in errorImageLinks.keys():
        link = "https://imgur.com/6Y8hibu"  # generic error
    else:
        link = errorImageLinks[errorCode]
    context.bot.send_photo(chat_id=update.message.chat_id, photo=link)

def main() -> None:
    token = ""  # replace with env var
    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher
    handler = MessageHandler(filters=Filters.command & Filters.text | Filters.reply, callback=commandProcessor)  # filter out media etc
    dispatcher.add_handler(handler)
    dispatcher.add_error_handler(sendError)
    
    # start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
