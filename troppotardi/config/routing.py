"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('index', '/', controller='pages', action='index', page='home')
    map.connect('home', '/home', controller='pages', action='index', page='home')
    map.connect('months', '/months/{year}/{month}', controller='images', action='months')
    map.connect('show_image', '/image/{day}', controller='images', action='show')
    map.connect('last', '/images/last', controller='images', action='last')
    map.connect('page', '/pages/{page}', controller='pages', action='index')
    map.connect('feed', '/feed.atom', controller='feed', action='index')
    
    map.connect('admin_home', '/admin/', controller='admin', action='index')

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map
