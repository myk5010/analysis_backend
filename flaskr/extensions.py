from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# 数据库管理扩展
db = SQLAlchemy()
# 数据迁移
migrate = Migrate()
