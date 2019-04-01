from google.appengine.ext import ndb


class WordModel(ndb.Model):
    wordList = ndb.StringProperty(repeated=True)
    wordCount = ndb.IntegerProperty()
    letterCount = ndb.IntegerProperty()
    userId = ndb.StringProperty()
