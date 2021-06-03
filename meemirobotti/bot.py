import typing
import configparser
import time

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

        updater = Updater(token=self.token, use_context=True)
        dispatcher = updater.dispatcher

        self.commands = {
            "meme": self.send_meme
        }

        for cmd, callback in self.commands.items():
            dispatcher.add_handler(PrefixHandler(['/'], cmd, callback))
            dispatcher.add_handler(CommandHandler(cmd, callback))

        dispatcher.job_queue.run_repeating(callback=self.refresh_cache, interval=4, first=5)
        updater.start_polling()
        updater.idle()
 
    def refresh_cache(self, update: Update) -> None:
        print("refresh_cache")
        if len(self.meme_cache) < 20:
            start = time.time()
            meme = self.redditor.get_meme(legacy=True)
            self.meme_cache.append(meme)
            end = time.time()
            print(f"refreshed in: {end-start}")

    def send_meme(self, update: Update, context: CallbackContext) -> None:

        if len(self.meme_cache) > 0:
            print("cache hit!", len(self.meme_cache))
            meme = self.meme_cache[0]
            self.meme_cache = self.meme_cache[1:]
        else:
            print("worst case scenario")
            meme = self.redditor.get_meme()

        context.bot.send_message(chat_id=update.message.chat_id, text=
            f"r/{meme.sub}:\n{meme.title}\n{meme.url}"
        )

if __name__ == '__main__':
    Bot()
