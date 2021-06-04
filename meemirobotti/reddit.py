import praw
import random
import configparser
import typing
from typing import List
from classes import Meme


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
        # fault_meme = Meme("kokeile myöhemmin uudestaan", "https://imgur.com/a/MLzITmE", "Koodissa vikaa")

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
