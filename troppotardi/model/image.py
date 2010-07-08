import couchdb.mapping as mapping
from datetime import datetime, timedelta
import os
import shutil
import imghdr
from PIL import Image as PILImage
import webhelpers.html.tags as tags
from webhelpers.html.builder import make_tag
from pylons import config, session, tmpl_context, request

from troppotardi.lib.mapping import DayField
from troppotardi.lib.image_utils import thumbnailer

class Image(mapping.Document):
    type = mapping.TextField(default='Image')

    text = mapping.TextField()
    author = mapping.TextField()
    author_url = mapping.TextField()
    author_ip = mapping.TextField()

    submitted = mapping.DateTimeField()
    day = DayField()
    revised_by = mapping.TextField()

    filename = mapping.TextField()

    @property
    def path(self):
        """Returns the full path to the image"""
        return os.path.join(config['images_dir'], self.filename)
    
    @property
    def url(self):
        """Returns the (relative, without the domain) url"""
        return os.path.join(config['images_base_url'], self.filename)

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

    def store(self, db, accept=False, image_file=None):
        # Record the date of submission and the ip of the submitter
        if not self.submitted:
            self.submitted = datetime.utcnow()
            self.author_ip = request.environ['REMOTE_ADDR']

        # If the accept argument is passed, we schedule it for the
        # next available day
        if accept:
            today = datetime.utcnow()
            today = datetime(today.year, today.month, today.day)
            
            # Get the image with the futuremost day
            days = list(Image.by_day(tmpl_context.db, descending=True, limit=1))
            
            # If that day is before then today, or if there are no images at
            # all, schedule it for today
            if (days and (days[0].day < today)) or (not days):
                self.day = today
            # Else, schedule it for the day after that day
            else:
                last_day = days[0].day
                self.day = datetime(last_day.year, last_day.month,
                                    last_day.day) + timedelta(days=1)

        # If there is a user in the session, store it in the revision
        if 'user' in session:
            self.revised_by = session['user'].id

        # Store it in the database.
        super(Image, self).store(db)

        # Save the image file. We do it afterwards storing the image
        # because we use the id as a filename, and we need to store the image
        # first to get an id.
        if image_file:
            # Get the image format...
            format = imghdr.what(image_file)
            # Only png and jpeg files. There is already a check with the validator
            # but you never know (:
            if format == 'png' or format == 'jpeg':

                self.filename = self.id + '.' + format
                # Store again with the filename
                super(Image, self).store(db)
                
                # Open the new file
                permanent_file = open(self.path, 'w')
                
                # Copy the temp file to its destination
                shutil.copyfileobj(image_file, permanent_file)
                image_file.close() # close everything
                permanent_file.close()


        return self
        
    def delete(self, db):
        # Delete image file
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

    pending_by_time = mapping.ViewField('images', '''
        function(doc) {
            if (doc.type == 'Image' && !doc.day) {
                emit(doc.submitted, doc);
            }
        }''')

    by_day = mapping.ViewField('images', '''
        function(doc) {
           if (doc.type == 'Image' && doc.day) {
               emit(doc.day, {
                   author: doc.author,
                   author_url: doc.author_url,
                   text: doc.text,
                   filename: doc.filename,
                   day: doc.day,
               });
           }
        }''')

    by_month = mapping.ViewField('images', '''
        function(doc) {
            if (doc.type == 'Image' && doc.day) {
                var year = parseInt(doc.submitted.substr(0, 4), 10);
                var month = parseInt(doc.submitted.substr(5, 2), 10);
                emit([year, month, doc.day], {
                    author: doc.author, filename: doc.filename,
                    author_url: doc.author_url, day: doc.day,
                });
            }
        }''')
