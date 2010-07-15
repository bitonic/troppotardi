import couchdb.mapping as mapping
from datetime import datetime

class Email(mapping.Document):
    type = mapping.TextField(default='Email')

    text = mapping.TextField()
    subject = mapping.TextField()
    recipients = mapping.ListField(mapping.TextField)
    sender = mapping.TextField()
    issued = mapping.DateTimeField()

    def __init__(self, **kwargs):
        super(Email, self).__init__()

        for k in kwargs:
            setattr(self, k, kwargs[k])

    def store(self, db):
        if not self.issued:
            self.issued = datetime.utcnow()

        super(Email, self).store(db)

        return self

    by_time = mapping.ViewField('emails', '''
        function(doc) {
            if (doc.type == 'Email') {
                emit(doc.issued, doc);
            }
        }''')
