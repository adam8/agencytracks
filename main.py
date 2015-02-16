from views import *
import webapp2
from webapp2_extras.routes import RedirectRoute

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'raindrops-keep-fallin-on-yer-heads!!!!!!',
    'cookie_name': 'thelevel_client_project'
}
# Using RedirectRoute for strict_slash
application_routes = [ 
  RedirectRoute(r'/', HomeHandler, 'HomeHandler', strict_slash=True),
  RedirectRoute(r'/dashboard/<client>/notes/<user>', NotesClientDashboardHandler, 'NotesClientDashboardHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/notes/<user>', NotesHandler, 'NotesHandler', strict_slash=True),
  RedirectRoute(r'/dashboard/<client>', DashboardClientHandler, 'DashboardClientHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/steps/<item_keyname>', StepsAjaxHandler, 'StepsAjaxHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/tasks/delete/<victim>', TasksDeleteHandler, 'TasksDeleteHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/tasks/order', TaskOrderHandler, 'TaskOrderHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/tasks/<task_id>', TasksHandler, 'TasksHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/tasks', TasksHandler, 'TasksHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/questionnaire', QuestionnaireHandler, 'QuestionnaireHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/questionnaire-init', QuestionnaireInitHandler, 'QuestionnaireInitHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/widget', WidgetHandler, 'WidgetHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/widget/order', WidgetOrderHandler, 'WidgetOrderHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/widget/<widget_id>', WidgetHandler, 'WidgetHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/widget-update/<widget_id>', WidgetUpdateHandler, 'WidgetUpdateHandler', strict_slash=True),
  RedirectRoute(r'/clients/delete', ClientsDeleteHandler, 'ClientsDeleteHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/edit', ClientsHandler, 'ClientsHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>/users', ClientsUsersHandler, 'ClientsUsersHandler', strict_slash=True),
  RedirectRoute(r'/steps/task/new', StepsTaskHandler, 'StepsTaskHandler', strict_slash=True),
  RedirectRoute(r'/steps/delete', StepsDeleteHandler, 'StepsDeleteHandler', strict_slash=True),
  RedirectRoute(r'/steps/<step_keyname>', StepsHandler, 'StepsHandler', strict_slash=True),
  RedirectRoute(r'/steps', StepsHandler, 'StepsHandler', strict_slash=True),
  RedirectRoute(r'/clients/<client>', DashboardTheLevelHandler, 'DashboardTheLevelHandler', strict_slash=True),
  RedirectRoute(r'/clients', ClientsHandler, 'ClientsHandler', strict_slash=True)
]

application = webapp2.WSGIApplication(routes=application_routes, config=config, debug=True)
