#!~/.local/share/virtualenvs/bmapp-uY0xXsS3/bin/python
from api import create_app

# for gunicorn, by default it searches for "application"
application = create_app()

if __name__ == '__main__':
    application.run()
