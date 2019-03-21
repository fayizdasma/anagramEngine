import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from userModel import UserModel

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        response_url = ''
        response_url_string = ''
        user = users.get_current_user()
        if user:
            response_url = users.create_logout_url(self.request.uri)
            response_url_string = 'logout'

            myuser_key = ndb.Key('UserModel', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                myuser = UserModel(id=user.user_id())
                myuser.user = user.email()
                myuser.put()

        else:
            response_url = users.create_login_url(self.request.uri)
            response_url_string = 'login'

        # pass values to the html page
        template_values = {
            'url': response_url,
            'url_string': response_url_string,
            'user': user,
        }
        main_template = JINJA_ENVIRONMENT.get_template('/templates/homePage.html')
        self.response.write(main_template.render(template_values))


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
