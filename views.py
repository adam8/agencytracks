import cgi
import os
import webapp2
import json
import ndb_json
#import datetime
#import time
from google.appengine.ext import ndb
from google.appengine.api import users 
from google.appengine.api import memcache
from base_handler import BaseHandler
import re
import jinja2
jinja_env = jinja2.Environment(autoescape=True, loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))
#
from models import *



#
#####--- Functions ---####
#
def slugify(string):
	import re
	string.lstrip()
	string.rstrip()
	if string == "":
	  string = "untitled"
	string = re.sub('\s+', '-', string)
	string = re.sub('[^\w.-]', '', string)
	string = re.sub('---', '--', string)
	string = string[0:80]
	return string.strip('_.- ').lower()

def randomString(num):
  import random  
  letters = list("abcdefghijkmnopqrstuvwxyz23456789")
  pw = ''.join([random.choice(letters) for i in xrange(num)])
  return str(pw)
  
def getUniqueKey(ModelName):
  the_key_name = randomString(4)
  duplicate_instance = ndb.Key(ModelName, the_key_name).get()
  if duplicate_instance is not None:
    getUniqueKey(ModelName)
  else:
    return the_key_name

def get_tasks(client_key,the_step_key):
  tasks = memcache.get('postTasks' + client_key + '-' + the_step_key + 'Memcache')
  if tasks is not None:
    return tasks 
  else:
    #tasks = Tasks.query().order(-Tasks.created).fetch(20)
    tasks = Tasks.query(ancestor = client_key).filter(Tasks.step==the_step_key).order(Tasks.order).fetch()
    if not memcache.add('postTasks' + client_key + '-' + the_step_key + 'Memcache', tasks, 1000):
      logging.error('Memcache set failed.')
  return tasks 

def get_clients():
  clients = memcache.get('clientsMemcache')
  if clients is not None:
    return clients
  else:
    clients = Clients.query(ancestor = ndb.Key(Clients, "lvl")).order(-Clients.created).fetch(20)
    if not memcache.add('clientsMemcache', clients, 1000):
      logging.error('Memcache set failed.')
  return clients 

def get_steps():
  steps = memcache.get('stepsMemcache')
  if steps is not None:
    return steps
  else:
    steps = Steps.query(ancestor = ndb.Key(Clients, "lvl")).order(Steps.order).fetch()
    if not memcache.add('stepsMemcache', steps, 604800000): # one week
      logging.error('Memcache set failed.')
  return steps
def get_questions(client):
  questions = memcache.get('questions-'+ client.key.id() + '-Memcache')
  if questions is not None:
    return questions
  else:
    questions = Questions.query(ancestor = client.key).fetch()
    if not memcache.add('questions-'+ client.key.id() + '-Memcache', questions, 604800000): # one week
      logging.error('Memcache set failed.')
  return questions



def create_default_questionnaire():
  return [
    (u'question_success', u'What will make this project successful?'), 
    (u'question_domain', u'Does this website have a domain name already?'), 
    (u'question_goals', u'Set the website\'s top 3 goals in order of priority. Try to be specific:'),
    (u'question_goal1', u''), 
    (u'question_goal2', u''), 
    (u'question_goal3', u''), 
    (u'question_target_audience', u'Who is the target audience?'), 
    (u'question_brand', u'How would you describe the brand?'), 
    (u'question_competitive_advantage', u'Does your company have a competetive advantage?'),  
    (u'question_envy', u'List 3 websites you like:'),
    (u'question_envy1', u''), 
    (u'question_envy2', u''), 
    (u'question_envy3', u''), 
    (u'question_envy_details', u'What do you like about these websites?'), 
    (u'question_competitors', u'List 3 competitor websites:'),
    (u'question_competitor1', u''), 
    (u'question_competitor2', u''), 
    (u'question_competitor3', u''), 
    (u'question_competitor_details', u'What are these competitor\'s strengths/weaknesses?'), 
    (u'question_marketing', u'Do you have any marketing campaigns?'), 
    (u'question_budget_timeframe', u'Do you have a budget and/or timeframe for this project?'), 
    (u'question_additional_info', u'Anything else you\'d like to add or ask us?'), 
    (u'question_name', u'Your name'), 
    (u'question_email', u'Your email'), 
    (u'question_phone', u'Your phone')
  ]
