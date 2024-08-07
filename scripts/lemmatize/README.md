# Lemmatizing literature

The unholiest part of the repository. Here lies nlp tomfoolery that
[lemmatizes](https://en.wikipedia.org/wiki/Lemmatization) the entirety of a text file.

Run all commands in ´scripts´ directory. All necessary requirements are specified in `requirements.txt`.

## Finnish

    $ ./prepare_bible_fi.sh
    $ python lemmatize.py -l fi -i temp/fi/bible_fi.txt -o temp/fi/bible_fi_lemmatized.txt

## English

    $ ./prepare_bible_en.sh
    $ python lemmatize.py -l en -i temp/en/bible_en.txt -o temp/en/bible_en_lemmatized.txt
