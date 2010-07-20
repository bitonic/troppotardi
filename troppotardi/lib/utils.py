import string
import random
import smtplib
from email import Header
from email.mime.text import MIMEText
from pylons import config, request
from hashlib import sha1

def generate_password(size=None):
    if not size:
        size = random.randint(8, 12)

    return ''.join([random.choice(string.letters + string.digits)
                    for i in range(size)])

def hash_password(plain_text):
    return sha1(plain_text).hexdigest()
    
def send_email(body, subject, recipients, sender=None):
    """Send an email.

    All arguments should be Unicode strings (plain ASCII works as well).

    Only the real name part of sender and recipient addresses may contain
    non-ASCII characters.

    The email will be properly MIME encoded and delivered though SMTP to
    localhost port 25.  This is easy to change if you want something different.

    The charset of the email will be the first one out of US-ASCII, ISO-8859-1
    and UTF-8 that can represent all the characters occurring in the email.
    Thanks to http://mg.pov.lt/blog/unicode-emails-in-python.html
    """
    
    # Fallback to default sender
    if not sender:
        sender = config['smtp_email']
    
    # Header class is smart enough to try US-ASCII, then the charset we
    # provide, then fall back to UTF-8.
    header_charset = 'ISO-8859-1'

    # We must choose the body charset manually
    for body_charset in 'US-ASCII', 'ISO-8859-1', 'UTF-8':
        try:
            body.encode(body_charset)
        except UnicodeError:
            pass
        else:
            break

    # Make sure email addresses do not contain non-ASCII characters
    sender = sender.encode('ascii')
    recipients = [recipient.encode('ascii') for recipient in recipients]

    # Sends the email through SSL
    msg = MIMEText(body.encode(body_charset), 'plain', body_charset)
    msg['Subject'] = subject.encode('ascii')
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
    server.login(config['smtp_username'], config['smtp_password'])

    server.sendmail(sender, recipients, msg.as_string())
    server.quit()

def visitor_ip():
    """Function to get the visitor ip, necessary becaue if I use
    nginx with paster behind it all requests appear to be from
    127.0.0.1, and so I set the X-real-ip header"""
    if 'HTTP_X_REAL_IP' in request.environ:
        return request.environ['HTTP_X_REAL_IP']
    return request
