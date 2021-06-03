import praw
import random
import configparser
import typing
from typing import List
from classes import Meme

import time

class Redditor:
    """
    Virtual redditor who browses reddit and gives us memes
    """
    def __init__(self) -> None:

        config = configparser.ConfigParser()
        config.read('config')
        self.client_id      = config['reddit']['client_id']
        self.secret         = config['reddit']['secret']
        self.user_agent     = config['reddit']['user_agent']

        self.subreddits = []
        self.parse_subreddits(
            config['reddit']['subreddit_list']
        )
        self.multireddit = "+".join(self.subreddits)

        self.reddit = praw.Reddit(
            client_id = self.client_id,
            client_secret = self.secret,
            user_agent = self.user_agent
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

    def get_meme(self, legacy: bool = False) -> Meme:

        start = time.time()

        limit = 75
        allow_pre = ("imgur", "i.imgur", "i.redd")
        allow_post = ('.jpg', 'jpeg', '.png', '.gif')
        fault_meme = Meme("kokeile myöhemmin uudestaan", "https://imgur.com/a/MLzITmE", "Koodissa vikaa")

        if legacy:
            # older logic, get post from a randomized sub
            sub = self.reddit.subreddit(
                random.choice(self.subreddits)
            )
            posts = sub.top(time_filter='day', limit=limit)
            posts = [post for post in posts]
            if len(posts) < 5:
                # sub is not super active, get top posts of week instead to
                # avoid very low quality posts
                posts = sub.top(time_filter='week', limit=limit)
                posts = [post for post in posts]

        else:  # new logic, get post from big multireddit, should be
               # more fault tolerant
            posts = self.reddit.subreddit(self.multireddit).hot(limit=limit)
            posts = [post for post in posts]  # from ListingGenerator to list
        
        random.shuffle(posts)

        for post in posts:
            loc = len("https://")
            if post.url[loc:].startswith(allow_pre) and post.url.endswith(allow_post):
                meme = Meme(post.subreddit, post.title, post.url)
                end = time.time()
                print("reddit-pass", end-start)
                return meme

        end = time.time()
        print("reddit-fail", end-start)
        return fault_meme  # in case list is empty or nothing matches allowlists

        def get_memes(self, amount: int = 1, legacy: bool = False) -> List[Meme]:
            """
            The redditor is very generous and sends as many memes as the cache needs
            """
            pass
            # re-implemet get_meme() with a sense of how many are returned
            # this helps with reddit API throttling re:the cache
