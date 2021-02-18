import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template
from datetime import datetime


def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
        return names, emails

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def send_email():
    try:
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login('stockdatapython@gmail.com', 'ojk76131')

        names, emails = get_contacts('email.txt')
        message_template = read_template('message.txt')

        for name, email in zip(names, emails):
            msg = MIMEMultipart()
            message = message_template.substitute(PERSON_NAME=name.title())
            msg['From']='stockdatapython@gmail.com'
            msg['To']=email
            msg['Subject']='This is the alert from Stock Data'

            msg.attach(MIMEText(message, 'plain'))

            print('Sending E-Mail!')
            s.send_message(msg)
            del msg
    except:
        print("ERROR: In function send_email")
