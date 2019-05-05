import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from viewtweets import ViewTweets
import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
                       extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome User'
        myuser = None
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'Sign_out'
            email = users.get_current_user().email()
            myuser_key = ndb.Key('MyUser', email)
            myuser = myuser_key.get()
            mk=ndb.Key('ViewTweets','db')
            m=mk.get()
            if m==None:
                m=ViewTweets(id='db')
                m.put()
            if myuser == None:
                welcome = 'Welcome User'
                myuser = MyUser(id=email)
                myuser.put()
            if myuser.uname==None:
                self.redirect('/username')
        else:

            url = users.create_login_url(self.request.uri)
            url_string = 'Signin'
        query=query = MyUser.query().fetch()
        username=self.request.get('usersearch')
        lastuser=None
        a=0
        searchtweet=self.request.get('searchtweet')
        finaltweet=[]
        b=0
        action=self.request.get('button')
        if action=='Search':
            for i in query:
                if i.uname==username:
                    a=a+1
                    lastuser=username
        if action=='Tweet Search':
            for i in query:
                for j in i.tweet:
                    if searchtweet in j:
                        b=b+1
                        finaltweet.append(j)
        list_followers=0
        list_following=0
        if myuser!=None:
            for i in myuser.followers:
                    list_followers=list_followers+1
            for j in myuser.following:
                    list_following=list_following+1

        t_key = ndb.Key('ViewTweets', 'db')
        tkey = t_key.get()
        tl=[]
        tun=[]
        if tkey!=None:
            for i in reversed(tkey.all_tweets):
                tl.append(i)
            tl = tl[:50]
            for j in reversed(tkey.un):
                tun.append(j)
            tun=tun[:50]
        tff = map(' --> '.join,zip(tun,tl))

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'myuser' : myuser,'a':a,
            'lastuser':lastuser,'b':b,
            'finaltweet':finaltweet,
            'list_followers':list_followers,
            'list_following':list_following,'tff':tff
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))



