import logging
from datetime import datetime

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect
from pylons.decorators.rest import restrict, dispatch_on
from pylons.decorators import validate

from couchdb.mapping import DateTimeField

from troppotardi.lib.base import BaseController, render
from troppotardi.lib import return_to
from troppotardi.lib.helpers import flash
from troppotardi.model.forms import ImageSubmit
from troppotardi.model import Image
from troppotardi.lib.mapping import day_to_str

log = logging.getLogger(__name__)

class ImagesController(BaseController):

    def show(self, day):
        c.image = list(Image.by_day(self.db, startkey=day))[0]

        olders = list(Image.by_day(self.db,
                                   descending=True,
                                   limit=2,
                                   startkey=day))
        if len(olders) > 1:
            c.older = day_to_str(olders[1].day)
            
        newers = list(Image.by_day(self.db,
                                   limit=2,
                                   startkey=day))

        if (len(newers) > 1) and (datetime.utcnow() >= newers[1].day):
            c.newer = day_to_str(newers[1].day)
            
        session['return_to'] = url(controller='images', action='show', day=day)

        return render('/images/show.mako')

    def months(self):
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
        image.text = self.form_result.get('text')

        image_file = self.form_result.get('image_file').file
        image.store(self.db, image_file=image_file)
        
        flash('Image submitted correctly')
        
        return_to(url('last'))
    
    def last(self):
        day = list(Image.by_day(self.db,
                                limit=1,
                                startkey=day_to_str(datetime.utcnow())))[0].day

        redirect(url(controller='images', action='show', day=day_to_str(day)))
