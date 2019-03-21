from google.appengine.ext import ndb


class WordModel(ndb.Model):
    wordList = ndb.StringProperty()
    wordCount = ndb.IntegerProperty()
    letterCount = ndb.IntegerProperty()
