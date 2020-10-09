from datetime import datetime
from flaskr.extensions import db
from marshmallow import Schema, fields, validate

# 出库批次表
class Batch_out(db.Model):
  id          = db.Column(db.Integer, primary_key=True)
  out_number  = db.Column(db.DECIMAL(6,1), nullable=False, comment='出库数量')
  price       = db.Column(db.DECIMAL(6,1), nullable=False, comment='出售单价')
  loss        = db.Column(db.DECIMAL(6,1), default=0, comment='损耗')
  document    = db.Column(db.String(20), comment='单据编号')
  code        = db.Column(db.String(20), comment='物料长代码')
  comment     = db.Column(db.Text, comment='备注')
  created_at  = db.Column(db.DateTime, default=datetime.utcnow, comment='出库时间')
  updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  delete_at   = db.Column(db.DateTime)
  # 关联 - batch_in
  batch_in_id = db.Column(db.Integer, db.ForeignKey('batch_in.id'), nullable=False, comment='关联入库批次ID')
  batch_in    = db.relationship('Batch_in', back_populates='batch_outs')

class Batch_out_schema(Schema):
  id          = fields.Integer(dump_only=True)
  out_number  = fields.Decimal()
  out_time    = fields.DateTime()
  price       = fields.Decimal()
  loss        = fields.Decimal()
  document    = fields.String()
  code        = fields.String()
  comment     = fields.String()