from os import getenv
from dotenv import load_dotenv

load_dotenv()

def required(name: str) -> str:
    value = getenv(name)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

class Config:
    ROBOTTI_TG_TOKEN = required("ROBOTTI_TG_TOKEN")
    ROBOTTI_TG_STALE_MESSAGE_AGE = int(getenv("ROBOTTI_TG_STALE_MESSAGE_AGE", 15))
    ROBOTTI_REDDIT_CLIENT_ID = required("ROBOTTI_REDDIT_CLIENT_ID")
    ROBOTTI_REDDIT_SECRET = required("ROBOTTI_REDDIT_SECRET")
    ROBOTTI_REDDIT_USER_AGENT = getenv("ROBOTTI_REDDIT_USER_AGENT", "meemirobotti")
    ROBOTTI_REDDIT_QUEUE_SIZE = int(getenv("ROBOTTI_REDDIT_QUEUE_SIZE", 25))
    ROBOTTI_SENTRY_DSN = required("ROBOTTI_SENTRY_DSN")
    ROBOTTI_SENTRY_ENV = getenv("ROBOTTI_SENTRY_ENV", "dev")

CONFIG = Config()