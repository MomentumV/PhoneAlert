# PhoneAlert README #

 ## Setup instructions ##
   - This is a Python app; you'll need to have a Python 2.7 installation.
   - You will need to create both a twitter app and a Twilio free user trial
   - Enter your api keys from twitter and twilio, as well as the search terms into config.yml.sample, save it as config.yml.

 ## helpful hints ##
   - get_ids.py is a little script that returns the twitter user id from an entered twitter @handle
   - sms notification is used when your streaming app is rate limited (code 420... chill out; seriously, that's what twitter calls it). Plan to only start ~2 streams per day; save some data and work with that for testing.

