''' Routes '''
import logging
from flask import render_template
from . import main
from flask_jwt import jwt_required


LOGGER = logging.getLogger(__name__)


@main.route('/')
def index():
    """
    Index page
    """
    return render_template('index.html')


@main.route('/contacts')
def contacts():
    """
    Contacts page
    """
    return render_template('contacts.html')
