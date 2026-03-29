import json
import subprocess

from libvoikko import Voikko
from lightlemma import lemmatize

v = Voikko("fi")

def lemmatize_en():
    subprocess.run(["./prepare_bible_en.sh"], check=True)

    with open("./temp/en/bible_en.txt", "r") as f:
        text = f.read()
        words = text.split()
        unique_words = set(words)

    lemmatized = []
    for word in unique_words:
        lemma = lemmatize(word)
        lemmatized.append(lemma.lower())

    lemmatized = set(lemmatized)
    lemmatized.discard("")
    return lemmatized

def lemmatize_fi():
    subprocess.run(["./prepare_bible_fi.sh"], check=True)

    with open("./temp/fi/bible_fi.txt", "r") as f:
        text = f.read()
        words = text.split()
        unique_words = set(words)

    lemmatized = []
    for word in unique_words:
        try:
            lemma = v.analyze(word)[0]["BASEFORM"]
            lemmatized.append(lemma.lower())
        except IndexError:
            print(f"Could not lemmatize {word}")
            lemmatized.append(word.lower())
            continue

    lemmatized = set(lemmatized)
    lemmatized.discard("")
    return lemmatized

def main():
    en = lemmatize_en()
    fi = lemmatize_fi()

    with open('results/lemmatized_en.json', 'w', encoding='utf-8') as f:
        json.dump(list(en), f, ensure_ascii=False, indent=4)

    with open('results/lemmatized_fi.json', 'w', encoding='utf-8') as f:
        json.dump(list(fi), f, ensure_ascii=False, indent=4)

    subprocess.run(["./cleanup.sh"], check=True)

if __name__ == "__main__":
    main()
