import tweepy
import yaml
import json
import os
import traceback
import asyncio

file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml')

config = yaml.load(open(file_path ,'r'), Loader=yaml.Loader)
auth = tweepy.OAuthHandler(config['api_key'], config['api_secret_key'])
auth.set_access_token(config['access_token'], config['access_secret_token'])

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# api.update_status('Test Tweet from Python')

class RestockStreamListener(tweepy.StreamListener):
    def __init__(self, discord, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.discord = discord
        self.loop = loop

    def on_data(self, data):
        tweet = json.loads(data)
        link = f"http://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}"
        future = asyncio.run_coroutine_threadsafe(self.discord(msg), self.loop)
        future.result()
        print(link)

    def on_error(self, status_code):
        print(f'ERROR. Status Code: {status_code}')
        return False

# create async method for twitter updates
def twitter_stock_updates(myBot):
    try:
        # get users the twitter account follows
        users = [str(i) for i in api.friends_ids('coderbott')]

        # keywords for finding stock
        keywords = ['ps5 restock', 'ps5 disc', 'ps5 digital', '[DROP]', 'ps5 bundle', 'xbox bundle']

        # start stream
        myStream = tweepy.Stream(auth = api.auth, listener=RestockStreamListener(callback=send_msg(myBot)))
        print('Start streaming.')
        myStream.filter(track=keywords)
    except Exception as e:
        print(e)
        traceback.print_exc()
        print("Stopped.")
    finally:
        print('Done.')
        myStream.disconnect()