def login():
  user = users.get_current_user()
  if user:
    client = Clients.query(Clients.email == user.email()).get()
    if client or user.email() == "test@example.com":
      return '<div id="logout">' + user.nickname() + ' <a class="pure-button" href="' + users.create_logout_url("/") + '" rel="nofollow">Sign Out</a></div>'
    else:
      return user.email()
  else:
    return ''

#
login = login()
user = users.get_current_user()
if user is not None:
  domain = re.search("@[\w.]+", user.nickname()).group()
author = "client"
if domain == "@corp.thelevel.com":
  author = "lvl"
template_values = { 'login': login, "user": user, "author": author } #TODO memcache this
#
####--- Handlers ---#### 
#
class TestHandler(BaseHandler):
  def get(self):
    self.response.out.write("Hey!")

class DashboardTheLevelHandler(BaseHandler):
  def get(self,client):
    client_key = ndb.Key(Clients, "lvl", Clients, client)
    client = client_key.get()
    template_values['client'] = client
    template_values['steps'] = get_steps()
    template_values['step_open'] = self.request.get('step') 
    template_values['notes'] = ndb.get_multi(client.note_keys) 
    for question in get_questions(client):
      template_values[question.key.id()] = question
    self.render_template('dashboard_thelevel.html', template_values)


class DashboardClientHandler(BaseHandler):
  def get(self,client):
    client_entity = ndb.Key(Clients, "lvl", Clients, client).get()
    if client_entity is not None:
      widgets_dirty = ndb.get_multi(client_entity.widget_keys)
      widgets = []
      for w in widgets_dirty:
        if w is not None:
          widgets.append(w)
      template_values['widgets'] = widgets
      template_values['client'] = client_entity
      self.render_template('dashboard_client.html', template_values)
    else:
      self.response.out.write('Sorry, client not found.')
      self.response.set_status(404)

class HomeHandler(BaseHandler):
  def get(self):
    template_values['clients'] = get_clients()
    template_values['steps'] = get_steps()
    self.render_template('index.html', template_values)

class TasksHandler(BaseHandler):
  def get(self,client,task_id):
    the_task = ndb.Key(Clients, client, Tasks, task_id).get()
    the_client = ndb.Key(Clients, "lvl", Clients, client).get()
    if the_task is not None:
      template_values['task'] = the_task
      template_values['client'] = the_client
      self.render_template('tasks.html', template_values) 
    else:
      self.response.out.write('eh?')
      self.response.set_status(404)
  @ndb.transactional(xg=True)
  #@BaseHandler.is_user_admin
  def post(self,client):
    task_text = self.request.get('task_text')
    client_key = ndb.Key(Clients, "lvl", Clients, client)
    if client_key.get() is not None:
      the_key_name = getUniqueKey("Tasks")  
      task = Tasks( parent = client_key,
                    client_abbreviation = self.request.get('client'),
                    task_text = task_text,
                    id = the_key_name ) 
      task.put()
      self.redirect("/clients/" + client)
    else:
      self.response.out.write('not ok')





class NotesHandler(BaseHandler):
  @ndb.transactional(xg=True)
  def post(self,client,user):
    note = self.request.get('note').strip()
    if user == "lvl":
      author = "lvl"
    else:
      author = client
    client_key = ndb.Key(Clients, "lvl", Clients, client)
    the_client = client_key.get()
    if the_client is not None:
      #user = users.get_current_user()
      user = users.User(user)
      nickname = user.nickname().split("@")[0]
      note = Notes( parent = client_key, id = randomString(8), text = note, author = author, user = user, nickname = nickname )
      note.put()
      the_client.note_keys.insert(0,note.key)  # When note is removed, be sure to delete widget key referenced in client
      the_client.put()
      #self.redirect("/clients/" + client)
      self.response.out.write('success')
    else:
      self.response.out.write('not ok')

class NotesClientDashboardHandler(BaseHandler):
  @ndb.transactional(xg=True)
  def get(self,client,user):
    the_client = ndb.Key(Clients, "lvl", Clients, client).get()
    if the_client is not None:
      template_values['client'] = the_client
      template_values['notes'] = ndb.get_multi(the_client.note_keys[0:10])
      self.render_template('notes.html', template_values)

