import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from troppotardi.lib.base import BaseController, render
from troppotardi.model import Image
from troppotardi.lib.mapping import day_to_str

log = logging.getLogger(__name__)

class PagesController(BaseController):

    def index(self, page):
        return render('/pages/' + page + '.mako')
