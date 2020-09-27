from datetime import datetime
from flaskr.extensions import db
from marshmallow import Schema, fields, validate


# 入库批次表
class Batch_in(db.Model):
  id         = db.Column(db.Integer, primary_key=True)
  serial     = db.Column(db.Integer, nullable=False, comment='批次序列号')
  in_number  = db.Column(db.Float(6,1), nullable=False, comment='入库数量')
  price      = db.Column(db.Float(6,1), nullable=False, comment='进货单价')
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
  in_number  = fields.Float()
  in_time    = fields.DateTime()
  price      = fields.Float()
  comment    = fields.String()





