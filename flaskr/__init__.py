import os
from flask import Flask
from flaskr.extensions import db
# 蓝图
from flaskr.blueprints.admin import admin_bp

def create_app(test_config = None):
  # create and configure the app
  app = Flask(__name__, instance_relative_config = True)
  app.config.from_mapping(
    SECRET_KEY = 'dev',
    # DATABASE = os.path.join(app.instance_path, 'flask.sqlite'),
    SQLALCHEMY_DATABASE_URI = os.path.join(app.instance_path, 'flask.sqlite'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
  )

  if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent = True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  # a simple page that says hello
  @app.route('/hello')
  def hello():
    return 'Hello, World!'

  register_extensions(app)
  register_blueprints(app)

  return app

def register_extensions(app):
  # 初始化扩展
  db.init_app(app)


def register_blueprints(app):
  # 注册蓝图
  app.register_blueprint(admin_bp)
