"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render
import pylons

from couchdb import Database
import cgi

#from troppotardi.model import Image, User

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        
        # Set up the database object
        pylons.tmpl_context.db = self.db = Database(pylons.config['couchdb_uri'])

        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        return WSGIController.__call__(self, environ, start_response)
