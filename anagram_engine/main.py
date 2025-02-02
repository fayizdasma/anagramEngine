import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from countModel import CountModel
from userModel import UserModel
from wordModel import WordModel
from subAnagram import SubAnagram
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

            myuser_key = ndb.Key(UserModel, user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                myuser = UserModel(id=user.user_id())
                myuser.user = user.email()
                myuser.put()

            # get total anagram count
            count_data_key = ndb.Key(CountModel, user.email())
            count_data = CountModel.query(CountModel.key == count_data_key).fetch()

            if count_data != None:
                if len(count_data) > 0:
                    wordCount = count_data[0].totalcount
                    anagramCount = count_data[0].uniqueCount

        else:
            response_url = users.create_login_url(self.request.uri)
            response_url_string = 'login'

        # when search button is clicked
        if self.request.get('button') == 'Search':
            isSearchClicked = True
            userEmail = ''
            searchWord = self.request.get('word_name').upper()
            sortedWord = generate_key(searchWord)
            if users.get_current_user() != None:
                userEmail = users.get_current_user().email()
            anagram_key = ndb.Key(WordModel, sortedWord + ',' + userEmail)
            anagram = WordModel.query(WordModel.key == anagram_key).fetch()
            if anagram != None:
                if len(anagram) > 0:
                    search_result = anagram[0].wordList

        # when upload button is clicked, read file and populate user dictionary
        if self.request.get('button') == 'Upload':
            uploadFile = self.request.get('wordListFile')
            if uploadFile != None:
                os_directory = os.path.dirname(__file__)
                file = open(os.path.join(os_directory, uploadFile), "r")
                print file.readline()
                for x in file:
                    if x != None:
                        x = x.rstrip()
                        add_to_database(x.upper())
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


app = webapp2.WSGIApplication([('/', MainPage), ('/add', AddWord), ('/subAnagram', SubAnagram)], debug=True)
