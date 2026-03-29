import json
import string

from libvoikko import Voikko
from lightlemma import lemmatize, text_to_lemmas, tokenize

from meemirobotti.model import telegram

v = Voikko("fi")

def tokenize_en(text: str) -> list[str]:
    return tokenize(text)

def check_if_biblical(lemmae: list[str], lang: str) -> str:
    # Compare (preferably lemmatized) list of words to the lemmatized bible, return amt of matches
    with open(f'./scripts/lemmatize/results/lemmatized_{lang}.json', 'r', encoding='utf-8') as f:
        biblical_words = set(json.load(f))

    matches = [lemma for lemma in lemmae if lemma.lower() in biblical_words]
    return len(matches)

def bible(update: telegram.Update) -> str:
    if update.message.reply_to_message:
        text = update.message.reply_to_message.text

    lemmatized = text_to_lemmas(text)
    original_lemmae = len(lemmatized)
    biblical_lemmae = check_if_biblical(lemmatized, 'en')
    percentage = (biblical_lemmae / original_lemmae) * 100 if original_lemmae > 0 else 0
    return f"{percentage:.2f}% of these words are in the bible"

def raamattu(update: telegram.Update) -> str:
    if update.message.reply_to_message:
        text = update.message.reply_to_message.text

    tokenized_raw = [token.tokenText for token in v.tokens(text) if token.WORD == 1]
    # remove tokens that are only punctuation or only whitespace
    tokenized = {
        t for t in tokenized_raw
        if t.strip() and not all(ch in string.punctuation for ch in t)
    }
    lemmatized = []
    for word in tokenized:
        try:
            lemma = v.analyze(word)[0]['BASEFORM']
            lemmatized.append(lemma)
        except IndexError:
            # word not recognized, skip it
            continue
    original_lemmae = len(lemmatized)
    biblical_lemmae = check_if_biblical(lemmatized, 'fi')
    percentage = (biblical_lemmae / original_lemmae) * 100 if original_lemmae > 0 else 0
    return f"{percentage:.2f}% näistä sanoista on raamatussa"
    
