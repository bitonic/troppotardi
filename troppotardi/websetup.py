"""Setup the troppotardi application"""
import logging
from couchdb import Database
from couchdb.design import ViewDefinition

import pylons.test

from troppotardi.config.environment import load_environment
from troppotardi.model import Image, User

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup troppotardi here"""
    config = load_environment(conf.global_conf, conf.local_conf)
    
    print "Syncing the couchdb database..."
    db = Database(config['couchdb_uri'])
    ViewDefinition.sync_many(db, [
            Image.pending_by_time, Image.by_day, Image.by_month, Image.deleted_by_time,
            User.by_time, User.by_username,
            ])

    if not list(User.by_username(db)):
        print "Creating first user - username and password \"admin\""
        admin = User()
        admin.username = "admin"
        admin.password = "admin"
        admin.email = "some@email.com"
        admin.role = "Admin"
        admin.store(db, revised_by=False)

    print "Done."
    
