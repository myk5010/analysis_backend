from flaskr.extensions import db
from marshmallow import Schema, fields


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
  id       = fields.Integer(dump_only=True)
  amount   = fields.Float()
  gross    = fields.Float()
  # 必须使用exclude或only参数避免无限递归
  materiel = fields.Nested('flaskr.models.materiel.Materiel_schema', exclude=('stocks',))