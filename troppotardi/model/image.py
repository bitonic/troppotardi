import couchdb.mapping as mapping
from datetime import datetime, timedelta
import os
import shutil
import imghdr
from PIL import Image as PILImage
import webhelpers.html.tags as tags
from webhelpers.html.builder import make_tag
from pylons import config, session, tmpl_context, request, url as pylons_url

from troppotardi.lib.base import render
from troppotardi.lib.mapping import DayField, day_to_str
from troppotardi.lib.image_utils import thumbnailer
from troppotardi.lib.utils import send_email

class Image(mapping.Document):
    type = mapping.TextField(default='Image')

    text = mapping.TextField()
    author = mapping.TextField()
    author_url = mapping.TextField()
    author_ip = mapping.TextField()
    author_email = mapping.TextField()

    submitted = mapping.DateTimeField()
    day = DayField()
    prev_day = DayField()
    revised_by = mapping.TextField()
    state = mapping.TextField(default='pending')

    filename = mapping.TextField()

    @property
    def path(self):
        """Returns the full path to the image"""
        return os.path.join(config['images_dir'], self.filename)
    
    @property
    def url(self):
        """Returns the (relative, without the domain) url"""
        return os.path.join(config['images_base_url'], self.filename)

    @property
    def pending(self):
        return self.state == 'pending'

    @property
    def accepted(self):
        return self.state == 'accepted'

    def __init__(self, **kwargs):
        super(Image, self).__init__()
        
        # Assign every kwarg to self
        for k in kwargs:
            setattr(self, k, kwargs[k])
            
    def admin_thumb(self, max_width=None, max_height=None):
        """Returns an <img> tag for the listings in the admin page"""
        if self.filename:
            image = PILImage.open(self.path)
            (width, height) = image.size
            
            if max_width and width > max_width:
                thumb = thumbnailer(self.filename, max_width=max_width)
            if max_height and height > max_height:
                thumb = thumbnailer(self.filename, max_height=max_height)
            return make_tag('a', href=self.url, c=tags.image(thumb, None))

    def store(self, db, image_file=None):
        # Record the date of submission and the ip of the submitter
        if not self.submitted:
            self.submitted = datetime.utcnow()
            self.author_ip = request.environ['REMOTE_ADDR']


        if self.accepted:
            if self.day:
                # We check that that's the only image we have that day
                days = list(Image.by_day(db,
                                         descending=True,
                                         startkey=day_to_str(self.day),
                                         limit=2))
                # If there is more than one image on that day, we reschedule it.
                if len(days) > 1:
                    self.schedule(db)
            else:
                self.schedule(db)

        # Send the email only if the image is accepted
        # and if we have an email, of course
        if self.accepted and self.author_email:
            # If there is no previous day, then it means that we are scheduling
            # the image for the first time.
            if not self.prev_day:
                # Sends the email
                tmpl_context.day = self.day
                tmpl_context.author = self.author
                tmpl_context.image_url = pylons_url(str(self.url), qualified=True)
                send_email(render('/emails/accepted.mako'),
                           'troppotardi.com',
                           [self.author_email])
            # Else, we are rescheduling it.
            elif self.prev_day != self.day:
                # Sends the reschedule email
                tmpl_context.day = self.day
                tmpl_context.author = self.author
                tmpl_context.image_url = pylons_url(str(self.url), qualified=True)
                send_email(render('/emails/accepted_again.mako'),
                           'troppotardi.com',
                           [self.author_email])
            # Now we can set the prev_day to the present day
            self.prev_day = self.day

        # If there is a user in the session, store it in the revision
        if 'user' in session:
            self.revised_by = session['user'].id

        # Store it in the database.
        super(Image, self).store(db)

        # Save the image file. We do it afterwards storing the image
        # because we use the id as a filename, and we need to store the image
        # first to get an id.
        if image_file:
            self.store_file(image_file, self.id, db)

        return self

    def store_file(self, image_file, new_filename, db):
        # Get the image format...
        format = imghdr.what(image_file)
        # Only png and jpeg files. There is already a check with the validator
        # but you never know (:
        if format in ['png', 'jpeg']:
            
            self.filename = new_filename + '.' + format
            # Store again with the filename
            super(Image, self).store(db)
            
            # Open the new file
            permanent_file = open(self.path, 'w')
                
            # Copy the temp file to its destination
            shutil.copyfileobj(image_file, permanent_file)
            image_file.close() # close everything
            permanent_file.close()

    def schedule(self, db):
        """Schedules the image to the first available day"""
        today = datetime.utcnow()
        today = datetime(today.year, today.month, today.day)
        
        # Get the image with the futuremost day
        days = list(Image.by_day(db, descending=True, limit=1))
        
        # If that day is before then today, or if there are no images at
        # all, schedule it for today
        if (days and (days[0].day < today)) or (not days):
            self.day = today
        # Else, schedule it for the day after that day
        else:
            last_day = days[0].day
            self.day = datetime(last_day.year, last_day.month,
                                last_day.day) + timedelta(days=1)
            
    def delete(self, db):
        # Puts the image in the 'deleted' state
        self.state = 'deleted'
        self.store(db)

    def delete_permanently(self, db):
        # Removes image document AND files.
        full_filename = os.path.join(config['images_dir'], self.filename)
        os.remove(full_filename)

        # Delete thumbs
        thumbs_list = [file for file in [files for root, dirs, files in
                                         os.walk(config['thumbs_dir'])][0]]
        (name, _) = os.path.splitext(self.filename)
        thumbs_list = filter(lambda fn: fn.startswith(name + '_'), thumbs_list)
        for file in thumbs_list:
            os.remove(os.path.join(config['thumbs_dir'], file))

        # Delete the actual document
        db.delete(self)

    # The possible states
    states = ['accepted', 'pending', 'deleted']

    pending_by_time = mapping.ViewField('images', '''
        function(doc) {
            if (doc.type == 'Image' && doc.state == 'pending') {
                emit(doc.submitted, doc);
            }
        }''')
    
    deleted_by_time = mapping.ViewField('images', '''
        function(doc) {
            if (doc.type == 'Image' && doc.state == 'deleted') {
               emit(doc.submitted, doc);
            }
        }''')

    by_day = mapping.ViewField('images', '''
        function(doc) {
           if (doc.type == 'Image' && doc.state == 'accepted') {
               emit(doc.day, {
                   author: doc.author,
                   author_url: doc.author_url,
                   text: doc.text,
                   filename: doc.filename,
                   day: doc.day,
                   author_email: doc.author_email,
                   submitted: doc.submitted,
               });
           }
        }''')
