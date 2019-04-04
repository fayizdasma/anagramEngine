from google.appengine.ext import ndb


class CountModel(ndb.Model):
    uniqueCount = ndb.IntegerProperty()
    totalcount = ndb.IntegerProperty()
