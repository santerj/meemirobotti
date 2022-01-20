# meemirobotti

This is my first ever programming project. It is a not very serious Telegram bot for me and my friends. I started working on it in 2018 with no programming knowledge and it has sort of evolved over time along with my skills (not to mean it is well-written even today). In 2022 almost the entire app was rewritten into a microservices/modular architecture.

# how to
1. make sure that you have a way to build and run OCI compliant containers. I us `docker` and `docker-compose`.
2. make sure that you have API credentials to Telegram (message @botfather), Reddit and openweathermap
3. clone this repository
4. rename the examples file (`$ mv docker-compose.yml.example docker-compose.yml`) and edit your credentials into the environment variables sections.
5. build and start the app: `$ docker-compose build && docker-compose up`
6. app is now running, try to message your bot!

# tech
There are microservices.

- `tg-gateway`: handles HTTP traffic to and from Telegram servers. It is a translation layer to convert bot commands to internal API calls. Theoretically it can be replicated to upscale traffic troughut (but not practically). It is built with python-telegram-bot.
- `python-api`: Built with FastApi. It is completely decoupled from Telegram bot command model thanks to `tg-gateway`.
- `redditor`: Built with praw. It seeks memes from reddit and puts them into a message queue.
- `redis`: Used to decouple `python-api` and `redditor`. Contains a queue that is fed by `redditor` and consumed by `python-api`.

# other
Don't take the content of this repository too seriously.
