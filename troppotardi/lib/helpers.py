"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
from webhelpers.html.tags import *
from webhelpers.html.builder import literal
from webhelpers.pylonslib import Flash as _Flash
from pylons import config
from troppotardi.lib import thumbnailer
from troppotardi.lib.mapping import day_to_str

flash = _Flash()

from pylons import url

def google_analytics():
    script = '\n<script type="text/javascript">\n\n  var _gaq = _gaq || [];\n  _gaq.push([\'_setAccount\', \'' + config['analytics_id'] + '\']);\n  _gaq.push([\'_trackPageview\']);\n\n  (function() {\n    var ga = document.createElement(\'script\'); ga.type = \'text/javascript\'; ga.async = true;\n    ga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\n    var s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(ga, s);\n  })();\n\n</script>'
    return literal(script)

def reinvigorate():
    script = '<script type="text/javascript" src="http://include.reinvigorate.net/re_.js"></script>\n<script type="text/javascript">\ntry {\nreinvigorate.track("' + config['reinvigorate_id'] + '");\n} catch(err) {}\n</script>'
    return literal(script)

def ordinal(value):
    try:
        value = int(value)
    except ValueError:
        return value

    if value % 100//10 != 1:
        if value % 10 == 1:
            ordval = u"%d%s" % (value, "st")
        elif value % 10 == 2:
            ordval = u"%d%s" % (value, "nd")
        elif value % 10 == 3:
            ordval = u"%d%s" % (value, "rd")
        else:
            ordval = u"%d%s" % (value, "th")
    else:
        ordval = u"%d%s" % (value, "th")

    return ordval
