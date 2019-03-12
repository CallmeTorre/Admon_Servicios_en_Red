import os
import base64
import urllib.request as urllib
from threading import Thread

import sendgrid
from sendgrid.helpers.mail import *

def sendemail(image_path, content):
    sg = sendgrid.SendGridAPIClient(apikey='YOUR_API_KEY')
    from_email = Email("example@hotmail.com")
    to_email = Email("example@outlook.com")
    subject = "Notificación"
    content = Content("text/plain", content)

    with open(image_path,'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.content = encoded
    attachment.type = "image/png"
    attachment.filename = "notification.png"
    attachment.disposition = "attachment"
    attachment.content_id = "notification"

    mail = Mail(from_email, subject, to_email, content)
    mail.add_attachment(attachment)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
    except urllib.HTTPError as e:
        print(e.read())

    print(response.status_code)
    print(response.body)
    print(response.headers)

def asyncsend(image_path, content):
    """
    Same as 'send', but performed in a background thread.

    The thread is automatically started, but not joined on.
    Still, the thread object is returned in case it is
    required.
    """
    thread = Thread(target=sendemail, args=(image_path, content))
    thread.start()
    return thread