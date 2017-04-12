import yaml,json,time,pdb
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twilio.rest import Client

#retrieve config file with secrets
config = yaml.safe_load(open("config.yml"))
#print(config)
#with open("config.yml",'r') as ymlfile:
#    cfg = yaml.load(ymlfile)
#twitdict= cfg['twitter_set']
twitdict = config['twitter_set']
#twildict= cfg['twilio_set']
twildict = config['twilio_set']
searchdict = config['search_set']
#store twitter secrets in variables
access_token = twitdict['access_token']
access_token_secret = twitdict['access_secret']
consumer_key = twitdict['consumer_key']
consumer_secret = twitdict['consumer_secret']

#store twilio secrets in variables
account = twildict['account']
token = twildict['token']

#get a twilio token


#store call details from config in variables
tophone = twildict['tophone']
errorphone = twildict['err_notification']
fromphone = twildict['fromphone']
callurl = twildict['url']

#create client object to use for calls or texts
client = Client(account,token)

#store search parameters
ulist = searchdict['user']
tlist = searchdict['track']
exclude = searchdict['not']

#define message strings
errtextmess = 'error code: {0}'
ratelimitmess = '420 error! chill out, man! we are down.'

#define a basic listener
class CallListener(StreamListener):

    def on_data(self, data):
        print 'matched tweet'
        jsondata=json.loads(data)
        with open('data.txt','w') as outfile:
            json.dump(jsondata,outfile)
        #pdb.set_trace()
        userid = jsondata['user']['id_str']
        if not userid in ulist:
            print 'not one of our users'
            return True
        tweettext=jsondata['text']
        print tweettext.encode('utf-8')
        #pdb.set_trace()
        trigger = 0
        for word in tlist:
            if word in tweettext.lower():
                print 'keyword {0} found'.format(word)
                trigger += 1
        for word in exclude:
            if word in tweettext.lower():
                print 'excluded string {0} found'.format(word)
                trigger = -1
        if trigger > 0:
            #print 'make call to '+tophone+' from '+fromphone
            #make phone call first
            call = client.calls.create(to=tophone, from_=fromphone, url=callurl)
            #send text message containg the twitter message to tophone
            message = client.api.account.messages.create(to=tophone,from_=fromphone,body=tweettext) 
            #save tweet as test data
            with open('triggered_data.txt','w') as ou$
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

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = CallListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    #This line filter Twitter Streams to capture tweets from the user ids listed in ulist, which are pulled in from the config file. use the get_ids.py helper script to extract user ids from @handles
    stream.filter(follow=ulist,async=True)
