from couchdb.mapping import Field
from calendar import timegm
from datetime import datetime
from time import strptime

class DayField(Field):
    """Mapping field to store days in the format %Y-%m-%d
    Ex: 2010-06-21
    """

    def _to_python(self, value):
        if isinstance(value, basestring):
            try:
                timestamp = timegm(strptime(value, '%Y-%m-%d'))
                value = datetime.utcfromtimestamp(timestamp)
            except ValueError:
                raise ValueError('Invalid date %r' % value)
        return value

    def _to_json(self, value):
        return value.strftime('%Y-%m-%d')

def day_to_str(daydate):
    """Helper function that transform the datetime object
    in the string"""
    daydate = daydate.strftime("%Y-%m-%d")
    return daydate

def str_to_day(daystr):
    timestamp = timegm(strptime(daystr, '%Y-%m-%d'))
    return datetime.utcfromtimestamp(timestamp)
