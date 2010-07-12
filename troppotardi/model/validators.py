import formencode
import pylons
import os
import imghdr
import urllib2, urllib
from datetime import datetime
from PIL import Image as PILImage

from pylons import tmpl_context, request, config
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
        # Checks the file size. There is already a check for 4MB at
        # the request level, but this displays a nicer output for 2MB-4MB
        # files...
        value.file.seek(0, 2)
        if value.file.tell() > int(pylons.config['images_max_size']):
            raise formencode.Invalid(
                'Images must be smaller than 2MB',
                value, state)
        value.file.seek(0, 0)

        # For some reason, this messes up the file. I have to solve this
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
    """Checks the credentials of the user when logging in"""
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
    """Checks that the day you are entering as the scheduled
    day is not already occupied."""
    def validate_python(self, field_dict, state):
        # 'change_day' is a hidden input that sinals that
        # the user can edit the date. This is necessary because
        # if the image is still pending there is no need to check,
        # since there is no day field to edit at all
        if 'change_day' in field_dict:
            day = day_to_str(datetime(year=int(field_dict['year']),
                                      month=int(field_dict['month']),
                                      day=int(field_dict['day'])))
            
            imgs = list(Image.by_day(tmpl_context.db, startkey=day, limit=2))

            # Checks that there are no different images from this with
            # the same day.
            if imgs and imgs[0].id != field_dict['id'] and day_to_str(imgs[0].day) == day:
                        raise formencode.Invalid(
                            'The day you entered already exists.',
                            field_dict, state)

class ReCaptcha(formencode.FancyValidator):
    def validate_python(self, field_dict, state):
        values = {
            'privatekey': config['recaptcha_privkey'],
            'remoteip': request.environ['REMOTE_ADDR'],
            'challenge': field_dict['recaptcha_challenge_field'],
            'response': field_dict['recaptcha_response_field'],
            }
        req = urllib2.urlopen(config['recaptcha_server'],
                              urllib.urlencode(values))
        if req.read().splitlines()[0] != 'true':
            raise formencode.Invalid(
                'Wrong captcha.',
                field_dict, state)
