import typing

from classes import Meme
from reddit import Redditor
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, PrefixHandler, CallbackContext
from telegram import TelegramError, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

# TODO: check imports for unused classes and methods

class TelegramBot:

    def __init__(self) -> None:
        config = configparser.ConfigParser()
        config.read('config')
        self.token = config['telegram']['bot_token']

        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = updater.dispatcher
        self.redditor = Redditor()
        self.meme_cache = []

        self.commands = {
            "meme": self.send_meme
        }

        for cmd, callback in self.commands.items():
            dispatcher.add_handler(PrefixHandler(['/'], cmd, callback))
            dispatcher.add_handler(CommandHandler(cmd, callback))

        dispatcher.job_queue.run_repeating(self.refreshCache, interval=60, first=5)        
        self.updater.start_polling()
 

    def refreshCache(self, update: Update) -> None:
        while len(self.meme_cache) < 15:
            meme = self.redditor.get_meme()
            self.meme_cache.append(meme)

    def send_meme(self, update: Update, context: CallbackContext) -> None:
        if len(self.meme_cache) > 0:
            meme = self.meme_cache[0]
            self.meme_cache = self.meme_cache[1:]
        else:
            meme = self.redditor.get_meme()
        
        context.bot.send_message(chat_id=update.message.chat_id, message=
            f"""r/{meme.sub}:
            {meme.title}
            {meme.link}
            """
        )
