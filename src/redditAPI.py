import json

import praw
import requests
import requests.auth


class redditAPI:
    def __init__(self, id, secret, user, password):
        self.REDDIT_ID = id
        self.REDDIT_SECRET = secret
        self.REDDIT_USER = user
        self.REDDIT_PASS = password

        #### Courtesy of https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
        client_auth = requests.auth.HTTPBasicAuth(self.REDDIT_ID, self.REDDIT_SECRET)
        post_data = {
            "grant_type": "password",
            "username": self.REDDIT_USER,
            "password": self.REDDIT_PASS,
        }
        headers = {"User-Agent": "yvillia-bot/0.1 by " + self.REDDIT_USER}
        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=client_auth,
            data=post_data,
            headers=headers,
        )
        access = response.json()["access_token"]
        headers = {
            "Authorization": "bearer " + access,
            "User-Agent": "yvillia-bot/0.1 by " + self.REDDIT_USER,
        }
        response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
        # print(json.dumps(response.json(), indent=3))
        ####

        self.reddit = praw.Reddit(
            client_id=self.REDDIT_ID,
            client_secret=self.REDDIT_SECRET,
            user_agent="CoderBot/0.1 by " + self.REDDIT_USER,
            username=self.REDDIT_USER,
            password=self.REDDIT_PASS,
        )

        self.me = self.reddit.user.me()
