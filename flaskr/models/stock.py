from flaskr.extensions import db
from marshmallow import Schema, fields


# 库存表
class Stock(db.Model):
  id          = db.Column(db.Integer, primary_key=True, mssql_identity_start=1, mssql_identity_increment=2)
  price       = db.Column(db.DECIMAL(6,1), nullable=False, comment='总价')
  in_number   = db.Column(db.DECIMAL(6,1), nullable=False, comment='总量')
  # 关联 - materiel
  materiel_id = db.Column(db.Integer, db.ForeignKey('materiel.id'), nullable=False, comment='关联物料ID')
  materiel    = db.relationship('Materiel', back_populates='stocks')
  # 关联 - batch_in
  batch_ins   = db.relationship('Batch_in', back_populates='stock')


class Stock_schema(Schema):
  id          = fields.Integer(dump_only=True)
  price       = fields.Decimal()
  in_number   = fields.Decimal()
  materiel_id = fields.Integer()
  # 如果存在相互调用,必须使用exclude或only参数避免无限递归
  materiel    = fields.Nested('flaskr.models.materiel.Materiel_schema', only=('materiel_name','standard','unit',))
  batch_ins   = fields.Nested('flaskr.models.batch_in.Batch_in_schema', many=True, only=('serial','in_number','price','comment','created_at','id','stock',))
