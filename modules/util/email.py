from datetime import datetime
import secrets
import smtplib
from email.message import EmailMessage
import threading
import time


def email(subject: str, body: str, to: str = secrets.TO_EMAIL_ADDRESS):
    user = secrets.EMAIL_ADDRESS
    password = secrets.EMAIL_PASSWORD

    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = user

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()


def start_alerter(subject: str, body: str, boolfunc, check_interval_minutes: int = 10, name: str = '') -> threading.Thread:
    def waiter():
        while True:
            print(f'\nRunning alert check: [{name}]')
            if boolfunc():
                print(f'Conditions met! Cancelling alert: {name}')
                email(subject, body + f'\n\n Sent {datetime.now()}')
                break
            print(f'Condition not met. Continuing alert: [{name}]')
            time.sleep(60*check_interval_minutes)

    return threading.Thread(target=waiter, name=name)
