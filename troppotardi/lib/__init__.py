from authorize import authorize
from pylons import session
from pylons.controllers.util import redirect
import re
from troppotardi.lib.upload_size import *

def slugify(aslug):
    aslug = re.sub('[^\w\s-]', '', aslug).strip().lower()
    aslug = re.sub('\s+', '-', aslug)
    return aslug

def return_to(fallback):
    if 'return_to' in session:
        url = session['return_to']
        del session['return_to']
        redirect(url)
    else:
        redirect(fallback)
    
