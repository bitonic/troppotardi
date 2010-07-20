1) Install couchdb
2) Create a database
3) Configure config.ini
4) Change setup_conf.py replacing prod.ini with your config file, and adding to cron send_emails and compact_database
4) Install the required dependencies (python setup.py develop)
5) Sync the database: paster setup-app config.ini
6) Run it: paster serve --reload config.ini
