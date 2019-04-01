import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from userModel import UserModel
from wordModel import WordModel
from addWord import AddWord

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        isSearchClicked = False
        search_result = None
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

            # get all
            anagram_all = WordModel.query(WordModel.userId == user.email()).fetch()
            wordCount = 0
            anagramCount = 0
            if anagram_all != None:
                # print anagram_all
                anagramCount = len(anagram_all)
                for x in anagram_all:
                    wordCount = wordCount + x.wordCount
                print 'total word count'
                print wordCount
                print 'unique count'
                print anagramCount

        else:
            response_url = users.create_login_url(self.request.uri)
            response_url_string = 'login'

        # when search button is clicked
        if self.request.get('button') == 'Search':
            isSearchClicked = True
            searchWord = self.request.get('word_name')
            sortedWord = generate_key(searchWord)
            anagram = ndb.Key(WordModel, sortedWord).get()
            if anagram != None:
                search_result = anagram.wordList

        # pass values to the html page
        template_values = {
            'url': response_url,
            'url_string': response_url_string,
            'user': user,
            'search_result': search_result,
            'isSearchClicked': isSearchClicked,
            'anagram_count': anagramCount,
            'word_count': wordCount
        }
        main_template = JINJA_ENVIRONMENT.get_template('/templates/homePage.html')
        self.response.write(main_template.render(template_values))


# sort all letters of the word into lexicographical order
def generate_key(param):
    sorted_list = sorted(param)
    sorted_string = ''
    for x in sorted_list:
        sorted_string = sorted_string + x
    return sorted_string


app = webapp2.WSGIApplication([('/', MainPage), ('/add', AddWord)], debug=True)
