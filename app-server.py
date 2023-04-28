from api import create_app
from waitress import serve

# for gunicorn, by default it searches for "application"
application = app = create_app()


if __name__ == '__main__':
    #application.run()
    serve(application, host='127.0.0.1', port=5055)
