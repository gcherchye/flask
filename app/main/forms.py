"""Web Forms"""
from __future__ import absolute_import

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(FlaskForm):
    """Class to ask name of the user"""
    name = StringField('What is your name ?', validators=[DataRequired()])
    submit = SubmitField('Submit')
