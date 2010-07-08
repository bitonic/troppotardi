from webob import Request
from webob.exc import HTTPBadRequest

class LimitUploadSize(object):
    """Class to include in the middleware that limits the
    upload size."""

    def __init__(self, app, size):
        self.app = app
        self.size = size
        
    def __call__(self, environ, start_response):
        req = Request(environ)
        if req.method=='POST':
            len = req.headers.get('Content-length')
            if not len:
                return HTTPBadRequest("No content-length header specified")(environ, start_response)
            elif int(len) > self.size:
                return HTTPBadRequest("POST body exceeds maximum limits")(environ, start_response)
        resp = req.get_response(self.app)
        return resp(environ, start_response)
