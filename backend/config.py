import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLAlchemy 1.4 no longer supports url strings that start with 'postgres'
    # (only 'postgresql') but heroku's postgres add-on automatically sets the
    # url in the hidden config vars to start with postgres.
    # so the connection uri must be updated here (for production)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL').replace('postgres://', 'postgresql://')
    SQLALCHEMY_ECHO = True



    # Flask-Mail Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None # Use TLS if env var is set (e.g., 'true')
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is None # Use SSL if env var is set (e.g., 'true')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') # Your email address
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # Your email password or app password
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or ('Book Table', os.environ.get('MAIL_USERNAME')) # Tuple (Display Name, email_address) or just email_address