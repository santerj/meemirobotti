import json
from socket import gaierror
from time import time

import requests

import config
import funcs
import reddit_handler

TOKEN = config.token
CLIENT_ID = config.client_id
SECRET = config.secret
USER_AGENT = config.user_agent
ADMIN_ID = config.admin_id


class Bot:

    def __init__(self):

        self.__url = 'https://api.telegram.org/bot%s/' % TOKEN
        self.__multireddit = funcs.get_subreddits()
        self.__offset = 0
        self.__last_update = 0

        # stats
        self.__start_time = time()
        self.__memes_sent = 0
        self.__help_sent = 0
        self.__translations = 0

        # meme
        self.__link = ""
        self.__title = ""
        self.__sub = ""
        self.new_meme()

        # for admin tools
        self.__admin_id = ADMIN_ID

    def get_updates(self):

        try:
            updates = json.loads(requests.get(self.__url + 'getUpdates?offset=' + str(self.__offset)).content)
        except gaierror:
            updates = json.loads(requests.get(self.__url + 'getUpdates').content)

        for update in updates['result']:

            # Refresh this
            if self.__last_update < update['update_id']:
                self.__last_update = update['update_id']

            try:
                # Don't process old updates.
                if time() - update['message']['date'] < 10:
                    self.process_update(update)

            # Some updates don't contain 'message'.
            except KeyError:
                pass

            # New offset to automatically clear the queue at tg server-side
            self.__offset = update['update_id'] + 1

    def send_message(self, update, message):

        chat_id = update['message']['chat']['id']
        requests.get(self.__url + 'sendMessage', params=dict(chat_id=chat_id, text=message))

    def process_update(self, update):

        # A command interpreter of sorts - all used Telegram bot commands should be specified here

        if update['message']['entities'][0]['type'] != 'bot_command':
            # only process messages that begin with /
            pass

        elif '/meme' in update['message']['text']:
            self.send_meme(update)
            self.__memes_sent += 1

        elif '/help' in update['message']['text']:
            self.send_help(update)
            self.__help_sent += 1

        elif '/stats' in update['message']['text']:
            self.stats(update)

        elif '/wappuun' in update['message']['text']:
            self.wappu(update)

        elif '/kaannos' in update['message']['text']:
            if 'reply_to_message' in update['message'].keys():
                self.translate(update)
                self.__translations += 1
            else:
                message = '/kaannos: vastaa johonkin viestiin komennolla ' \
                          '/kaannos. Ei toimi muiden bottien viesteihin.'
                self.send_message(update, message)

    #                                  method bodies defined below.

    def send_meme(self, update):

        if update['message']['entities'][0]['type'] == 'bot_command':

            message = 'r/' + self.__sub + ':' '\n' + self.__title + '\n' + self.__link
            self.send_message(update, message)
            # Refresh meme
            self.new_meme()

    def send_help(self, update):

        if update['message']['from']['is_bot'] is False:
            message = funcs.decide(update['message']['text'])
            self.send_message(update, message)

    def new_meme(self):
        # Refresh the meme
        try:
            self.__link, self.__title, self.__sub = reddit_handler.get_url(
                multireddit=self.__multireddit, client_id=CLIENT_ID, client_secret=SECRET, user_agent=USER_AGENT
            )
        except TypeError:
            self.new_meme()

    def stats(self, update):

        message = funcs.uptime(time() - self.__start_time)
        message = message + str(self.__memes_sent) + " memes sent \n" + \
            str(self.__help_sent) + " helps sent \n" + \
            str(self.__translations) + " translations"

        self.send_message(update, message)

    def translate(self, update):

        message = funcs.scramble(update['message']['reply_to_message']['text'])
        self.send_message(update, message)

    def wappu(self, update):

        tampin_paljastuspaiva_2019 = 1555452000
        message = funcs.time_until(tampin_paljastuspaiva_2019)
        self.send_message(update, message)
