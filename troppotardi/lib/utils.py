import string
import random
import smtplib
from email.mime.text import MIMEText
from pylons import config
from hashlib import sha1

def generate_password(size=None):
    if not size:
        size = random.randint(8, 12)

    return ''.join([random.choice(string.letters + string.digits)
                    for i in range(size)])

def hash_password(plain_text):
    return sha1(plain_text).hexdigest()
    
def send_email(text, subject, recipients, sender=None):
    
    if not sender:
        sender = config['smtp_email']

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    server = smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port'])
    server.login(config['smtp_username'], config['smtp_password'])

    server.sendmail(sender, recipients, msg.as_string())
