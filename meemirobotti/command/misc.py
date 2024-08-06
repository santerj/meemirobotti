import random

from loguru import logger
from model import telegram
from uwuipy import Uwuipy


def uwu(update: telegram.Update) -> str:
    uwu_ = Uwuipy(action_chance=0, exclamation_chance=0, face_chance=0.1)
    if update.message.reply_to_message:
        return uwu_.uwuify(update.message.reply_to_message.text)
    else:
        try:
            return random.choice(uwu_._Uwuipy__faces)
        except AttributeError:  # above might break
            logger.error(f'Failed getting faces from uwuipy')
            return 'UwU'
    
def help(update: telegram.Update) -> str:
    command_name = '/help'
    logger.debug(update)
    if update.message.reply_to_message:
        text = update.message.reply_to_message.text
    elif update.message.text:
        text = update.message.text
    else:
        text = ''

    text = text.replace(command_name, '')

    choiceDelimiter = " vai "

    if text == '':
        helptext = "/help: Valitse vaihtoehtojen välillä käyttämällä sanaa \"vai\". Muissa tapauksissa saat joo/ei vastauksen"
        return helptext

    # string has choice delimiter
    elif text.find(choiceDelimiter) != -1:
        parts = text.split(choiceDelimiter)
        return random.choice(parts)

    else:
        return random.choice(("Joo", "Ei"))
