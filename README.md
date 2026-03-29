# meemirobotti

# Getting started

## Prerequisites

This project requires `Python 3.12`+.

For local testing, you can use [ngrok](https://ngrok.com/)

1. Start ngrok

    ngrok http http://localhost:8000

2. Set webhook URL for Telegram

    ```
    export TG_TOKEN=yourtoken
    export NGROK_URL=yoururl

    curl "https://api.telegram.org/bot$TG_TOKEN/setWebhook?url=$NGROK_URL/bot"
    ```

3. Start unvicorn server

    uvicorn meemirobotti.main:app --host 0.0.0.0 --port 8000 --reload


## Installation

Tasks for unit testing, linting, security auditing etc. are included in the `noxfile.py`. Try to invoke it with

    nox

If you don't have nox installed globally, just use the one included in the virtual environment:

    dev-venv/bin/nox