class Username(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user().email()
        myuser_key = ndb.Key('MyUser', email)
        myuser = myuser_key.get()
        self.response.out.write("<html><head></head><body>")
        self.response.out.write("""<form method='get' action='/username'>""")
        self.response.out.write("""USERNAME:<br/><input type='text' name='input' required='True'/><br/>""")
        self.response.out.write("""INFO:<br/><input style="height:200px;width:1000px;font-size:14pt;
                                " type='text' name='input1' required='True' maxlength="280"/><br/>""")
        self.response.out.write("""<input type='submit' name='button' value='Submit'/>""")
        self.response.out.write("""</form>""")
        action=self.request.get('button')
        url = users.create_logout_url(self.request.uri)
        if action == 'Submit':
                username=self.request.get('input')
                info=self.request.get('input1')
                myuser.uname=username
                myuser.userinfo=info
                myuser.put()
                self.redirect('/')
        self.response.write('<br/><a href="/">Logout</a>')
        self.response.out.write("</body></html>")


class Edit(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user().email()
        myuser_key = ndb.Key('MyUser', email)
        myuser = myuser_key.get()
        self.response.out.write("<html><head></head><body>")
        self.response.out.write("Edit your information below:<br/>")
        self.response.out.write("""<form method='get' action='/edit'>""")
        a=myuser.userinfo
        self.response.out.write("""INFO:<br/><input style="height:200px;width:1000px;font-size:14pt;
                                " type='text' name='input1' required='True' maxlength="280" placeholder="%s"/>
                                <br/>"""%(a))
        self.response.out.write("""<input type='submit' name='button' value='Submit'/>""")
        self.response.out.write("""</form>""")
        self.response.out.write("<a href='/'>Home</a>")
        action=self.request.get('button')
        if action == 'Submit':
            info=self.request.get('input1')
            myuser.userinfo=info
            myuser.put()
            self.redirect('/')
        self.response.out.write("</body></html>")
    def post(self):
        email = users.get_current_user().email()
        myuser_key = ndb.Key('MyUser', email)
        myuser = myuser_key.get()
        action=self.request.get('button')
        mk=ndb.Key('ViewTweets', 'db')
        m=mk.get()
        name=myuser.uname
        if action == 'Submit':
            tweet=self.request.get('tweet')
            myuser.tweet.append(tweet)
            m.all_tweets.append(tweet)
            m.un.append(name)
            m.put()
            myuser.put()
            self.redirect('/')

class UInfo(webapp2.RequestHandler):
    def get(self,id):
        self.response.headers['Content-Type'] = 'text/html'
        my=id
        query = MyUser.query(MyUser.uname == my)
        l=[]
        for i in query:
            for j in reversed(i.tweet):
                l.append(j)
        l = l[:50]
        template_values={'query':query,'l':l}
        template=JINJA_ENVIRONMENT.get_template('uinfo.html')
        self.response.write(template.render(template_values))
    def post(self,id):
        email = users.get_current_user().email()
        myuser_key = ndb.Key('MyUser', email)
        myuser = myuser_key.get()
        username=myuser.uname
        my=id
        emails=None
        followers_username=None
        query = MyUser.query(MyUser.uname == my)
        for i in query:
            emails=i.key.id()
        action=self.request.get('button')
        if action == 'FOLLOW':
                myuser_keys = ndb.Key('MyUser', emails)
                myusers = myuser_keys.get()
                followers_username=myusers.uname
                if username==myusers.uname:
                        self.redirect('/uinfo/%s'%(my))
                else:
                    if username in myusers.followers:
                            self.redirect('/uinfo/%s'%(my))
                    else:
                            myusers.followers.append(username)
                            myuser.following.append(followers_username)
                            myuser.put()
                            myusers.put()
                            self.redirect('/uinfo/%s'%(my))
        if action == 'UNFOLLOW':
            myuser_keys = ndb.Key('MyUser', emails)
            myusers = myuser_keys.get()
            followers_username=myusers.uname
            if username in myusers.followers:
                myusers.followers.remove(username)
                myusers.put()
                if followers_username in myuser.following:
                    myuser.following.remove(followers_username)
                    myuser.put()
            self.redirect('/uinfo/%s'%(my))



class DelEdit(webapp2.RequestHandler):
    def get(self,id):
        self.response.headers['Content-Type'] = 'text/html'
        my=id
        email = users.get_current_user().email()
        myuser_key = ndb.Key('MyUser', email)
        myuser = myuser_key.get()
        l=myuser.tweet
        l=l[::-1]
        template_values={'myuser':myuser,'l':l}
        template=JINJA_ENVIRONMENT.get_template('deledit.html')
        self.response.write(template.render(template_values))
    def post(self,id):
        action = self.request.get('button')
        email = users.get_current_user().email()
        myuser_key = ndb.Key('MyUser', email)
        myuser = myuser_key.get()
        db_key = ndb.Key('ViewTweets', 'db')
        db = db_key.get()
        my=id
        tw=None
        if action == 'delete':
            l=myuser.tweet
            l=l[::-1]
            del l[int(self.request.get('index')) - 1]
            l=l[::-1]
            myuser.tweet=l
            myuser.put()
            tw=self.request.get('users_name')
            db.all_tweets.remove(tw)
            db.put()
            self.redirect('/deletedit/%s'%(my))
        if action=='Edit':
            tw=self.request.get('users_name')
            l1=myuser.tweet
            l1=l1[::-1]
            tw1=l1[int(self.request.get('index'))-1]
            l=myuser.tweet
            l=l[::-1]
            l[int(self.request.get('index'))-1]=self.request.get('users_name')
            l=l[::-1]
            myuser.tweet=l
            myuser.put()
            db.all_tweets[db.all_tweets.index(tw1)]=tw
            db.put()
            self.redirect('/deletedit/%s'%(my))

app = webapp2.WSGIApplication([('/', MainPage),
('/username', Username),('/edit',Edit),('/uinfo/(.*)',UInfo),
('/deletedit/(.*)',DelEdit)], debug=True)
