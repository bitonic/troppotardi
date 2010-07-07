import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from troppotardi.lib.base import BaseController, render

log = logging.getLogger(__name__)

class PagesController(BaseController):

    def index(self, page):
        return render('/pages/' + page + '.mako')
