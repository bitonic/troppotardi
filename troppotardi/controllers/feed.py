import logging
from datetime import datetime
from webhelpers.feedgenerator import Atom1Feed

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from troppotardi.lib.base import BaseController, render
from troppotardi.model import Image
from troppotardi.lib.mapping import day_to_str

log = logging.getLogger(__name__)

class FeedController(BaseController):

    def index(self):
        """ Feed with the last images """
        feed = Atom1Feed(
            title="troppotardi.com Image Feed",
            link=url.current(qualified=True),
            description="The last 10 entries from troppotardi.com",
            language="en",
            )

        images = Image.by_day(self.db,
                              startkey=day_to_str(datetime.utcnow()),
                              descending=True,
                              limit=10)
        
        for image in images:
            feed.add_item(title=image.author + ", " + day_to_str(image.day),
                          link=url(controller='images',
                                   action='show',
                                   day=day_to_str(image.day),
                                   qualified=True),
                          description="Image of the day by " + (image.author_url and ("<a href=\"" + image.author_url + "\">" + image.author + "</a>") or image.author),
                          date=image.day,
                          )

        response.content_type = 'application/atom+xml'

        return feed.writeString('utf-8')
