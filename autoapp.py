import os

from app.app import create_app


app = create_app(os.environ['APP_CONFIG'])
