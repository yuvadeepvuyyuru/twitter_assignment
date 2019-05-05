from google.appengine.ext import ndb


class MyUser(ndb.Model):
    uname = ndb.StringProperty()
    userinfo = ndb.StringProperty()
    tweet = ndb.StringProperty(repeated=True)
    followers = ndb.StringProperty(repeated=True)
    following = ndb.StringProperty(repeated=True)
