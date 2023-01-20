import os

class Config:
    DEBUG = True
    SECRET_KEY = "Some text which is a password"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAIL_SERVER = 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USE_TLS = True 
    # MAIL_USERNAME = os.environ.get('mail_username')
    # MAIL_PASSWORD = os.environ.get('mail_password')