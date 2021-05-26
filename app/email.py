"""Mailing module"""
from __future__ import absolute_import

from threading import Thread

from flask import current_app, render_template
from flask.app import Flask
from flask_mail import Message

from . import mail


def send_mail(to: str, subject: str, template: str, **kwargs) -> Thread:
    """Send a mail to someone using a template

    Args:
        to (str): The mail address of the recipient
        subject (str): The subject oof the mail
        template (str): The name of the template to use

    Returns:
        threading.Thread: The thread that will execute the sending
    """
    app = current_app._get_current_object()

    msg = Message(
        app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
        sender=app.config['FLASKY_MAIL_SENDER'],
        recipients=[to]
    )

    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()

    return thr


def send_async_mail(app: Flask, msg: Message):
    with app.app_context():
        mail.send(msg)
