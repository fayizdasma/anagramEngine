import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import users

from addWord import generate_key
from wordModel import WordModel
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class SubAnagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        isSearchClicked = False
        search_result = None
        sub_anagram_result = None

        # when search button is clicked
        if self.request.get('button') == 'Search':
            isSearchClicked = True
            searchWord = self.request.get('word_name').upper()
            userEmail = users.get_current_user().email()
            sortedWord = generate_key(searchWord)
            anagram_key = ndb.Key(WordModel, sortedWord + ',' + userEmail)

            # query for anagram
            anagram = searchForAnagram(anagram_key)
            if anagram != None:
                search_result = anagram[0].wordList

            # query for sub-anagram
            print '---sub anagram---'
            for index in range(len(sortedWord)):
                search_key = ndb.Key(WordModel, sortedWord[index:4])
                s = searchForAnagram(search_key)
                if s != None:
                    sub_anagram_result[index] = s

        template_values = {
            'search_result': search_result,
            'isSearchClicked': isSearchClicked,
        }
        template = JINJA_ENVIRONMENT.get_template('templates/subAnagramPage.html')
        self.response.write(template.render(template_values))


def searchForAnagram(anagram_key):
    query = WordModel.query()
    query = query.filter(WordModel.userId == users.get_current_user().email())
    query = query.filter(WordModel.key == anagram_key)
    anagram = query.fetch()
    return anagram
