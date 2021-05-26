"""Application routes in the main blueprint"""
from __future__ import absolute_import

from datetime import datetime

from flask import current_app, redirect, render_template, session, url_for

from .. import db
from ..email import send_mail
from ..models import User
from . import main
from .forms import NameForm


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            
            session['known'] = False

            if current_app.config['FLASKY_ADMIN']:
                send_mail(
                    current_app.config['FLASKY_ADMIN'],
                    'New User',
                    'mail/new_user',
                    user=user
                )
        else:
            session['known'] = True
        
        session['name'] = form.name.data
        form.name.data = ''

        return redirect(url_for('.index'))

    return render_template(
                'index.html',
                form=form,
                name=session.get('name'),
                current_time=datetime.utcnow(),
                known=session.get('known', False)
            )