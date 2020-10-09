from datetime import datetime
from flaskr.extensions import db
from marshmallow import Schema, fields, validate


# 入库批次表
class Batch_in(db.Model):
  id         = db.Column(db.Integer, primary_key=True, mssql_identity_start=2, mssql_identity_increment=2)
  serial     = db.Column(db.Integer, nullable=False, comment='批次序列号')
  in_number  = db.Column(db.DECIMAL(6,1), nullable=False, comment='入库数量')
  remainder  = db.Column(db.DECIMAL(6,1), nullable=False, comment='剩余库存')
  price      = db.Column(db.DECIMAL(6,1), nullable=False, comment='进货单价')
  commission = db.Column(db.DECIMAL(6,1), default=0, comment='佣金')
  comment    = db.Column(db.Text, comment='备注')
  created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='入库时间')
  updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  delete_at  = db.Column(db.DateTime)
  # 关联 - stock
  stock_id   = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False, comment='关联库存ID')
  stock      = db.relationship('Stock', back_populates='batch_ins')
  # 关联 - batch_out
  batch_outs = db.relationship('Batch_out', back_populates='batch_in')


class Batch_in_schema(Schema):
  id         = fields.Integer(dump_only=True)
  serial     = fields.Integer()
  in_number  = fields.Decimal()
  remainder  = fields.Decimal()
  commission = fields.Decimal()
  price      = fields.Decimal()
  comment    = fields.String()
  created_at = fields.Date()
  stock_id   = fields.Integer(load_only=True)
  # 如果存在相互调用,必须使用exclude或only参数避免无限递归
  stock      = fields.Nested('flaskr.models.stock.Stock_schema', only=('materiel',))






