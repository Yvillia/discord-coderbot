import tweepy
import yaml
import json
import os
import sys
# import redis
from urllib3.exceptions import ProtocolError

file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml')

try:
    config = yaml.load(open(file_path ,'r'), Loader=yaml.Loader)
except FileNotFoundError as e:
    print(e)
    print("Please setup a yaml file with api_key, api_secret_key, bearer_token, access_token, access_secret_token keys as strings")
    sys.exit(0)

auth = tweepy.OAuthHandler(config['api_key'], config['api_secret_key'])
auth.set_access_token(config['access_token'], config['access_secret_token'])

api = tweepy.API(auth)

# r = redis.Redis(host='localhost', port=6379, db=0)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# api.update_status('Test Tweet from Python')

class RestockStreamListener(tweepy.StreamListener):
    def __init__(self, users, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users = users
        print('init Stream listener')

    def on_data(self, data):
        tweet = json.loads(data)

        if tweet['user']['id'] in self.users:
            print('authentic tweet')
            link = f"http://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}"
            r.set(f"link:{tweet['id']}", link)
        else:
            unAuthTweetCount = r.get('unAuthTweetCount')
            if unAuthTweetCount:
                unAuthTweetCount = int(unAuthTweetCount) + 1
                r.set('unAuthTweetCount', unAuthTweetCount)
            else:
                r.set('unAuthTweetCount', 1)

        # print(tweet)

    def on_error(self, status_code):
        print(f'ERROR. Status Code: {status_code}')
        return False
    
def twitter_update():
    print('starting stream')
    while True:
        try:
            _twitter_update()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(e)
            continue


def _twitter_update():
    users = [str(i) for i in api.friends_ids('coderbott')]
    print(users)
    stream = tweepy.Stream(auth = api.auth, listener=RestockStreamListener(users=users))
    while True:
        try: 
            stream.filter(track = ['ps5 restock', 'ps5 disc', 'ps5 digital', '[DROP]', 'ps5 bundle', 'xbox bundle'], follow=users, filter_level="medium")
        except (ProtocolError, ArithmeticError):
            continue
        except KeyboardInterrupt:
            sys.exit(0)

if __name__=='__main__':
    twitter_update()