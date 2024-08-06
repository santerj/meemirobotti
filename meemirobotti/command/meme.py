import random
import time
from collections import deque
from dataclasses import dataclass
from tempfile import tempdir
from typing import List

import praw
from loguru import logger


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
    def __init__(self, client_id: str, secret: str, user_agent: str, queue_size: int = 25) -> None:
        self.targetQueueLength = queue_size
        self.subreddits = []
        self.parse_subreddits("reddits.txt")
        self.multireddit = "+".join(self.subreddits)
        self.queue = deque()

        self.reddit = praw.Reddit(
            client_id = client_id,
            client_secret = secret,
            user_agent = user_agent
        )
        self.reddit.read_only = True
        self.refresh_queue()

    def parse_subreddits(self, filename: str) -> None:
        with open(filename, 'r') as f:
            lines = f.readlines()
        f.close()

        for line in lines:
            if line.startswith('#') or line == '\n':
                continue
            else:
                self.subreddits.append(line.rstrip("\n"))

    def _get_memes(self, amount: int) -> List[Meme]:
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

    def _queue_size(self) -> int:
        return len(self.queue)

    def _push_to_queue(self, memes: List[Meme]):
        for meme in memes:
            self.queue.append(meme2Str(meme))

    def refresh_queue(self):
        tic = time.perf_counter()
        length = self._queue_size()
        target = self.targetQueueLength
        queueLengthDiff = target - length
        if queueLengthDiff > 0:
            logger.info(f'REFRESHING QUEUE | {length=} | {target=}')
            memes = self._get_memes(amount=queueLengthDiff)
            self._push_to_queue(memes=memes)
            toc = time.perf_counter()
            logger.success(f'DONE | took {toc - tic:0.4f} s')
        else:
            logger.info(f'QUEUE FULL | {length=}')

    def get_meme(self) -> Meme:
        return self.queue.popleft()
