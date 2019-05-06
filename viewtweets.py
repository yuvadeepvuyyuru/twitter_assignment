from google.appengine.ext import ndb


class ViewTweets(ndb.Model):
    all_tweets = ndb.StringProperty(repeated=True)
    un = ndb.StringProperty(repeated=True)
    a
