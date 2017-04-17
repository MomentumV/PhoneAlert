# PhoneAlert README #

 ## Setup instructions ##
   - This is a Python app; you'll need to have a Python 2.7 installation.
   - You will need to create both a twitter app and a Twilio free user trial
   - Enter your api keys from twitter and twilio into secrets.yml.sample and save it as secrets.yml
   - Enter your phone numbers, search settings into config.yml.sample, save it as config.yml


 ## helpful hints ##
   - the streaming.py for tweepy has some important improvements since the 3.5 version available through pip.
   - get_ids.py is a little script that returns the twitter user id from an entered twitter @handle
   - sms notification is used when your streaming app is rate limited  from too many started streams (code 420... chill out; seriously, that's what twitter calls it). Plan to only start ~2 streams per day; save some data and work with that for testing.

