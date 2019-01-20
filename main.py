from time import sleep

from Bot import Bot


def main():
    tg = Bot()

    while True:
        tg.get_updates()
        sleep(1.5)


if __name__ == "__main__":
    main()
