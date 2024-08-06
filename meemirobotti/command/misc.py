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
            return 'UwU'
    
def help(update: telegram.Update) -> str:
    logger.info(update)
    if update.message.reply_to_message:
        text = update.message.reply_to_message.text
    elif update.message.text:
        text = update.message.text
    else:
        text = ''

    choiceDelimiter = " vai "

    if text == '':
        helptext = "/help: Valitse usean vaihtoehdon välillä käyttämällä sanaa \"vai\". Jos haluat joo/ei päätöksen, päätä viesti kysymysmerkkiin (?)"
        return helptext

    # string has choice delimiter
    elif text.find(choiceDelimiter) != -1:
        parts = text.split(choiceDelimiter)
        return random.choice(parts)

    # question mark terminator
    elif text[-1] == "?":
        return random.choice(("Joo", "Ei"))

    else:
        return "En tiedä"
