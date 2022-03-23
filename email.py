import os
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
load_dotenv()

HOST_ADRESS = os.environ.get('HOST_ADRESS')
SMTP_ADRESS = os.environ.get('SMTP_ADRESS')
SSL_PORT = os.environ.get('SSL_PORT')
EMAIL_ADRESS = os.environ.get('EMAIL_ADRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

context = ssl.create_default_context()

def send_confirmation_email(receiver: str, code: str):
    message = MIMEMultipart('alternative')
    message['Subject'] = 'Please confirm your email adress!'
    message['From'] = EMAIL_ADRESS
    message['To'] = receiver

    text = """\
        Please click or copy the following link in order to confirm your email adress:
        {}/{}
    """.format(HOST_ADRESS, code)
    html = """\
        <html>
            <body>
                <a href="{}/{}>Confirm your email adress</a>
            </body>
        </html>
    """.format(HOST_ADRESS, code)

    message.attach(MIMEText(text, 'plain'))
    message.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL(SMTP_ADRESS, SSL_PORT, context=context) as server:
        server.login(EMAIL_ADRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADRESS, receiver, message.as_string())