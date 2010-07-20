#!/usr/bin/python
from setup_config import setup_config
from pylons import config
from couchdb import Database

if __name__ == '__main__':
    setup_config()

    db = Database(config['couchdb_uri'])
    db.compact()
    db.compact('images')
    db.compact('users')
    db.compact('emails')

