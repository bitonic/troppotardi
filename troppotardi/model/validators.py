import formencode
import pylons
import os
import imghdr
from datetime import datetime
from PIL import Image as PILImage

from pylons import tmpl_context
from troppotardi.model import User, Image
from troppotardi.lib.mapping import day_to_str

class ImageFormat(formencode.FancyValidator):
    """Verifies that the image submitted is an image"""
    def _to_python(self, value, state):
        image_type = imghdr.what(value.file)

        if not (image_type == 'png' or image_type == 'jpeg'):
            raise formencode.Invalid(
                'The file you submitted is not a image',
                value, state)
        return value

class ImageSize(formencode.FancyValidator):
    """Checks that the size of the image is appropriate"""
    def _to_python(self, value, state):
        value.file.seek(0, 2)
        if value.file.tell() > int(pylons.config['images_max_size']):
            raise formencode.Invalid(
                'Images must be smaller than 2MB',
                value, state)
        value.file.seek(0, 0)

        """
        im = PILImage.open(value.file)
        (width, height) = im.size
        
        if width < 500 or height < 500:
            raise formencode.Invalid(
                'The image must be at least 500 by 500 pixels.',
                value, state)
                """
                
        return value

class VerifyUser(formencode.FancyValidator):
    def validate_python(self, field_dict, state):
        users = User.by_username(pylons.tmpl_context.db)[field_dict['username']]
        users = list(users)
        if not users:
            raise formencode.Invalid(
                'Invalid username.',
                field_dict, state)

        user = users[0]
        if not user.check_password(field_dict['password']):
            raise formencode.Invalid(
                'Wrong password.',
                field_dict, state)

class UniqueUsername(formencode.FancyValidator):
    def _to_python(self, value, state):
        user = User.by_username(pylons.tmpl_context.db)[value]

        if user:
            raise formencode.Invalid(
                'The username you selected already exists.',
                value, state)
        return value

class ExistingRole(formencode.FancyValidator):
    def _to_python(self, value, state):
        if not (value in User.roles):
            raise formencode.Invalid(
                'The role does not exist.',
                value, state)
        return value

class UniqueDate(formencode.FancyValidator):
    def validate_python(self, field_dict, state):
        if 'change_day' in field_dict:
            day = day_to_str(datetime(year=int(field_dict['year']),
                                      month=int(field_dict['month']),
                                      day=int(field_dict['day'])))
            
            imgs = list(Image.by_day(tmpl_context.db, startkey=day, limit=2))
            if imgs and imgs[0].id != field_dict['id'] and day_to_str(imgs[0].day) == day:
                        raise formencode.Invalid(
                            'The day you entered already exists.',
                            field_dict, state)
