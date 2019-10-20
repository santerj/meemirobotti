#!/usr/bin/env python

from time import sleep

from Bot import Bot

import logging

def main():

    tg = Bot()
    logging.basicConfig(filename='app.log')

    while True:
        try:
            tg.get_updates()
        except:
            logging.exception("nurin meni", exc_info=True)
            pass
        finally:
            sleep(1.5)


if __name__ == "__main__":
    main()
