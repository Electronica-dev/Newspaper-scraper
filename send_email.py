# Script to send an attachment(s) to an email

from os import environ
from os import path
from smtplib import SMTP_SSL
from email.message import EmailMessage
from sys import exit

# Email and application password are stored as environment variables.
email = environ.get('EMAIL_ADDRESS')
pwd = environ.get('EMAIL_PASSWORD')


def send_email_pdf(recipient_list, pdf_file_path_list, subject='(no subject)', body='(no body)'):
    if type(pdf_file_path_list) is not list:
        print('Path should be in a list.')
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

    recipient_string = ', '.join([mail for mail in recipient_list])
    pdf_string = ', '.join(map(str, ([path.basename(pdf) for pdf in pdf_file_path_list])))

    print(f'Sending email to: {recipient_string} with\nSubject: {subject}\nBody: {body}\nAttached PDFs: {pdf_string}')

    with SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, pwd)
        smtp.send_message(msg)
        print('Email sent successfully.')
