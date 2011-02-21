import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict, dispatch_on
from pylons.decorators import validate
from pylons.decorators.rest import restrict, dispatch_on

from troppotardi.lib.base import BaseController, render
from troppotardi.model import User
from troppotardi.model.forms import Login, CpForm
from troppotardi.lib.helpers import flash
from troppotardi.lib import authorize

log = logging.getLogger(__name__)

class UsersController(BaseController):

    @dispatch_on(POST='_dologin')
    def login(self):
        return render('/users/login.mako')

    @authorize('logged_in')
    def logout(self):
        if 'user' in session:
            del session['user']
            session.save()
        if 'redirect_to' in session:
            redirect(session['redirect_to'])
        else:
            redirect(url('home'))

    @authorize('logged_in')
    @dispatch_on(POST='_docp')
    def cp(self):
        return render('/users/cp.mako')
        
    @authorize('logged_in')
    @restrict('POST')
    @validate(schema=CpForm(), form='cp')
    def _docp(self):
        session['user'].password = self.form_result.get('newpassword')
        session['user'].store(self.db)
        session.save()
        flash('Changes were successful')
        redirect(url(controller='users', action='cp'))

    @restrict('POST')
    @validate(schema=Login(), form='login')
    def _dologin(self):
        session['user'] = list(User.by_username(self.db)[self.form_result['username']])[0]
        session.save()
        flash('Login successful')

        if 'redirect_to' in session:
            redir_url = session['redirect_to']
            del session['redirect_to']
            session.save()
            redirect(redir_url)
        else:
            redirect(url('home'))
