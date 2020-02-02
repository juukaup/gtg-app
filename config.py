import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'secret key'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    ENV = 'development'
    DEBUG = True


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    TESTING = True