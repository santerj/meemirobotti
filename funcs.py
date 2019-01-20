import config
import praw
import prawcore
import json
import requests
from time import time, sleep
from random import randrange, getrandbits

# file containing the default subreddits
DEFAULT = "default_subreddits.txt"

CLOSEST_SYMBOLS_QWERTY = {

    ' ': ['.', ',', 'b', 'c', 'm', 'n', 'v', 'x'],
    '.': ['', '\n', ' ', 'm', 'n'],
    '/': [',', ')', '9', '0'],
    '@': ['#', '1', '2'],
    '#': ['*', '1', '2', '3', '@', '€'],

    '0': ['+', '0', '8', '9', 'i', 'k', 'l', 'p', 'ö'],
    '1': ['2', 'q', 'w', '§'],
    '2': ['1', '3', 'e', 'q', 'w'],
    '3': ['2', '4', 'e', 'w'],
    '4': ['3', '5', 'e', 'r'],
    '5': ['4', '6', 'r', 't'],
    '6': ['5', '7', 't', 'y'],
    '7': ['6', '8', 'u', 'y'],
    '8': ['7', '9', 'i', 'u'],
    '9': ['0', '8', 'i', 'o'],

    'a': ['q', 's', 'w'],
    'b': [' ', 'g', 'h', 'n', 'v'],
    'c': [' ', 'c', 'd', 'f', 'g', 'x'],
    'd': ['e', 'f', 'r', 's', 'w', 'x', 'z'],
    'e': ['d', 'f', 'r', 's', 'w'],
    'f': ['c', 'd', 'e', 'g', 'r', 't', 'v'],
    'g': ['b', 'f', 'h', 'r', 't', 'v', 'y'],
    'h': ['b', 'g', 'j', 'n', 't', 'u', 'y'],
    'i': ['j', 'k', 'l', 'o', 'u'],
    'j': ['h', 'i', 'k', 'm', 'n', 'u'],
    'k': [',', 'i', 'j', 'l', 'm', 'o'],
    'l': [',', '.', 'k', 'o', 'p', 'ö'],
    'm': [' ', ',', 'j', 'k', 'n'],
    'n': [' ', 'b', 'h', 'j', 'm'],
    'o': ['i', 'k', 'l', 'p', 'ö'],
    'p': ['o', 'ä', 'å', 'ö'],
    'q': ['a', 's', 'w'],
    'r': ['d', 'e', 'f', 'g', 't'],
    's': ['a', 'd', 'e', 'q', 'w', 'x', 'z'],
    't': ['f', 'g', 'h', 'r', 'y'],
    'u': ['h', 'i', 'j', 'k', 'y'],
    'v': [' ', 'b', 'c', 'f', 'g'],
    'w': ['a', 'd', 'e', 'q', 's'],
    'x': [' ', ',', 'c', 'd', 'f', 'g', 's', 'z'],
    'y': ['g', 'h', 'j', 't', 'u'],
    'z': [',', 'd', 'f', 's', 'x'],
    'å': ['p', 'ä', 'ö'],
    'ä': ['', 'p', 'å', 'ö'],
    'ö': ['', '.', 'o', 'p', 'ä', 'å'],

    'A': ['Q', 'S', 'W'],
    'B': [' ', 'G', 'H', 'N', 'V'],
    'C': [' ', 'C', 'D', 'F', 'G', 'X'],
    'D': ['E', 'F', 'R', 'S', 'W', 'X', 'Z'],
    'E': ['D', 'F', 'R', 'S', 'W'],
    'F': ['C', 'D', 'E', 'G', 'R', 'T', 'V'],
    'G': ['B', 'F', 'H', 'R', 'T', 'V', 'Y'],
    'H': ['B', 'G', 'J', 'N', 'T', 'U', 'Y'],
    'I': ['J', 'K', 'L', 'O', 'U'],
    'J': ['H', 'I', 'K', 'M', 'N', 'U'],
    'K': [',', 'I', 'J', 'L', 'M', 'O'],
    'L': [',', '.', 'K', 'O', 'P', 'Ö'],
    'M': [' ', ',', 'J', 'K', 'N'],
    'N': [' ', 'B', 'H', 'J', 'M'],
    'O': ['I', 'K', 'L', 'P', 'Ö'],
    'P': ['L', 'O', 'Ä', 'Å', 'Ö'],
    'Q': ['A', 'S', 'W'],
    'R': ['D', 'E', 'F', 'G', 'T'],
    'S': ['A', 'D', 'E', 'Q', 'W', 'X', 'Z'],
    'T': ['F', 'G', 'H', 'R', 'Y'],
    'U': ['H', 'I', 'J', 'K', 'Y'],
    'V': [' ', 'B', 'C', 'F', 'G'],
    'W': ['A', 'D', 'E', 'Q', 'S'],
    'X': [' ', ',', 'C', 'D', 'F', 'G', 'S', 'Z'],
    'Y': ['G', 'H', 'J', 'T', 'U'],
    'Z': [',', 'D', 'F', 'S', 'X'],
    'Å': ['P', 'Ä', 'Ö'],
    'Ä': ['', 'P', 'Å', 'Ö'],
    'Ö': ['', '.', 'L', 'O', 'P', 'Ä', 'Å']

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
        # 0 or 1
        rnd = getrandbits(1)
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

        if text[i] not in CLOSEST_SYMBOLS_QWERTY.keys():
            # Current character is something like an emoji or something
            char = text[i]

        else:
            # Every n character on average will be misclicked (value from testing).
            # People capable of typing longer messages are typically less likely
            # to be super intoxicated.
            if len(text) < 50:
                chance = randrange(13)
            else:
                chance = randrange(23)

            if chance == 0:
                typos = CLOSEST_SYMBOLS_QWERTY[text[i]]
                rnd = randrange(len(typos))
                char = typos[rnd]
            else:
                char = text[i]

        scrambled_text += char

    if scrambled_text == text:
        # Recursion to avoid cases where no characters were changed (somewhat volatile)
        scrambled_text = scramble(text)

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
