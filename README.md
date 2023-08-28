# meemirobotti
_since 2018!_

## Quickstart

Easiest way to run is with [Docker](https://www.docker.com/) (or [podman](https://podman.io/)).

First, make your very own environment variable file:

    cp .env.example .env

Next, obtain any necessary API tokens or relevant nonsense and fill any placeholders in the file.

    $EDITOR .env

Now you can run your own local instance of the meemirobotti by entering this in your terminal.

    docker run --env-file=".env" --rm $(docker build -q .)

If something goes wrong with the build, examine logs for example by running

    docker build .

and submitting an issue.

If for some reason you will not use docker, the following should get you started:

    # make sure your python interpreter is at least at version 3.10
    python -m venv venv && venv/bin/python install -r requirements.txt
    venv/bin/python main.py

