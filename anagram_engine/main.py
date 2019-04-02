import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from userModel import UserModel
from wordModel import WordModel
from addWord import AddWord, add_to_database, generate_key

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
        wordCount = 0
        anagramCount = 0
        if user:
            response_url = users.create_logout_url(self.request.uri)
            response_url_string = 'logout'

            myuser_key = ndb.Key('UserModel', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                myuser = UserModel(id=user.user_id())
                myuser.user = user.email()
                myuser.put()

            # get total anagram count
            anagram_all = WordModel.query(WordModel.userId == user.email()).fetch()

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
            searchWord = self.request.get('word_name').upper()
            sortedWord = generate_key(searchWord)
            anagram_key = ndb.Key(WordModel, sortedWord)
            anagram = WordModel.query(ndb.AND(WordModel.userId == user.email(), WordModel.key == anagram_key)).fetch()
            print anagram
            if anagram != None:
                search_result = anagram

        # when upload button is clicked, read file and populate user dictionary
        if self.request.get('button') == 'Upload':
            uploadFile = self.request.get('wordListFile')
            if uploadFile != None:
                os_directory = os.path.dirname(__file__)
                file = open(os.path.join(os_directory, uploadFile), "r")
                print file.readline()
                for x in file:
                    if x != None:
                        isAlreadyThere = add_to_database(x.upper())
                file.close()
                self.response.out.write('''<script>alert('Upload wordlist to database complete');</script>''')

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


app = webapp2.WSGIApplication([('/', MainPage), ('/add', AddWord)], debug=True)
