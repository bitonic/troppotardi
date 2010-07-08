"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
from webhelpers.html.tags import *
from webhelpers.html.builder import literal
from webhelpers.pylonslib import Flash as _Flash
from pylons import config
from troppotardi.lib.image_utils import *
from troppotardi.lib.mapping import day_to_str

flash = _Flash()

from pylons import url

def google_analytics():
    return literal("<script type=\"text/javascript\">var _gaq = _gaq || []; _gaq.push(['_setAccount', '" + config['analytics_id'] + "']); _gaq.push(['_trackPageview']); (function() {var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true; ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js'; var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);})();</script>")
