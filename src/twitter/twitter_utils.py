import tweepy
import yaml
import json

config = yaml.load(open('config.yml' ,'r'), Loader=yaml.Loader)
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
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_data(self, data):
        self.callback(data)

    def on_error(self, status_code):
        print(f'ERROR. Status Code: {status_code}')
        return False

# create a wrapper function so that bot can send message. 
def send_msg(myBot):
    def wrapper(data):
        tweet = json.loads(data)
        link = f"http://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}"
        myBot.channels['stock-updates'].send_message(link)

    return wrapper

# create async method for twitter updates
async def twitter_stock_updates(myBot):
    try:
        # get users the twitter account follows
        users = [str(i) for i in api.friends_ids('coderbott')]

        # keywords for finding stock
        keywords = ['ps5 restock', 'ps5 disc', 'ps5 digital', '[DROP]', 'ps5 bundle', 'xbox bundle']

        # start stream
        myStream = tweepy.Stream(auth = api.auth, listener=RestockStreamListener(callback=send_msg(myBot)))
        print('Start streaming.')
        await myStream.filter(track=keywords, is_async=True)
    except Exception as e :
        print("Stopped.")
    finally:
        print('Done.')
        myStream.disconnect()