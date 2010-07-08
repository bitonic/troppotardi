from pylons import session, url, request
from pylons.controllers.util import redirect, abort
from decorator import decorator

def authorize(permission):
    """Given a permission, checks if the user is authorized"""
    def validator(func, *args, **kwargs):
        # If the visitor is not logged in, redirect him to the login page
        if 'user' not in session:
            session['redirect_to'] = request.environ.get('PATH_INFO')
            if request.environ.get('QUERY_STRING'):
                session['redirect_to'] += '?' + request.environ['QUERY_STRING']

            redirect(url(controller='users', action='login'))

        # If the user doesn't have permission, abort with 403 error
        if not session['user'].has_permission(permission):
            abort(403)
            
        return func(*args, **kwargs)

    return decorator(validator)
