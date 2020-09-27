import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
  prefix = "sqlite:///"
else:
  prefix = "sqlite:////"


class BaseConfig(object):
  SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

  DEBUG_TB_INTERCEPT_REDIRECTS = False
  
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_RECORD_QUERIES = True


class DevelopmentConfig(BaseConfig):
  # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, "data-dev.db")
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123123@127.0.0.1:3306/analysis"


class TestingConfig(BaseConfig):
  TESTING = True
  WTF_CSRF_ENABLED = False
  # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, "data-test.db")
  SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123123@127.0.0.1:3306/analysis"


class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, "data.db"))

config = {
  'development': DevelopmentConfig,
  'testing': TestingConfig,
  'production': ProductionConfig
}