import yaml 
from tweepy import OAuthHandler, API

#retrieve config file with secrets
config = yaml.safe_load(open("config.yml"))
twitdict = config['twitter_set']

#store twitter secrets in variables
access_token = twitdict['access_token']
access_token_secret = twitdict['access_secret']
consumer_key = twitdict['consumer_key']
consumer_secret = twitdict['consumer_secret']

if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    handle = raw_input('enter user handle :@')
    user = api.get_user(screen_name=handle)
    print(user.id)
