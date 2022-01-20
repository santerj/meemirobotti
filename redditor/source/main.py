import random
from dataclasses import dataclass
from os import getenv
from tempfile import tempdir
from time import sleep
from typing import List

import praw
import redis


@dataclass
class Meme:
    sub: str
    title: str
    url: str

def meme2Str(meme: Meme) -> str:
    return f"{meme.sub}:\n{meme.title}\n{meme.url}"

class Redditor:
    """
    Virtual redditor who browses reddit and gives us memes
    """
    def __init__(self) -> None:

        self.client_id  = getenv("REDDIT_CLIENT_ID")
        self.secret     = getenv("REDDIT_SECRET")
        self.user_agent = getenv("REDDIT_USER_AGENT")
        self.redis_host = getenv("REDIS_HOST")
        self.redis_port = getenv("REDIS_PORT")
        self.redis_pass = getenv("REDIS_PASSWORD")
        self.redis_key  = "queue:memes"

        self.subreddits = []
        self.parse_subreddits("reddits.txt")
        self.multireddit = "+".join(self.subreddits)

        self.reddit = praw.Reddit(
            client_id = self.client_id,
            client_secret = self.secret,
            user_agent = self.user_agent
        )

        self.redis = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            db=0,
            password=self.redis_pass,
            decode_responses=True,
        )

    def parse_subreddits(self, filename: str) -> None:
        with open(filename, 'r') as f:
            lines = f.readlines()
        f.close()

        for line in lines:
            if line.startswith('#') or line == '\n':
                continue
            else:
                self.subreddits.append(line.rstrip("\n"))

    def get_memes(self, amount: int) -> List[Meme]:
        """
        Does NOT guarantee that return array contains <amount> amount
        of memes. Works as best effort, can be anything 0 <= amount
        """
        limit = 100
        if amount > limit:
            raise Exception(
                "amount of memes requested is greater \
                than the amount of memes available"
            )

        allow_pre = ("imgur", "i.imgur", "i.redd")
        allow_post = ('.jpg', 'jpeg', '.png', '.gif')

        #posts = self.reddit.subreddit(self.multireddit).hot(limit=limit)
        posts = self.reddit.subreddit(self.multireddit).top(time_filter='day', limit=limit)
        #posts = self.reddit.subreddit(self.multireddit).rising()
        posts = [post for post in posts]  # from ListingGenerator to list
    
        random.shuffle(posts)

        post_list = []
        loc = len("https://")
        
        while len(post_list) < amount:
            for i, post in enumerate(posts):
                if post.url[loc:].startswith(allow_pre) and post.url.endswith(allow_post):
                    meme = Meme(post.subreddit, post.title, post.url)
                    post_list.append(meme)

                if len(post_list) == amount or i+1 == limit:
                    # amount reached or post list completely exhausted
                    return post_list

    def get_meme(self) -> Meme:
        # return a single meme
        return self.get_memes(amount=1)[0]

    def getQueueSize(self) -> int:
        return self.redis.llen(self.redis_key)

    def pushToQueue(self, memes: List[Meme]):
        tempQ = []
        for meme in memes:
            tempQ.append(meme2Str(meme))
        self.redis.rpush(self.redis_key, *tempQ)

def main():
    targetQueueLength = 25
    redditor = Redditor()

    while True:
        queueLengthDiff = targetQueueLength - redditor.getQueueSize()
        if queueLengthDiff > 0:
            memes = redditor.get_memes(amount=queueLengthDiff)
            redditor.pushToQueue(memes=memes)
        sleep(15)

if __name__ == '__main__':
    main()
