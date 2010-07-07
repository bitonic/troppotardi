from pylons import session, url, request
from pylons.controllers.util import redirect, abort
from decorator import decorator

def authorize(permission):
    
    def validator(func, *args, **kwargs):
        if 'user' not in session:
            session['redirect_to'] = request.environ.get('PATH_INFO')
            if request.environ.get('QUERY_STRING'):
                session['redirect_to'] += '?' + request.environ['QUERY_STRING']

            redirect(url(controller='users', action='login'))

        if not session['user'].has_permission(permission):
            abort(403)
            
        return func(*args, **kwargs)

    return decorator(validator)
