from app.app import create_app


app = create_app('dev.cfg')
app.run(host='0.0.0.0')
