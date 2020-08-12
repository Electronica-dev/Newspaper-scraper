""" Script to send attachment(s) to an email """

from os import environ
from os import path
from smtplib import SMTP
from email.message import EmailMessage
from sys import exit

# Email and application password are stored as environment variables.
email = environ.get('EMAIL_ADDRESS')
pwd = environ.get('EMAIL_PASSWORD')


def send_email_pdf(recipient_list, pdf_file_path_list, subject='(no subject)', body='(no body)'):

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email
    msg['To'] = ', '.join(recipient_list)
    msg.set_content(body)

    for file in pdf_file_path_list:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = path.basename(f.name)
            if not file_name.endswith('pdf'):
                print(f'{file_name} is not a pdf file.')
                exit()
        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(email, pwd)
        smtp.send_message(msg)
