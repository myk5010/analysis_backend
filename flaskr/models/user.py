from flaskr.extensions import db
from marshmallow import Schema, fields

# 用户
class User(db.Model):
  id       = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(30), unique=True, nullable=False)
  password = db.Column(db.Text, nullable=False)

class User_schema(Schema):
  id       = fields.Integer(dump_only=True)
  username = fields.String()