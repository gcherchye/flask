"""Blueprints creation"""
from __future__ import absolute_import

from flask import Blueprint

# Instanciate the Blueprint here to avoid circular references
main = Blueprint('main', __name__)

from . import errors, forms
