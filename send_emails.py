#!/usr/bin/python
from setup_config import setup_config
from couchdb import Database
from pylons import config
from troppotardi.model import Email
from troppotardi.lib.utils import send_email

if __name__ == '__main__':
    setup_config()

    # Set up the database
    db = Database(config['couchdb_uri'])
    emails = Email.by_time(db)


    for email in emails:
        send_email(body=email.text,
                   subject=email.subject,
                   recipients=email.recipients,
                   sender=email.sender)
        db.delete(email)
