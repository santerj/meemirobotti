import random

async def help(text: str) -> str:
    choiceDelimiter = " vai "

    text = text[len("text")+1:]  # strip command part out
    if len(text) == 0:
        return f"/help: Valitse usean vaihtoehdon välillä käyttämällä sanaa \"vai\".\n" \
               f"Jos haluat joo/ei päätöksen, päätä viesti kysymysmerkkiin"

    # string has choice delimiter
    elif text.find(choiceDelimiter) != -1:
        parts = text.split(choiceDelimiter)
        return random.choice(parts)

    # question mark terminator
    elif text[-1] == "?":
        return random.choice(("Joo", "Ei"))

    else:
        return "En tiedä"
