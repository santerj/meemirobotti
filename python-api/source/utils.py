import virtualkb

import random
import re


def help(text: str) -> str:
    choiceDelimiter = " vai "

    if len(text) == 0:
        helpText = "/help: Valitse usean vaihtoehdon välillä käyttämällä sanaa \"vai\". Jos haluat joo/ei päätöksen, päätä viesti kysymysmerkkiin (?)"
        return helpText

    # string has choice delimiter
    elif text.find(choiceDelimiter) != -1:
        parts = text.split(choiceDelimiter)
        return random.choice(parts)    

    # question mark terminator
    elif text[-1] == "?":
        return random.choice(("Joo", "Ei"))


def uwuify(text: str) -> str:
    # parse kaomoji thingies
    kaomojiFile = "uwus.txt"
    with open(kaomojiFile, "r") as f:
        kaomojis = f.readlines()
    f.close()
    for i, kaomoji in enumerate(kaomojis):
        kaomojis[i] = kaomoji.rstrip("\n")

    if len(text) == 0:
        return random.choice(kaomojis)
    
    # replace symbols
    text = re.sub('R', 'W', text)
    text = re.sub('L', 'W', text)
    text = re.sub('r', 'w', text)
    text = re.sub('l', 'w', text)
    text = re.sub('\.', '!!!!', text)

    parts = text.split(" ")
    for i, part in enumerate(parts):
        if random.randint(0, 15) == 0:
            # capitalize word on chance
            parts[i] = part.upper()
        if part[-1] == "!" and random.randint(0, 3) == 0:
            # add random kaomoji on chance
            parts[i] = f"{part[:-1]} {random.choice(kaomojis)}"
    
    # end on kaomoji
    parts.append(random.choice(kaomojis))
    
    return " ".join(parts)


def misspell(text: str, multiplier: int = 1) -> str:
    """
    Return text but with typos
    TODO: rework multiplier
    """
    if multiplier <= 0:  # avoid death by mathematics
        multiplier = 1

    if len(text) == 0:
        return "/kaannos: Vastaa johonkin viestiin komennolla /kaannos"
    elif len(text) < 50:
        chance = 25 // multiplier
    else:
        chance = 10 // multiplier

    nearKeys = virtualkb.neigboringKeys(virtualkb.keyboardUpper)
    nearKeys.update(virtualkb.neigboringKeys(virtualkb.keyboardLower))
    knownChars = nearKeys.keys()
    
    newText = ""  # str is immutable so build new str as we go
    for symbol in text:
        if symbol not in knownChars:
            newText += symbol
            continue
        if random.randint(0, chance) == 0:
            # simulate typo on QWERTY keeb
            newText += random.choice(nearKeys[symbol])
        else:
            newText += symbol

    return newText
