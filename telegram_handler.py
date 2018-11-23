import config
import reddit_handler
import requests
import json
from funcs import get_subreddits
from funcs import decide
from time import sleep as sleep

#######################################
#                                     #
#    THIS FILE IS DEPRECATED AND      #
#   SHOULD NOT BE USED ANY LONGER     #
#                                     #
#######################################


TOKEN = config.token
CLIENT_ID = config.client_id
SECRET = config.secret
USER_AGENT = config.user_agent
MULTI_REDDIT = get_subreddits()


def telegram_bot():

    # This will mark the last update we've checked
    last_update = 0
    # This is the url for communicating with my bot
    url = 'https://api.telegram.org/bot%s/' % TOKEN
    offset = 0

    # Retrieve initial link, title, and subreddit.
    link, title, sub = reddit_handler.get_url(multireddit=MULTI_REDDIT, client_id=CLIENT_ID,
                                              client_secret=SECRET, user_agent=USER_AGENT)

    # This nest is iterated every 3 seconds.
    while True:
        # Get all updates (see offset):
        try:
            get_updates = json.loads(requests.get(url + 'getUpdates?offset=' + str(offset)).content)
        except:
            # TODO: Unknown reason why this is here...
            get_updates = json.loads(requests.get(url + 'getUpdates').content)
        # iterate through each one
        for update in get_updates['result']:
            # First make sure I haven't read this update yet (in case my offset has a problem)
            if last_update < update['update_id']:
                last_update = update['update_id']

                # I've got a new update. If it contains a message:
                if 'message' in update:
                    print("New update:")
                    print(update['update_id'], update['message']['from']['username'])

                    try:
                        if '/meme' in update['message']['text'] \
                                and update['message']['entities'][0]['type'] == 'bot_command' \
                                and update['message']['from']['is_bot'] is False:

                            message = 'r/' + sub + ':' '\n' + title + '\n' + link

                            # Send message.
                            requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'],
                                                                          text=message))
                            print("Link sent.")
                            # Get new link now instead of as a response to a request.
                            link, title, sub = reddit_handler.get_url(multireddit=MULTI_REDDIT, client_id=CLIENT_ID,
                                                                      client_secret=SECRET, user_agent=USER_AGENT)

                        # Make decision
                        elif '/help' in update['message']['text'] \
                                and update['message']['from']['is_bot'] is False:
                            message = decide(update['message']['text'])
                            requests.get(url + 'sendMessage', params=dict(chat_id=update['message']['chat']['id'],
                                                                          text=message))
                            print("Made decision.")

                    # for updates that don't contain text - like from being added to groups
                    except KeyError:
                        pass

                    # New offset to make room for new updates
                    offset = update['update_id'] + 1
                    print()     # for console

        # Let's wait a few seconds for new updates - we don't want to fry Telegram servers
        sleep(3)
