import os
import base64
import sendgrid
import datetime
import urllib.request as urllib
from threading import Thread
from sendgrid.helpers.mail import *

last_email = None
elapsed_minutes = 0

def sendemail(typedata, threshold, imagepath):
    global last_email
    global elapsed_minutes

    if last_email:
        current_time = datetime.datetime.now()
        elapsed_minutes = (current_time - last_email) // datetime.timedelta(seconds=60)

    if not last_email:
        elapsed_minutes = 5

    if elapsed_minutes >= 5:
        sg = sendgrid.SendGridAPIClient(apikey='API')
        from_email = Email("email@hotmail.com")
        to_email = Email("email@gmail.com")
        subject = "Notificación"
        content = Content("text/plain", "El tipo de dato " + typedata + " a sobrepasado el " + threshold + "%")
        with open(imagepath,'rb') as f:
            data = f.read()
            f.close()
        encoded = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.content = encoded
        attachment.type = "image/png"
        attachment.filename = "graph.png"
        attachment.disposition = "attachment"
        attachment.content_id = "ASD"
        mail = Mail(from_email, subject, to_email, content)
        mail.add_attachment(attachment)
        try:
            response = sg.client.mail.send.post(request_body=mail.get())
        except urllib.HTTPError as e:
            print(e.read())
        last_email = datetime.datetime.now().time()
        print(response.status_code)
        last_email = datetime.datetime.now()
        print("Email Sended")

def asyncsendAb(imagepath, time):

    sg = sendgrid.SendGridAPIClient(apikey='API')
    from_email = Email("email@hotmail.com")
    to_email = Email("email@gmail.com")
    subject = "Notificación"
    content = Content("text/plain", "Fallas encontradas en " + time)
    with open(imagepath,'rb') as f:
        data = f.read()
        f.close()
    encoded = base64.b64encode(data).decode()
    attachment = Attachment()
    attachment.content = encoded
    attachment.type = "image/png"
    attachment.filename = "graph.png"
    attachment.disposition = "attachment"
    attachment.content_id = "ASD"
    mail = Mail(from_email, subject, to_email, content)
    mail.add_attachment(attachment)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
    except urllib.HTTPError as e:
        print(e.read())
    last_email = datetime.datetime.now().time()
    print(response.status_code)
    last_email = datetime.datetime.now()
    print("Email Sended")

def asyncsend(typedata, threshold, imagepath):
    thread = Thread(target=sendemail, args=(typedata, threshold, imagepath), daemon=True).start()

def asyncsendAb(imagepath, time):
    Thread(target=sendemailAb, args=(imagepath, time), daemon=True).start()