class WidgetHandler(BaseHandler):
  def get(self,client,widget_id):
    the_widget = ndb.Key(Clients, "lvl", Clients, client, Widgets, widget_id).get()
    the_client = ndb.Key(Clients, "lvl", Clients, client).get()
    if the_widget is not None:
      template_values['widget'] = the_widget
      template_values['client'] = the_client
      self.render_template('widget.html', template_values) 
    else:
      self.response.out.write('Client not found.')
      self.response.set_status(404)
  @ndb.transactional(xg=True)
  def post(self,client):
    title = self.request.get('title').strip()
    text = self.request.get('text').strip()
    embed = self.request.get('embed').strip()
    theme = self.request.get('theme')
    client_key = ndb.Key(Clients, "lvl", Clients, client)
    the_client = client_key.get()
    if the_client is not None:
      widget = Widgets( parent = client_key, id = randomString(8), title = title, text = text, embed = embed, theme = theme )
      widget.put()
      the_client.widget_keys.insert(0,widget.key)
      the_client.put()
      self.redirect("/dashboard/" + client)
    else:
      self.response.out.write('not ok')


class WidgetUpdateHandler(BaseHandler):
  @ndb.transactional(xg=True)
  def post(self,client,widget_id):
    client_key = ndb.Key(Clients, "lvl", Clients, client)
    the_client = client_key.get()
    if the_client is not None:
      widget = ndb.Key(Clients, "lvl", Clients, client, Widgets, widget_id).get()
      if widget is not None:
        if self.request.get('victim') != widget_id:
          widget.title = self.request.get('title').strip()
          widget.text = self.request.get('text').strip()
          widget.embed = self.request.get('embed').strip()
          widget.link = self.request.get('link').strip()
          widget.theme = self.request.get('theme')
          widget.put()
        else:
          the_client.widget_keys.remove(widget.key) # also delete widget key referenced in client instance
          the_client.put()
          widget.key.delete()
        self.redirect("/dashboard/" + client)
      else:
        self.response.out.write('no widget found')
    else:
      self.response.out.write('no client') 


class WidgetOrderHandler(BaseHandler):
  @ndb.transactional(xg=True)
  def post(self,client):
    order = json.loads(self.request.get('order'))
    widget_keys = []
    widgets_updated = []
    the_client = ndb.Key(Clients, "lvl", Clients, client).get()
    if the_client is not None:
      for t in order:
        if 'id' in t:
          widget = ndb.Key(Clients, "lvl", Clients, client, Widgets, t['id'])
          widget_keys.append(widget)
      the_client.widget_keys = widget_keys
      the_client.put()
      widget_entities = ndb.get_multi(widget_keys)  
      for idx, the_widget in enumerate(widget_entities):
        if the_widget is not None:
          the_widget.order = float(idx)
          widgets_updated.append(the_widget)
      ndb.put_multi(widgets_updated)
      response = {'result':'success'}
      self.response.headers['Content-Type'] = "application/json"
      self.response.out.write(ndb_json.encode(response))

class TasksDeleteHandler(BaseHandler):
  def post(self,client,victim):
    client_key = client
    victim = victim
    victim = ndb.Key(Clients, "lvl", Clients, client_key, Tasks, victim)
    victim.delete()
    #memcache.delete('task'+victim+'Memcache')
    self.redirect("/clients/"+client_key+"?step="+self.request.get('step'))

