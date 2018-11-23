from Bot import Bot


def main():

    tg = Bot()

    while True:
        tg.get_updates()


if __name__ == "__main__":
    main()
