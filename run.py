from api import api


api.run(server='gunicorn', host='0.0.0.0', port=5000)