class ClientsHandler(BaseHandler):
  def get(self,client):
    the_client = ndb.Key(Clients, "lvl", Clients, client).get()
    if the_client is not None:
      template_values['client'] = the_client
      self.render_template('clients.html', template_values) 
    else:
      self.response.out.write('client not found?')
      self.response.set_status(404) 
  #@ndb.transactional(xg=True)
  #@BaseHandler.is_user_admin
  def post(self):
    client_name = self.request.get('client_name')
    abbreviation = slugify(self.request.get('abbreviation'))
    if client_name is not None:
      slug = slugify(client_name)
      doppleganger = ndb.Key(Clients, "lvl", Clients, abbreviation).get()
      if doppleganger:
        self.response.out.write('This client abbreviation already exists: ' + abbreviation)
      else:
        client = Clients( parent = ndb.Key(Clients, "lvl"), id = abbreviation, client_name = client_name, slug = slug, abbreviation = abbreviation ) 
        client.put()
        # Initilize Questionnaire
        default_questions = create_default_questionnaire()
        for q in default_questions:
          question_entity = Questions(parent=client.key,id=q[0])
          question_entity.question = q[1]
          question_entity.put()
        # Clone Project Template
        project_template = self.request.get("project_template")
        clone_company_key = ndb.Key(Clients, "lvl", Clients, project_template)
        clone_company = clone_company_key.get()
        tasks = Tasks.query(ancestor=clone_company_key).fetch()        
        if clone_company is not None:
          for task in tasks:
            # Clone the entity with new ID/NAME.
            clone = Tasks(parent=client.key, id=getUniqueKey("Tasks"), **task.to_dict())
            clone.parent = clone_company_key
            clone.client_abbreviation = abbreviation
            clone.time_actual = None
            clone.done = False
            clone.blocked = False
            # Delete properties. 
            # delattr(clone, 'prop_to_del')
            clone.put()
          self.redirect("/clients/"+abbreviation)
        else:
          self.redirect("/")
        memcache.delete('clientsMemcache')
    else:
      self.response.out.write('not ok')



class ClientsDeleteHandler(BaseHandler):
  def post(self):
    if self.request.get('victim') != "lvl":
      victim = ndb.Key(Clients, "lvl", Clients, self.request.get('victim'))
      victim.delete()
      memcache.delete('clientsMemcache')
      self.redirect("/")
    else:
      self.response.out.write("Don't delete The Level!")


class ClientsUsersHandler(BaseHandler):
  def post(self,client):
    the_client = ndb.Key(Clients, "lvl", Clients, client).get()
    if the_client is not None:
      if self.request.get('new_user').strip() != "":
        the_client.email.append(self.request.get('new_user').strip())
        the_client.put()
        self.redirect(self.request.referrer)
      else:
        self.redirect(self.request.referrer + "?err")
    else:
      self.response.out.write('client not found')

class StepsHandler(BaseHandler):
  def get(self,step_keyname):
    the_step_key = ndb.Key(Clients, "lvl", Steps, step_keyname)
    the_step = the_step_key.get()
    client_key = ndb.Key(Clients, "lvl")
    tasks = Tasks.query(ancestor = client_key).filter(Tasks.step==the_step_key).order(Tasks.order).fetch()
    if the_step is not None:
      template_values['step'] = the_step
      template_values['tasks'] = tasks
      self.render_template('step.html', template_values) 
    else:
      self.response.out.write('step not found.')
      self.response.set_status(404)
  def post(self):
    step_name = self.request.get('step_name').strip()
    order_number = self.request.get('order').strip()
    if order_number == "":
      order_number = 0
    try:
      order = int(order_number)
    except:
      self.response.out.write('Step number must be an integer')
    if order is not None:
      slug = slugify(step_name)
      if ndb.Key(Clients, "lvl", Steps, slug).get() is not None:
        self.response.out.write('hmm... this step already seems to exist: ' + step_name)
      else:
        step = Steps( parent = ndb.Key(Clients, "lvl"), id = slug, order = order, step_name = step_name ) 
        step.put()
        memcache.delete('stepsMemcache')
        self.redirect(self.request.referrer)
    else:
      self.response.out.write('not ok')
      


