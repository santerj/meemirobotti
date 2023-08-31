import re

from os import getenv

from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, CallbackContext
from telegram import Update, Message, MessageEntity

import commands


async def commandProcessor(update: Update, context: CallbackContext):
    message = update.message
    text = message.text

    # parse actual command
    for entity in message.entities:
        if entity.type == MessageEntity.BOT_COMMAND:
            rawCommand = message.parse_entity(entity)
            # regex out trailing bot slugs –– /command@bot_name -> /command
            m = re.match(pattern="^/[^@]*", string=rawCommand)
            command = m.group(0)
            break
    else:
        # no command found in message i.e. a sticker was sent in a reply
        return

    # ---- BOT MESSAGES -> FUNCTION CALLS GO HERE ---- #
    match command:
        case "/help":
            response = await commands.help(text)
        case _:
            # command not known
            pass

    await context.bot.send_message(chat_id=update.message.chat_id, text=response)


if __name__ == "__main__":
    token = getenv("TELEGRAM_TOKEN")
    application = ApplicationBuilder().token(token).build()
    handler = MessageHandler(filters=filters.COMMAND & filters.TEXT | filters.REPLY, callback=commandProcessor)
    application.add_handler(handler)
    application.run_polling()
