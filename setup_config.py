from pylons import config
from paste.deploy import appconfig

def setup_config():
    # Gets the config
    conf = appconfig('config:prod.ini', relative_to='/home/astroboy/proj/troppotardi/')
    config.push_process_config(conf.local_conf)
