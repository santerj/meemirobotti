# Lemmatizing literature

The unholiest part of the repository. Here lies nlp tomfoolery that
[lemmatizes](https://en.wikipedia.org/wiki/Lemmatization) the entirety of a text file.

The directory comes with a prebuilt index of lemmatized results in json format inside `results`.
It is also possible to tune the lemmatization process in `lemmatize.py` and the included shell scripts.

## How to

Setup venv, install dependencies

    python -m venv venv
    venv/bin/python -m pip install -r requirements.txt

Run lemmatizer

    venv/bin/python lemmatize.py

## Voikko

`libvoikko` has to be installed to build dictionary.
