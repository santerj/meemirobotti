import typing
import configparser
import time
import re
import random

from classes import Meme
from reddit import Redditor
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, PrefixHandler, CallbackContext
from telegram import TelegramError, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

# TODO: check imports for unused classes and methods

class Bot:

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config')
        self.token = config['telegram']['bot_token']
        self.redditor = Redditor()
        self.meme_cache = []
        self.meme_cache_len = 35

        updater = Updater(token=self.token, use_context=True)
        dispatcher = updater.dispatcher

        self.commands = {
            "meemi": self.send_meme,
            "uwu": self.uwu
        }

        for cmd, callback in self.commands.items():
            dispatcher.add_handler(PrefixHandler(['/'], cmd, callback))
            dispatcher.add_handler(CommandHandler(cmd, callback))

        dispatcher.job_queue.run_repeating(callback=self.refresh_cache, interval=20, first=1)
        updater.start_polling()
        updater.idle()
 
    def refresh_cache(self, update: Update) -> None:
        memes = self.redditor.get_memes(
            amount=self.meme_cache_len
        )
        self.meme_cache = memes

    def send_meme(self, update: Update, context: CallbackContext) -> None:
        if len(self.meme_cache) > 0:
            # cache hit
            meme = self.meme_cache[0]
            self.meme_cache.pop(0)
        else:
            # cache empty, worst case scenario
            meme = self.redditor.get_meme()

        context.bot.send_message(chat_id=update.message.chat_id, text=
            f"r/{meme.sub}:\n{meme.title}\n{meme.url}"
        )

    def uwu(self, update: Update, context: CallbackContext):
        chance = 35
        suffixes = (
            "uwu",
            "UwU",
            "o_0",
            "ﾟ ✧^w^✧ ﾟ",
            "(´◠ω◠`)",
            "ฅ^•ﻌ•^ฅ",
            "(・_・;)",
            "◖⚆ᴥ⚆◗",
            "(ᵘﻌᵘ)",
            "(◕‿◕✿)",
            "(U ᵕ U❁)",
            "(˯ ᵘ ꒳ ᵘ ˯)",
            "( ｡ᵘ ᵕ ᵘ ｡)",
            "(◡ w ◡)",
            "ʕ •ᴥ•ʔ",
            "▼・ᴥ・▼"
        )
        
        if not update.message.reply_to_message:
            context.bot.send_message(
                chat_id=update.message.chat_id,
                text=random.choice(suffixes)
                )
            return
        
        if update.message.reply_to_message.text:
            s = update.message.reply_to_message.text
        elif update.message.reply_to_message.caption:
            s = update.message.reply_to_message.caption
        else:
            return

        s = re.sub('R', 'W', s)
        s = re.sub('L', 'W', s)
        s = re.sub('r', 'w', s)
        s = re.sub('l', 'w', s)

        words = s.split(" ")
        for i, word in enumerate(words):
            if random.randrange(chance) == 0:
                # add stutter
                l = word[0]
                word = f"{l}-{l.lower()}-{l.lower()}" + word[1:]
                words[i] = word

        s = " ".join(words) + " " + random.choice(suffixes)
        context.bot.send_message(chat_id=update.message.chat_id, text=s)


if __name__ == '__main__':
    Bot()
