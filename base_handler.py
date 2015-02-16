import webapp2
from webapp2_extras import jinja2
from webapp2_extras import sessions
import json
import random

from models import *

from google.appengine.api import users

class BaseHandler(webapp2.RequestHandler):
  """The other handlers inherit from this class.  Provides some helper methods
for rendering a template and generating template links."""

  def dispatch(self):
	# Get a session store for this request.
    self.session_store = sessions.get_store(request=self.request)
    try:
	  # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
	  self.session_store.save_sessions(self.response)
      
  @webapp2.cached_property
  def session(self):
    backend = "securecookie" # other options are "secure", "datastore" and "memcache"
    return self.session_store.get_session(backend=backend)

  @classmethod
  def logged_in(cls, handler_method):
    # This decorator requires a logged-in user, and returns 403 otherwise.
    def auth_required(self, *args, **kwargs):
      if (users.get_current_user() or self.request.headers.get('X-AppEngine-Cron')):
        handler_method(self, *args, **kwargs)
      else:
        error(403)
    return auth_required

  @classmethod
  def is_user_admin(cls, handler_method):
    # This decorator requires a logged-in administrator, and returns 403 otherwise.
    def auth_admin_required(self, *args, **kwargs):
      if (users.is_current_user_admin() or self.request.get('X-AppEngine-Cron')):
        handler_method(self, *args, **kwargs)
      else:
        self.error(403)
    return auth_admin_required

  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def render_template(self, filename, template_args):
    self.response.write(self.jinja2.render_template(filename, **template_args))

  def render_json(self, response):
    self.response.write("%s(%s);" % (self.request.GET['callback'], json.dumps(response)))

  def getLoginLink(self):
    """Generate login or logout link and text, depending upon the logged-in status of the client."""
    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'
    return (url, url_linktext)

  def randomString(num):
    letters = list("abcdefghijkmnopqrstuvwxyz23456789")
    pw = ''.join([random.choice(letters) for i in xrange(num)])
    return str(pw)
  
  def userCreate(self):
    letters = list("abcdefghijkmnopqrstuvwxyz23456789")
    randomID = ''.join([random.choice(letters) for i in xrange(16)])
    self.session['thelevel_client_project'] = randomID
    the_user = Users(id=randomID) 
    the_user.user_id = randomID
    the_user.ip = self.request.remote_addr
    # Do this in a task to speed up?
    the_user.put()
    #return the_user
    return {'the_user':the_user}

''' turn off for a bit while testing so I see the debug mode error codes 
  def handle_exception(self, exception, debug):
      # Log the error.
      import logging
      logging.exception(exception)
      # Set a custom message.
      self.response.write('An error occurred.')
      # If the exception is a HTTPException, use its error code.
      # Otherwise use a generic 500 error code.
      if isinstance(exception, webapp2.HTTPException):
          self.response.set_status(exception.code)
      else:
          self.response.set_status(500)
      '''
      



