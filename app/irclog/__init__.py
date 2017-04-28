from flask import Blueprint

irclog = Blueprint('irclog', __name__)

from . import views
