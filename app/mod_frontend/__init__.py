from flask import Blueprint


mod_frontend = Blueprint('mod_frontend', __name__,
                         template_folder='templates')


from app.mod_frontend import errors, views
