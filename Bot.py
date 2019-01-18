import json
from socket import gaierror
from time import time, sleep

import requests

import config
import funcs
import reddit_handler

TOKEN = config.token
CLIENT_ID = config.client_id
SECRET = config.secret
USER_AGENT = config.user_agent
ADMIN_ID = config.admin_id
SLEEP = 1.5


class Bot:

    def __init__(self):

        self.__url = 'https://api.telegram.org/bot%s/' % TOKEN
        self.__multireddit = funcs.get_subreddits()
        self.__offset = 0
        self.__last_update = 0
        self.__start_time = time()
        self.__memes_sent = 0

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

        # Polling
        sleep(SLEEP)

    def process_update(self, update):

        # A command interpreter of sorts - all used Telegram bot
        # commands should be specified here

        if update['message']['entities'][0]['type'] != 'bot_command':
            # only process messages that begin with /
            pass

        elif '/meme' in update['message']['text']:
            self.send_meme(update)
            self.__memes_sent += 1

        elif '/help' in update['message']['text']:
            self.send_help(update)

        elif '/stats' in update['message']['text']:
            self.stats(update)

        elif update['message']['reply_to_message']:
            if '/kaannos' in update['message']['text']:
                self.translate(update)

    def send_meme(self, update):

        if update['message']['entities'][0]['type'] == 'bot_command' \
                and update['message']['from']['is_bot'] is False:

            message = 'r/' + self.__sub + ':' '\n' + self.__title + '\n' + self.__link
            chat_id = update['message']['chat']['id']
            requests.get(self.__url + 'sendMessage', params=dict(chat_id=chat_id, text=message))
            # Refresh meme
            self.new_meme()

    def send_help(self, update):

        if update['message']['from']['is_bot'] is False:
            message = funcs.decide(update['message']['text'])
            chat_id = update['message']['chat']['id']
            requests.get(self.__url + 'sendMessage', params=dict(chat_id=chat_id, text=message))

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
        message = message + str(self.__memes_sent) + " memes sent \n"
        chat_id = update['message']['chat']['id']
        requests.get(self.__url + 'sendMessage', params=dict(chat_id=chat_id, text=message))

    def translate(self, update):
        message = funcs.scramble(update['message']['reply_to_message']['text'])
        chat_id = update['message']['chat']['id']
        requests.get(self.__url + 'sendMessage', params=dict(chat_id=chat_id, text=message))
