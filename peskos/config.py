import os


class Config:
    DEBUG = True
    SECRET_KEY = "Some key here, not a password"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'db.sqlite')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    TESTING = False
    MAIL_USERNAME = "hanslettj@gmail.com"
    MAIL_DEFAULT_SENDER = "peskosgroup@peskos.com"
    MAIL_PASSWORD = "rudphandxyvrimtl"
