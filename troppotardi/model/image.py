import couchdb.mapping as mapping
from datetime import datetime, timedelta
import os
import shutil
import imghdr
from PIL import Image as PILImage
import webhelpers.html.tags as tags
from webhelpers.html.builder import make_tag
from pylons import config, session, tmpl_context

from troppotardi.lib.helpers import image_url, image_path
from troppotardi.lib import slugify
from troppotardi.lib.mapping import DayField

class Image(mapping.Document):
    type = mapping.TextField(default='Image')

    text = mapping.TextField()
    author = mapping.TextField()
    author_url = mapping.TextField()

    submitted = mapping.DateTimeField()
    day = DayField()
    revised_by = mapping.TextField()

    filename = mapping.TextField()

    @property
    def path(self):
        return image_path(self.filename)
    
    @property
    def url(self):
        return image_url(self.filename)

    def __init__(self, **kwargs):
        super(Image, self).__init__()
        
        for k in kwargs:
            setattr(self, k, kwargs[k])
            
    def admin_thumb(self, max_width=None, max_height=None):
        """Returns an <img> tag for the listings in the admin page"""
        if self.filename:
            image = PILImage.open(self.path)
            (width, height) = image.size
            if max_width and width > max_width:
                height = height * max_width / width
                width = max_width
            if max_height and height > max_height:
                width = width * max_height / height
                height = max_height
            return make_tag('a', href=self.url,
                            c=tags.image(self.url, None, width=width, height=height))

    def store(self, db, accept=False, image_file=None, revised_by=None):
        if not self.submitted:
            self.submitted = datetime.utcnow()

        if accept:
            today = datetime.utcnow()
            today = datetime(today.year, today.month, today.day)
            
            days = list(Image.by_day(tmpl_context.db, descending=True, limit=1))
            if days and (days[0].day < today):
                self.day = today
            elif not days:
                self.day = today
            else:
                last_day = days[0].day
                self.day = datetime(last_day.year, last_day.month,
                                    last_day.day) + timedelta(days=1)

        if revised_by:
            self.revised_by = revised_by.id

        super(Image, self).store(db)

        if image_file:
            self.store_image(image_file)

        return self

    def store_image(self, image_file):
        if image_file:
            format = imghdr.what(image_file)
            if format == 'png' or format == 'jpeg':
                
                """
                # The images are simply numbered from 1.
                # I get the maximum number in the directory +1 and that's the new name.
                
                file_list = [int(os.path.splitext(file)[0])
                             for file in [files for root, dirs, files in
                                          os.walk(config['images_dir'])][0]]
                if file_list:
                    self.filename = max(file_list)
                    self.filename = str(int(self.filename) + 1) + '.' + format
                else:
                    self.filename = '1.' + format
                    """
                self.filename = self.get('_id') + format
                
                permanent_file = open(self.path, 'w')
                
                # Copy the file
                shutil.copyfileobj(image_file, permanent_file)
                image_file.close()
                permanent_file.close()
        
    def delete(self, db):
        # Delete image file
        full_filename = os.path.join(config['images_dir'], self.filename)
        os.remove(full_filename)

        # Delete thumbs
        thumbs_list = [file for file in [files for root, dirs, files in
                                         os.walk(config['thumbs_dir'])][0]]
        (name, _) = os.path.splitext(self.filename)
        thumbs_list = filter(lambda fn: fn.startswith(name + '_'))
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
