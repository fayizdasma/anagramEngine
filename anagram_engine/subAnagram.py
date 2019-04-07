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

sub_list = []


class SubAnagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        isSearchClicked = False
        search_result = None
        sub_anagram_result = []

        # when search button is clicked
        if self.request.get('button') == 'Search':
            isSearchClicked = True
            searchWord = self.request.get('word_name').upper()
            userEmail = users.get_current_user().email()
            sortedWord = generate_key(searchWord)

            # query for anagram
            anagram_key = ndb.Key(WordModel, sortedWord + ',' + userEmail)
            anagram = WordModel.query(WordModel.key == anagram_key).fetch()
            if anagram != None:
                if len(anagram) > 0:
                    search_result = anagram[0].wordList

            # query for sub-anagram
            generateSubAnagram(sortedWord)
            # fetch db for this word
            for x in sub_list:
                search_key = ndb.Key(WordModel, x + ',' + userEmail)
                s_anagram = WordModel.query(WordModel.key == search_key).fetch()
                if s_anagram != None:
                    if len(s_anagram) > 0:
                        # print '------sub-------'
                        # print s_anagram[0].wordList
                        sub_anagram_result.append(s_anagram[0].wordList[0])
            del sub_list[:]

        template_values = {
            'search_result': search_result,
            'sub_anagram_result': sub_anagram_result,
            'isSearchClicked': isSearchClicked
        }
        template = JINJA_ENVIRONMENT.get_template('templates/subAnagramPage.html')
        self.response.write(template.render(template_values))


# removes each letter of word and generates sub anagram recursively
def generateSubAnagram(wrd):
    letters = list(wrd)
    for i in range(len(letters)):
        letters = list(wrd)
        letters.remove(letters[i])
        word = ''.join(letters)
        if len(word) >= 3:
            sorted = generate_key(word)
            # print sorted
            if sorted not in sub_list:
                sub_list.append(sorted)
            generateSubAnagram(word)
