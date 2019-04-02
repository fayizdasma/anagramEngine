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
            word = self.request.get('word_name').upper()
            # print '------------'
            # print word
            isAlreadyThere = add_to_database(word)
            if isAlreadyThere:
                self.response.out.write('''<script>alert('This word already added!');</script>''')
            else:
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


# add to db and return status
def add_to_database(word):
    sortedWord = generate_key(word)
    addWord = WordModel(id=sortedWord)
    word_key = ndb.Key('WordModel', sortedWord)
    oldWord = word_key.get()
    isWordAlreadyThere = False

    if oldWord != None:
        if word not in oldWord.wordList:
            oldWord.wordList.append(word)
            addWord.wordList = oldWord.wordList
        else:
            isWordAlreadyThere = True
    else:
        addWord.wordList = [word]

    if not isWordAlreadyThere:
        addWord.wordCount = len(addWord.wordList)
        addWord.letterCount = len(word)
        addWord.userId = users.get_current_user().email()
        addWord.put()

    return isWordAlreadyThere
