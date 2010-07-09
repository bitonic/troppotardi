import formencode
from formencode import validators
import pylons

from troppotardi.model import User
from troppotardi.model.validators import *

class ImageSubmit(formencode.Schema):
    # images/submit
    allow_extra_fields = True
    filter_extra_fields = False
    image_file = formencode.All(ImageFormat(not_empty=True),
                                ImageSize())
    author = formencode.All(validators.String(not_empty=True),
                            validators.MaxLength(150))
    author_url = validators.URL(add_http=True)
    text = formencode.All(validators.String(),
                          validators.MaxLength(200))
    email = validators.Email()
    pre_validators = [ReCaptcha()]

class Login(formencode.Schema):
    # users/login
    allow_extra_fields = True
    filter_extra_fields = False
    username = validators.String(not_empty=True)
    password = validators.String(not_empty=True)
    chained_validators = [VerifyUser()]



class CpForm(formencode.Schema):
    # users/cp
    allow_extra_fields = True
    filter_extra_fields = False
    chained_validators = [VerifyUser(), validators.FieldsMatch('newpassword', 'confirmpassword')]



class AddUser(formencode.Schema):
    # admin/adduser
    allow_extra_fields = True
    filter_extra_fields = False
    username = formencode.All(validators.String(not_empty=True),
                              UniqueUsername())
    email = validators.Email(not_empty=True)
    role = ExistingRole(not_empty=True)

    
class EditUser(formencode.Schema):
    # admin/edit_user
    allow_extra_fields = True
    username = formencode.All(validators.String(not_empy=True),
                              UniqueUsername())
    email = validators.Email(not_empty=True)
    password = validators.String()
    confirm_password = validators.String()
    role = ExistingRole(not_empty=True)
    chained_validators = [validators.FieldsMatch('password', 'confirm_password')]

class EditImage(formencode.Schema):
    # admin/edit/id
    allow_extra_fields = True
    filter_extra_fields = False
    chained_validators = [UniqueDate()]
