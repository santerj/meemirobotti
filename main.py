#!/usr/bin/env python

from time import sleep

from Bot import Bot

from requests.exceptions import ConnectionError


def main():
    tg = Bot()

    while True:
        try:
            tg.get_updates()
            sleep(1.5)
        except ConnectionError:
            sleep(5)
            main()


if __name__ == "__main__":
    main()
