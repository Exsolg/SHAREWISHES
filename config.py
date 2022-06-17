class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///../db/wish.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "my_secret_key"
    MAX_CONTENT_LENGTH = 10240 * 10240