class StepsAjaxHandler(BaseHandler):
  def get(self,client,item_keyname):
    the_step_key = ndb.Key(Clients, "lvl", Steps, item_keyname)
    the_step = the_step_key.get()
    client_key = ndb.Key(Clients, "lvl", Clients, client)
    tasks = Tasks.query(ancestor = client_key).filter(Tasks.step==the_step_key).order(Tasks.order).fetch()
    if the_step is not None:
      template_values['step'] = the_step
      template_values['tasks'] = tasks
      template_values['client'] = client_key.get()
      self.render_template('step_ajax.html', template_values) 
    else:
      self.response.out.write('step not found.')
      self.response.set_status(404)
  def post(self,client,item_keyname):
    the_task_key = ndb.Key(Clients, "lvl", Clients, client, Tasks, item_keyname)
    task = the_task_key.get()
    if self.request.get('done') == "True":
      task.done = True
    else:
      task.done = False
    if self.request.get('time_estimate'):
      task.time_estimate = int(self.request.get('time_estimate'))
    if self.request.get('time_actual'):
      task.time_actual = int(self.request.get('time_actual'))
    if self.request.get('order'):
      task.order = float(self.request.get('order').strip())
    if self.request.get('task_text'):
      task_text = self.request.get('task_text').strip()
      task.task_text = task_text.replace("<br>", " ");
    if self.request.get('task_type'):
      task.task_type = self.request.get('task_type').strip()
    if self.request.get('indent'):
      if task.indent == True:
        task.indent = False
      else:
        task.indent = True
    #memcache.delete('postTasks' + client_key + '-' + the_step_key + 'Memcache')
    task.put()
    self.response.out.write("Done.")
    

class TaskOrderHandler(BaseHandler):
  @ndb.transactional(xg=True)
  def post(self,client):
    order = json.loads(self.request.get('order'))
    task_keys = []
    tasks_updated = []
    for t in order:
      task = ndb.Key(Clients, "lvl", Clients, client, Tasks, t['id'])
      task_keys.append(task)
    task_entities = ndb.get_multi(task_keys)  
    for idx, the_task in enumerate(task_entities):
      if the_task is not None:
        the_task.order = float(idx)
        tasks_updated.append(the_task)
    ndb.put_multi(tasks_updated)
    response = {'result':'success'}
    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(ndb_json.encode(response))

class StepsTaskHandler(BaseHandler):
  def post(self):
    task_text = self.request.get('task_text')
    step_name = self.request.get('step_name')
    task_type = self.request.get('task_type')
    client = self.request.get('client')
    step_key = ndb.Key(Clients, "lvl", Steps, step_name)
    client_key = ndb.Key(Clients, "lvl", Clients, client)
    task_estimate = int(self.request.get('task_estimate'))
    order_num = float(self.request.get('order'))
    if client_key is not None and step_key is not None and task_text is not None:
      the_key_name = getUniqueKey("Tasks")
      task = Tasks( parent = ndb.Key(Clients, "lvl", Clients, client),
                    client_abbreviation = client,
                    step = step_key,
                    time_estimate = task_estimate,
                    task_text = task_text,
                    task_type = task_type,
                    order = order_num,
                    id = the_key_name ) 
      task.put()
      self.redirect("/clients/" + client + "?step=" + step_name)
    else:
      self.response.out.write('not ok')
class StepsDeleteHandler(BaseHandler):
  def post(self):
    victim = ndb.Key(Clients, "lvl", Steps, self.request.get('victim'))
    victim.delete()
    memcache.delete('stepsMemcache')
    self.redirect("/")

class QuestionnaireHandler(BaseHandler):
  def post(self,client):
    questions = self.request.POST.items()
    client_key = ndb.Key(Clients, "lvl", Clients, client)
    the_client = client_key.get()
    question_entities = []
    for i in questions:
      question_entity = ndb.Key(Clients, "lvl", Clients, client, Questions,i[0]).get()
      if question_entity is not None:
        question_entity.answer = i[1].strip()
        question_entities.append(question_entity)
        #question_entity.put()
    ndb.put_multi(question_entities)
    memcache.delete('questions-'+ the_client.key.id() + '-Memcache')
    self.redirect("/clients/"+client)
    #self.response.out.write("success")
class QuestionnaireInitHandler(BaseHandler):
  def get(self,client):
    default_questions = create_default_questionnaire()
    client_key = ndb.Key(Clients, "lvl", Clients, client)
    for q in default_questions:
      doppleganger = ndb.Key(Clients, "lvl", Clients, client, Questions,q[0]).get()
      if doppleganger is None:
        question_entity = Questions(parent=client_key,id=q[0])
        question_entity.question = q[1]
        question_entity.put()
    self.response.out.write("success")
    #self.response.out.write(default_questions)
#







