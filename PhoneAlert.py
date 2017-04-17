import yaml,json,time,pdb
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twilio.rest import Client

def load_secrets():
    with open("secrets.yml") as secrets_file:
        secrets = yaml.safe_load(secrets_file)
    return secrets

def load_settings():
    with open("config.yml") as settings_file:
        config = yaml.safe_load(settings_file)
    return config

#define a basic listener
class CallListener(StreamListener):

    def on_data(self, data):
        print 'matched tweet based on filtered user id'
        jsondata=json.loads(data)
        #write data to disk; serves to prove the script is working/running
        with open('data.txt','w') as outfile:
            json.dump(jsondata,outfile)
        userid = jsondata['user']['id_str']
        if not userid in ulist:
            print 'not one of our users'
            return True #return True continues the listener
        #reload the track list and exclude lists
        config = load_settings()
        searchdict = config['search_set']
        tlist = searchdict['track']
        exclude = searchdict['not']
        tweettext=jsondata['text']
        print tweettext.encode('utf-8')
        #pdb.set_trace()
        trigger = 0
        lowered_tweet_text = tweettext.lower()
        for word in tlist:
            if word in lowered_tweet_text:
                print 'keyword {0} found'.format(word)
                trigger += 1
        for word in exclude:
            if word in lowered_tweet_text:
                print 'excluded string {0} found'.format(word)
                trigger = -1
        if trigger > 0:
            print 'make call to {0} from {1}'.format(tophone,fromphone)
            #make phone call first
            call = client.calls.create(to=tophone, from_=fromphone, url=callurl)
            #send text message containg the twitter message to tophone
            message = client.api.account.messages.create(to=tophone,from_=fromphone,body=tweettext) 
            #save tweet as test data
            with open('triggered_data.txt','w') as outfile:
                json.dump(jsondata,outfile)   
        elif trigger == 0:
            print 'no keywords matched; no call made'
        elif trigger < 0:
            print 'excluded strings found; no call made'
        return True

    def on_error(self, code):
        if code == 420:
            message = client.api.account.messages.create(to=errorphone,from_=fromphone,body=ratelimitmess) 
            return False
        else:
            message = client.api.account.messages.create(to=errorphone,from_=fromphone,body=textmess.format(code))
            return False

if __name__ == '__main__':
    #load settings
    #retrieve secrets and configuration  files
    secrets = load_secrets()
    config = load_settings()
    twitsec = secrets['twitter_set']
    twilsec = secrets['twilio_set']
    
    #store twitter secrets in variables
    access_token = twitsec['access_token']
    access_token_secret = twitsec['access_secret']
    consumer_key = twitsec['consumer_key']
    consumer_secret = twitsec['consumer_secret']
    #store twilio secrets in variables
    account = twilsec['account']
    token = twilsec['token']
    
    #store configuration details in variables.
    searchdict = config['search_set']
    settings = config['settings']
    
    #store search parameters
    ulist = searchdict['user']
    tlist = searchdict['track']
    exclude = searchdict['not']
    
    #define message settings
    tophone = settings['tophone']
    errorphone = settings['err_notification']
    fromphone = settings['fromphone']
    callurl = settings['url']
    errtextmess = settings['err_txt'] #'error code: {0}'
    ratelimitmess = settings['rate_lim_txt'] #'420 error! chill out, man! we are down.'
    
    #create twilio client object to use for calls or texts
    client = Client(account,token)
    
    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = CallListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    #This line filter Twitter Streams to capture tweets from the user ids listed in ulist, which are pulled in from the config file. use the get_ids.py helper script to extract user ids from @handles
    stream.filter(follow=ulist,async=True)
