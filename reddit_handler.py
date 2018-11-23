import praw
import prawcore
import random


def get_url(multireddit, client_id, client_secret, user_agent):
    """RETURNS:
        link:str
        title:str
        subreddit:str
    """

    # Reddit script initialised here.
    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    if len(multireddit) < 1:
        print("Critical error! No subreddits found!")
        exit(1)

    # Retrieve a random subreddit.
    # Index is generated with 'random' library with max value of list length.
    random_sub = multireddit[random.randrange(len(multireddit))]

    sub = reddit.subreddit(random_sub)

    try:
        posts = [post for post in sub.hot(limit=100)]

    except prawcore.exceptions.Redirect:
        multireddit.remove(random_sub)
        random_sub = multireddit[random.randrange(len(multireddit))]
        sub = reddit.subreddit(random_sub)
        posts = [post for post in sub.hot(limit=100)]

    i = 0
    while True:

        if i > 50:
            get_url(multireddit, client_id, client_secret, user_agent)

        random_post_number = random.randrange(1, 99)
        random_post = posts[random_post_number]
        url = random_post.url

        # This part looks awful, but it returns the next 8(?)
        # characters from url which are after 'i.'.
        # So for example we can check if the link is from
        # i.imgur.com or i.redd.it (which is what is done below).
        loc = url.find('i.')
        site_name = url[loc + 2:loc + 10].split('.')[0]
        whitelist = ["imgur", "redd"]

        if site_name in whitelist:
            # Satisfying link was found.
            link = url
            title = random_post.title
            subreddit = str(sub)
            return link, title, subreddit

        i += 1
