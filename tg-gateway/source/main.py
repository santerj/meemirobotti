import re
import typing

from os import getenv

import requests

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext
from telegram import TelegramError, Update, Message, MessageEntity


def botCommand2ApiCall(message: Message) -> requests.Response:
    """
    Translation layer that turns TG bot commands to
    HTTP requests
    """
    backendHost = "http://python-api:80"

    for entity in message.entities:
        if entity.type == MessageEntity.BOT_COMMAND:
            command = message.parse_entity(entity)
    
    # regex out trailing bot slugs (/command@bot_name)
    m = re.match(pattern="^/[^@]*", string=command)
    method = m.group(0)

    match method:
        
        case "/help":
            text = message.text[len(command)+1:]
            call = f"{backendHost}{method}?text={text}"
            return requests.get(call)

        case "/kaannos":
            if not message.reply_to_message:
                text = ""
            else:
                if message.reply_to_message.text:
                    text = message.reply_to_message.text
                    option = message.text[len(command)+1:]
                elif message.reply_to_message.caption:
                    text = message.reply_to_message.caption
                    option = message.text[len(command)+1:]
                else:  # reply to a photo without caption
                    text = ""

            try:
                option = int(option)
                optionalArgument = f"&level={option}"
            except ValueError:
                text = ""
                optionalArgument = ""
            except UnboundLocalError:
                optionalArgument = ""

            call = f"{backendHost}{method}?text={text}{optionalArgument}"
            return requests.get(call)

        case "/uwu":
            if not message.reply_to_message:
                text = ""
            else:
                if message.reply_to_message.text:
                    text = message.reply_to_message.text
                elif message.reply_to_message.caption:
                    text = message.reply_to_message.caption
                else:  # reply to a photo without caption
                    text = ""

            call = f"{backendHost}{method}?text={text}"
            return requests.get(call)
        
        case _:
            call = f"{backendHost}{method}"
            return requests.get(call)

def commandProcessor(update: Update, context: CallbackContext):
    req = botCommand2ApiCall(update.message)

    if req.status_code != 200:
        sendError(update=update, context=context, errorCode=req.status_code)
    else:
        resp = req.text
        context.bot.send_message(chat_id=update.message.chat_id, text=resp)

def sendError(update: Update, context: CallbackContext, errorCode: int = 500):
    errorImageLinks = {
        404: "https://imgur.com/TkThb0y",
        500: "https://imgur.com/lozVeMH"
    }
    if errorCode not in errorImageLinks.keys():
        link = errorImageLinks[500]
    else:
        link = errorImageLinks[errorCode]
    context.bot.send_photo(chat_id=update.message.chat_id, photo=link)

def main() -> None:
    token = getenv("TELEGRAM_TOKEN")
    updater = Updater(token=token, use_context=True)

    dispatcher = updater.dispatcher
    handler = MessageHandler(filters=Filters.command & Filters.text | Filters.reply, callback=commandProcessor)  # filter out media etc
    dispatcher.add_handler(handler)
    #dispatcher.add_error_handler(sendError)
    
    # start bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
