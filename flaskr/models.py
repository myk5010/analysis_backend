from datetime import datetime
from flaskr.extensions import db
from marshmallow import Schema, fields, validate


# 用户
class User(db.Model):
  id       = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, unique=True, nullable=False)
  password = db.Column(db.Text, nullable=False)

class User_schema(Schema):
  id       = fields.Integer(dump_only=True)
  username = fields.String()


# 库存表
class Stock(db.Model):
  id          = db.Column(db.Integer, primary_key=True)
  amount      = db.Column(db.Float(6,1), nullable=False, comment='总价')
  gross       = db.Column(db.Float(6,1), nullable=False, comment='总量')
  comment     = db.Column(db.Text, comment='备注')
  # 关联 - materiel
  materiel_id = db.Column(db.Integer, db.ForeignKey('materiel.id'), nullable=False, comment='关联物料ID')
  materiel    = db.relationship('Materiel', back_populates='stocks')
  # 关联 - batch_in
  batch_ins   = db.relationship('Batch_in', back_populates='stock')


class Stock_schema(Schema):
  id     = fields.Integer(dump_only=True)
  amount = fields.Float()
  gross  = fields.Float()


# 入库批次表
class Batch_in(db.Model):
  id         = db.Column(db.Integer, primary_key=True)
  serial     = db.Column(db.Integer, nullable=False, comment='批次序列号')
  in_number  = db.Column(db.Float(6,1), nullable=False, comment='入库数量')
  in_time    = db.Column(db.DateTime, default=datetime.utcnow, index=True, comment='入库时间')
  price      = db.Column(db.Float(6,1), nullable=False, comment='进货单价')
  comment    = db.Column(db.Text, comment='备注')
  # 关联 - stock
  stock_id   = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False, comment='关联库存ID')
  stock      = db.relationship('Stock', back_populates='batch_ins')
  # 关联 - batch_out
  batch_outs = db.relationship('Batch_out', back_populates='batch_in')

class Batch_in_schema(Schema):
  id         = fields.Integer(dump_only=True)
  serial     = fields.Integer()
  in_number  = fields.Float()
  in_time    = fields.DateTime()
  price      = fields.Float()
  comment    = fields.String()


# 出库批次表
class Batch_out(db.Model):
  id          = db.Column(db.Integer, primary_key=True)
  out_number  = db.Column(db.Float(6,1), nullable=False, comment='出库数量')
  out_time    = db.Column(db.DateTime, default=datetime.utcnow, index=True, comment='出库时间')
  price       = db.Column(db.Float(6,1), nullable=False, comment='出售单价')
  loss        = db.Column(db.Float(6,1), default=0, comment='损耗')
  document    = db.Column(db.String(20), comment='单据编号')
  code        = db.Column(db.String(20), comment='物料长代码')
  comment     = db.Column(db.Text, comment='备注')
  # 关联 - batch_in
  batch_in_id = db.Column(db.Integer, db.ForeignKey('batch_in.id'), nullable=False, comment='关联入库批次ID')
  batch_in    = db.relationship('Batch_in', back_populates='batch_outs')

class Batch_out_schema(Schema):
  id          = fields.Integer(dump_only=True)
  out_number  = fields.Float()
  out_time    = fields.DateTime()
  price       = fields.Float()
  loss        = fields.Float()
  document    = fields.String()
  code        = fields.String()
  comment     = fields.String()


# 物料种类表
class Materiel(db.Model):
  id            = db.Column(db.Integer, primary_key=True)
  materiel_name = db.Column(db.String(30), nullable=False, comment='物料名称')
  standard      = db.Column(db.String(30), comment='规格')
  unit          = db.Column(db.String(10), comment='单位')
  # 关联 - stock
  stocks        = db.relationship('Stock', back_populates='materiel')

class Materiel_schema(Schema):
  id            = fields.Integer(dump_only=True)
  materiel_name = fields.String(required=True, validate=validate.Length(min=1), error_messages={'required': '物料名称不能为空'})
  standard      = fields.String()
  unit          = fields.String()
  stocks        = fields.Nested(Stock_schema, many=True)