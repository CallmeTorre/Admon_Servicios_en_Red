import sendgrid
import os
from sendgrid.helpers.mail import *

sg = sendgrid.SendGridAPIClient(apikey='YOUR_API_KEY')
from_email = Email("test@example.com")
to_email = Email("test@oexample.com")
subject = "Notificación"
content = Content("text/plain", "This is a test")
mail = Mail(from_email, subject, to_email, content)
response = sg.client.mail.send.post(request_body=mail.get())
print(response.status_code)
print(response.body)
print(response.headers)