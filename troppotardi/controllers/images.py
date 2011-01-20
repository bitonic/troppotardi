import logging
from datetime import datetime
from StringIO import StringIO

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict, dispatch_on
from pylons.decorators import validate

from couchdb.mapping import DateTimeField

from troppotardi.lib.base import BaseController, render
from troppotardi.lib import return_to
from troppotardi.lib.helpers import flash
from troppotardi.lib.thumbnailer import resize_image
from troppotardi.model.forms import ImageSubmit
from troppotardi.model import Image
from troppotardi.lib.mapping import day_to_str, str_to_day

log = logging.getLogger(__name__)

class ImagesController(BaseController):

    def show(self, day):
        if str_to_day(day) > datetime.utcnow():
            abort(404)
        else:
            """Shows a single image"""
            c.image = list(Image.by_day(self.db, startkey=day))[0]
            
            # Gets the older image (if there is one), the startkey is
            # the day of the image and the list is in descending order
            olders = list(Image.by_day(self.db,
                                       descending=True,
                                       limit=2,
                                       startkey=day))
            
            # If there is one store it
            if len(olders) > 1:
                c.older = url(controller='images',
                              action='show',
                              day=day_to_str(olders[1].day),
                              qualified=True)

            # Same thing, but the list is in ascending order for the
            # newer images
            newers = list(Image.by_day(self.db,
                                       limit=2,
                                       startkey=day))

            # We check that the newer image is not in a future date
            if (len(newers) > 1) and (datetime.utcnow() >= newers[1].day):
                c.newer = url(controller='images',
                              action='show',
                              day=day_to_str(newers[1].day),
                              qualified=True)

            session['return_to'] = url(controller='images', action='show', day=day)
            
            return render('/images/show.mako')

    def months(self):
        # Of course we start from the present day (since there could be
        # image scheduled for future days
        c.images = Image.by_day(self.db,
                                descending=True,
                                startkey=day_to_str(datetime.utcnow()))
        return render('/images/months.mako')

    @dispatch_on(POST='_dosubmit')
    def submit(self):
        c.recaptcha_key = config['recaptcha_pubkey']

        return render('/images/submit.mako')
    
    @validate(schema=ImageSubmit(), form='submit')
    def _dosubmit(self):
        
        image = Image()
        
        image.author = self.form_result.get('author')
        image.author_url = self.form_result.get('author_url')
        image.author_email = self.form_result.get('email')
        image.text = self.form_result.get('text')

        image_file = self.form_result.get('image_file').file
        image.store(self.db, image_file=image_file)
        
        flash('Image submitted correctly')
        
        return_to(url('last'))
    
    def last(self):
        # We get the last image from the present day.
        day = list(Image.by_day(self.db,
                                limit=1,
                                startkey=day_to_str(datetime.utcnow()),
                                descending=True))[0].day

        redirect(url(controller='images', action='show', day=day_to_str(day)))

    def display_thumb(self):
        get_params = request.GET

        if not 'image' in get_params:
            abort(500)
        if not ('max_width' in get_params or 'max_height' in get_params):
            abort(500)
            
        if 'max_width' in get_params:
            max_width = int(get_params['max_width'])
        else:
            max_width = None

        if 'max_height' in get_params:
            max_height = int(get_params['max_height'])
        else:
            max_height = None

        im = resize_image(get_params['image'],
                          max_width=max_width,
                          max_height=max_height,
                          )
        
        response.content_type = 'image/' + im.format.lower()

        buffer = StringIO()
        
        im.save(buffer, im.format.upper())

        return buffer.getvalue()

    def xml_list(self):
        c.images = Image.by_day(self.db,
                                descending=True,
                                startkey=day_to_str(datetime.utcnow()))
        return render('/images/xml_list.mako')        
