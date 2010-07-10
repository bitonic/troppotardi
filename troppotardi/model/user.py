import couchdb.mapping as mapping
from datetime import datetime
from troppotardi.lib.utils import hash_password
from pylons import session

class User(mapping.Document):
    type = mapping.TextField(default='User')
    
    username = mapping.TextField()
    email = mapping.TextField()
    hashed_password = mapping.TextField()
    role = mapping.TextField()
    
    created = mapping.DateTimeField()
    revised_by = mapping.TextField()
    
    def get_password(self):
        return self.hashed_password

    def set_password(self, plain_text):
        self.hashed_password = hash_password(plain_text)

    password = property(get_password, set_password)
    
    def check_password(self, plain_text):
        return hash_password(plain_text) == self.hashed_password
        
    def has_permission(self, permission):
        return (permission == 'logged_in') or (self.role in User.permissions[permission])

    def store(self, db, revised_by=None):
        if not self.created:
            self.created = datetime.utcnow()

        if revised_by:
            self.revised_by = revised_by.id

        super(User, self).store(db)

        # Updates the user object in the session
        if 'user' in pylons.session:
            if not pylons.session['user']:
                del pylons.session['user']
            else:
                pylons.session['user'] = User.load(self.db, pylons.session['user'].id)

        return self
    
    by_time = mapping.ViewField('users', '''
        function(doc) {
            if (doc.type == 'User') {
                emit(doc.created, doc);
            }
        }''')
    
    by_username = mapping.ViewField('users', '''
        function(doc) {
            if (doc.type == 'User') {
                emit(doc.username, doc);
            }
        }''')

    # The roles should be in order of "powerfulness"
    roles = ['Admin', 'Reviewer']
    permissions = {
        'review_images': ['Admin', 'Reviewer'],
        'manage_users': ['Admin'],
        'delete_images': ['Admin'],
        }
