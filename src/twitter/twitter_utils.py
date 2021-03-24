import tweepy
import yaml
import json
import os
import traceback
import asyncio
import redis

file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml')

config = yaml.load(open(file_path ,'r'), Loader=yaml.Loader)
auth = tweepy.OAuthHandler(config['api_key'], config['api_secret_key'])
auth.set_access_token(config['access_token'], config['access_secret_token'])

api = tweepy.API(auth)

r = redis.Redis(host='localhost', port=6379, db=0)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# api.update_status('Test Tweet from Python')

class RestockStreamListener(tweepy.StreamListener):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        print('init Stream listener')

    def on_data(self, data):
        tweet = json.loads(data)
        link = f"http://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}"
        print(link)
        r.set(f'link:{tweet['id']}', link)

    def on_error(self, status_code):
        print(f'ERROR. Status Code: {status_code}')
        return False

def twitter_update(myBot):
    print('starting stream')
    users = [str(i) for i in api.friends_ids('coderbott')]
    stream = tweepy.Stream(auth = api.auth, listener=RestockStreamListener(bot=myBot))
    stream.filter(track = ['ps5 restock', 'ps5 disc', 'ps5 digital', '[DROP]', 'ps5 bundle', 'xbox bundle', 'trump'])
    print('ending stream')


class DummyBot:
    tweets = []

if __name__=='__main__':
    twitter_update(DummyBot())