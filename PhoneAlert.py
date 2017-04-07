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
smsphone = twildict['sms_notification']
fromphone = twildict['fromphone']
callurl = twildict['url']

#create client object to use for calls or texts
client = Client(account,token)

#store search parameters
ulist=searchdict['user']
tlist=searchdict['track']

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
                print 'keyword '+word+' found'
                trigger = 1
        if trigger == 1:
            #print 'make call to '+tophone+' from '+fromphone
            call = client.calls.create(to=tophone, from_=fromphone, url=callurl)
        if trigger == 0:
            print 'no keywords matched; no call made'
        return True

    def on_error(self, code):
        if code == 420:
            message = client.api.account.messages.create(to=smsphone,from_=fromphone,body='420 error, we are down!') 
            return False
        else:
            message = client.api.account.messages.create(to=smsphone,from_=fromphone,body='error code: '+status)
            return False
if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = CallListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
#    api = tweepy.API(auth)
#    user = api.get_user(screen_name = 'MordecaiV')
#    print(user.id)
#    print(dir(user))

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(follow=ulist,async=True)
    #stream.filter(follow=u, async=True)
#for section,d in cfg.items():
#	for k,v in d.items():
#		print k+': '+v
