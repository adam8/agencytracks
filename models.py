from google.appengine.ext import ndb

class Questions(ndb.Model):
  question = ndb.StringProperty()
  answer = ndb.StringProperty()
  
class Clients(ndb.Model): 
  client_name = ndb.StringProperty()
  email = ndb.StringProperty(repeated=True)
  slug = ndb.StringProperty()
  abbreviation = ndb.StringProperty()
  created = ndb.DateTimeProperty(required=True, auto_now_add=True)
  note_keys = ndb.KeyProperty(repeated=True)
  widget_keys = ndb.KeyProperty(repeated=True)
  username = ndb.StringProperty() #temp!!!!
  passweird = ndb.StringProperty() #temp!!!!

class Tasks(ndb.Model):
  task_text = ndb.StringProperty()
  client_abbreviation = ndb.StringProperty()
  task_type = ndb.StringProperty()
  order = ndb.FloatProperty()
  step = ndb.KeyProperty()
  time_estimate = ndb.IntegerProperty()
  time_actual = ndb.IntegerProperty()
  done = ndb.BooleanProperty(default=False)
  indent = ndb.BooleanProperty(default=False)
  created = ndb.DateTimeProperty(required=True, auto_now_add=True) 
  blocked = ndb.BooleanProperty(default=False)
  
class Steps(ndb.Model):
  step_name = ndb.StringProperty()
  order = ndb.IntegerProperty()

class Notes(ndb.Model):
  text = ndb.TextProperty()
  author = ndb.StringProperty()
  user = ndb.UserProperty()
  nickname = ndb.StringProperty()
  created = ndb.DateTimeProperty(required=True, auto_now_add=True)
  updated = ndb.DateTimeProperty(required=True, auto_now=True)

class Widgets(ndb.Model):
  title = ndb.StringProperty()
  order = ndb.FloatProperty()
  text = ndb.TextProperty()
  embed = ndb.TextProperty()
  image = ndb.StringProperty()
  link = ndb.StringProperty()
  theme = ndb.StringProperty()
  created = ndb.DateTimeProperty(required=True, auto_now_add=True)
  