"""Simple example"""
from __future__ import absolute_import

from datetime import datetime

from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, session, redirect, url_for, flash

import nocommit


# Initialisation of the app and the flask extension
app = Flask(__name__)
app.config['SECRET_KEY'] = nocommit.SECRET_KEY

bootstrap = Bootstrap(app)
moment = Moment(app)

# Route definition
@app.route('/', methods=['GET', 'POST'])
def index():
    """Root page"""
    form = NameForm()

    if form.validate_on_submit():
        old_name = session.get('name')

        if old_name is not None and old_name != form.name.data:
            flash('Looks like you changed your name!')

        session['name'] = form.name.data

        return redirect(url_for('index'))

    return render_template(
                'index.html',
                form=form,
                name=session.get('name'),
                current_time=datetime.utcnow()
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


class NameForm(FlaskForm):
    """Class to ask name of the user"""
    name = StringField('What is your name ?', validators=[DataRequired()])
    submit = SubmitField('Submit')
