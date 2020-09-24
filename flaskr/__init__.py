import os
from flask import Flask
import click
# 配置
from flaskr.settings import config
# 扩展
from flaskr.extensions import db, migrate
# 蓝图
from flaskr.blueprints.admin import admin_bp
# 数据库模型
from flaskr.models import User, Materiel, Stock, Batch_in, Batch_out

def create_app(config_name = None):
  if config_name is None:
    config_name = os.getenv('FLASK_CONFIG', 'development')
  app = Flask(__name__)
  app.config.from_object(config[config_name])

  # 注册
  register_extensions(app)
  register_shell_context(app)
  register_blueprints(app)
  register_commands(app)

  return app


# 初始化扩展
def register_extensions(app):
  db.init_app(app)
  migrate.init_app(app, db)


# 蓝图
def register_blueprints(app):
  app.register_blueprint(admin_bp)


def register_shell_context(app):
  @app.shell_context_processor
  def make_shell_context():
    # 数据库模型
    return dict(db=db, User=User, Materiel=Materiel, Stock=Stock, Batch_in=Batch_in, Batch_out=Batch_out)


# 指令
def register_commands(app):
  @app.cli.command()
  @click.option('--drop', is_flag=True, help='Create after drop.')
  # 初始化数据库
  def initdb(drop):
    """Initialize the database."""
    if drop:
      click.confirm('This operation will delete the database, do you want to continue?', abort=True)
      db.drop_all()
      click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')
