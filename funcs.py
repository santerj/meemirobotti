import config
import praw
import prawcore
import json
import requests
from time import time, sleep
from random import randrange, getrandbits

# file containing the default subreddits
DEFAULT = "default_subreddits.txt"
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
            'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
            'y', 'z', 'å', 'ä', 'ö', '0', '3', '7',
            '8', '9', ' ', ',', '']

CLOSEST_SYMBOLS_QWERTY = {
    'a': ['q', 's', 'w'],
    'b': [' ', 'g', 'h', 'n', 'v'],
    'c': [' ', 'c', 'd', 'f', 'g', 'x'],
    'd': ['e', 'f', 'r', 's', 'w', 'x', 'z'],
    'e': ['2', '3', '4', 'd', 'f', 'r', 's', 'w'],
    'f': ['c', 'd', 'e', 'g', 'r', 't', 'v'],
    'g': ['b', 'f', 'h', 'r', 't', 'v', 'y'],
    'h': ['b', 'g', 'j', 'n', 't', 'u', 'y'],
    'i': ['8', '9', 'j', 'k', 'l', 'o', 'u'],
    'j': ['h', 'i', 'k', 'm', 'n', 'u'],
    'k': [',', 'i', 'j', 'l', 'm', 'o'],
    'l': [',', '.', 'k', 'o', 'p', 'ö'],
    'm': [' ', ',', 'j', 'k', 'n'],
    'n': [' ', 'b', 'h', 'j', 'm'],
    'o': ['0', '9', 'i', 'k', 'l', 'p', 'ö'],
    'p': ['+', '0', 'l', 'o', 'ä', 'å', 'ö'],
    'q': ['1', '2', 'a', 's', 'w'],
    'r': ['4', '5', 'd', 'e', 'f', 'g', 't'],
    's': ['a', 'd', 'e', 'q', 'w', 'x', 'z'],
    't': ['5', '6', 'f', 'g', 'h', 'r', 'y'],
    'u': ['7', '8', 'h', 'i', 'j', 'k', 'y'],
    'v': [' ', 'b', 'c', 'f', 'g'],
    'w': ['2', '3', 'a', 'd', 'e', 'q', 's'],
    'x': [' ', ',', 'c', 'd', 'f', 'g', 's', 'z'],
    'y': ['6', '7', 'g', 'h', 'j', 't', 'u'],
    'z': [',', 'd', 'f', 's', 'x'],
    'å': ['+', 'p', 'ä', 'ö'],
    'ä': ['', 'p', 'å', 'ö'],
    'ö': ['', '-', '.', 'l', 'o', 'p', 'ä', 'å']

    }


def error_message():
    input("Press any key...")
    exit(1)


def get_subreddits():

    subs = []
    file = open(DEFAULT)
    for line in file:
        if '*' not in line:
            # lines containing * will not be included
            subs.append(line.rstrip('\n'))
    file.close()
    return subs


def test_subreddit_validity(sub):

    # used for startup and routine checks.
    # not 100% sure about ResponseException here.

    client_id = config.client_id
    secret = config.secret
    user_agent = config.user_agent

    reddit = praw.Reddit(client_id=client_id, client_secret=secret, user_agent=user_agent)

    try:
        test_sub = reddit.subreddit(sub)
        # this line does the actual check, posts is not supposed to be used anymore
        posts = [post for post in test_sub.hot(limit=1)]
        return True

    except prawcore.exceptions.Redirect:
        print("Error: subreddit not accessible:", sub)
        return False

    except prawcore.exceptions.ResponseException:
        print("Error: 401 response from reddit")
        return False


def startup():

    print("Starting up...")

    token = config.token
    subs = get_subreddits()
    subs_to_be_removed = []

    print("Accessing reddit...")
    for sub in subs:

        flag = test_subreddit_validity(sub)
        if not flag:
            subs_to_be_removed.append(sub)

        sleep(1)

    print("Accessing telegram...")
    url = 'https://api.telegram.org/bot%s/' % token
    tg_test = json.loads(requests.get(url + 'getUpdates').content)

    if tg_test['ok'] is False:
        print("Error:", tg_test['error_code'], tg_test['description'])
        error_message()

    print("Done!\n")


def decide(msg):

    separator = "vai "
    command = "/help"

    if msg[-1] == '?':
        rnd = getrandbits(1) # 0 or 1
        if rnd:
            return "Joo"
        else:
            return "Ei"

    if separator not in msg:
        return "/help: Käytä avainsanaa \"vai\" tai päätä viesti kysymysmerkkiin"

    # TODO: better handling of empty fields

    index = msg.find(command)
    beginning = msg[:index]
    msg = msg.replace(beginning, "")

    msg = msg.replace(command, "")
    choices = msg.split(separator)
    choices = [word for word in choices if word not in ["", " "]]
    choices = [word.strip(" ") for word in choices]
    rnd = randrange(0, len(choices))
    return beginning + choices[rnd]


def uptime(timestamp):

    days = int(timestamp // 86400)
    timestamp = timestamp - (days * 86400)
    hours = int(timestamp // 3600)
    timestamp = timestamp - (hours * 3600)
    minutes = int(timestamp // 60)
    timestamp = timestamp - (minutes * 60)
    seconds = int(timestamp)

    message = f"Current uptime:\n" \
              f"{days} days\n" \
              f"{hours} hours\n" \
              f"{minutes} minutes\n" \
              f"{seconds} seconds\n\n"

    return message


def scramble(text):

    scrambled_text = ''

    for i in range(len(text)):
        chance = randrange(13)
        if chance == 0:
            char = ALPHABET[randrange(len(ALPHABET))]
        else:
            char = text[i]

        scrambled_text = scrambled_text + char

    return scrambled_text


def time_until(timestamp):

    remaining = timestamp - time()

    if remaining < 0:
        message = 'Wappuun on vielä pitkä, pitkä aika.'
        return message

    days = int(remaining // 86400)
    remaining = remaining - (days * 86400)
    hours = int(remaining // 3600)
    remaining = remaining - (hours * 3600)
    minutes = int(remaining // 60)
    remaining = remaining - (minutes * 60)
    seconds = int(remaining)

    message = f"{days} päivää, {hours} tuntia, {minutes} minuuttia ja {seconds} sekuntia."
    return message
