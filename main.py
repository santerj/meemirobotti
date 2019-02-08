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
            sleep(10)


if __name__ == "__main__":
    main()
