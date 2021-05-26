"""Flasky application"""
from __future__ import absolute_import

from datetime import datetime
import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import Role, User


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

# Shell context
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

# Send Mail
