"""Simple example"""
from __future__ import absolute_import

from datetime import datetime
import os
from threading import Thread

from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, session, redirect, url_for, flash

import nocommit


# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialisation of the app and the flask extension
app = Flask(__name__)

app.config['SECRET_KEY'] = nocommit.SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[FLASKY] '
app.config['FLASKY_MAIL_SENDER'] = 'FLASKY MASTER <g.cherchye@gmail.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# ORM
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self) -> str:
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self) -> str:
        return f'<User {self.username}>'

# Route definition
@app.route('/', methods=['GET', 'POST'])
def index():
    """Root page"""
    form = NameForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            
            session['known'] = False

            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        
        session['name'] = form.name.data
        form.name.data = ''

        return redirect(url_for('index'))

    return render_template(
                'index.html',
                form=form,
                name=session.get('name'),
                current_time=datetime.utcnow(),
                known=session.get('known', False)
            )

@app.route('/user/<name>')
def user(name):
    """Named user page"""
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    """Error 404 page"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Error 500 page"""
    return render_template('500.html'), 500


# Name Form
class NameForm(FlaskForm):
    """Class to ask name of the user"""
    name = StringField('What is your name ?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Shell context
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

# Send Mail
def send_mail(to, subject, template, **kwargs):
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

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)
