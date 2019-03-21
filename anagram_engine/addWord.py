import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

from wordModel import WordModel
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class AddWord(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template('templates/addPage.html')
        self.response.write(template.render())

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') == 'Add':
            word = self.request.get('word_name')
            print '------------'
            print word
            # word_key = ndb.Key('WordModel', word)
            # addWord = word_key.get()

            addWord = WordModel(id=generate_key(word))
            addWord.wordList = self.request.get('word_name')
            addWord.wordCount = len(word)
            addWord.letterCount = len(word)
            addWord.userId = users.get_current_user().email()

            addWord.put()
            self.redirect('/')

        elif self.request.get('button') == 'Cancel':
            self.redirect('/')


# sort all letters of the word into lexicographical order
def generate_key(param):
    sorted_list = sorted(param)
    sorted_string = ''
    for x in sorted_list:
        sorted_string = sorted_string + x
    return sorted_string
