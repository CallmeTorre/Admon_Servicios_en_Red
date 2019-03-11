import base64
import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey='YOUR_API_KEY')
from_email = Email("example@hotmail.com")
to_email = Email("example@outlook.com")
subject = "Notificación"
content = Content("text/plain", "This is a test")

with open('//Users/Callmetorre/Desktop/Admon_Servicios_en_Red/P1/data/images/linux.png','rb') as f:
    data = f.read()
    f.close()
encoded = base64.b64encode(data).decode()
attachment = Attachment()
attachment.content = encoded
attachment.type = "image/png"
attachment.filename = "cositas.png"
attachment.disposition = "attachment"
attachment.content_id = "ASD"

mail = Mail(from_email, subject, to_email, content)
mail.add_attachment(attachment)

response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)