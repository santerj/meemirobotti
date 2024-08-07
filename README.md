# meemirobotti

# Getting started

## Prerequisites

This project requires `Python 3.12`.

For local testing, you can use [ngrok](https://ngrok.com/)

1. Start ngrok

    `ngrok http http://localhost:5000`

2. Set webhook URL for Telegram

    ```
    export TG_TOKEN=yourtoken
    export NGROK_URL=yoururl

    curl "https://api.telegram.org/bot$TG_TOKEN/setWebhook?url=$NGROK_URL/bot"
    ```

3. Start flask dev server

    ```
    cd meemirobotti
    FLASK_APP=main flask run
    ```

    Or if using gotask:

    `task run`

    Or start something closer to a production server:

    ```
    cd meemirobotti
    gunicorn main:app -b 127.0.0.1:5050
    ```

## Installation

Clone this repository.

    git clone https://github.com/santerj/python-project-template.git [my-project]

## Usage

Run the interactive installer.

    python ./setup.py

After installation, there is some boilerplate code in `meemirootti/main.py` and `tests/test_main.py`.

Tasks for unit testing, linting, security auditing etc. are included in the `noxfile.py`. Try to invoke it with

    nox

If you don't have nox installed globally, just use the one included in the virtual environment:

    dev-venv/bin/nox
