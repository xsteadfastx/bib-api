from flask import Blueprint


mod_api = Blueprint('mod_api', __name__)


from app.mod_api import errors, views
