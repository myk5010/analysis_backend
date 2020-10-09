from flaskr.extensions import db
from marshmallow import Schema, fields, validate

# 物料种类表
class Materiel(db.Model):
  id            = db.Column(db.Integer, primary_key=True)
  materiel_name = db.Column(db.String(30), unique=True, nullable=False, comment='物料名称')
  standard      = db.Column(db.String(30), comment='规格')
  unit          = db.Column(db.String(10), comment='单位')
  # 关联 - stock
  stocks        = db.relationship('Stock', back_populates='materiel')


class Materiel_schema(Schema):
  id            = fields.Integer(dump_only=True)
  materiel_name = fields.String(required=True, validate=validate.Length(min=1), error_messages={'required': '物料名称不能为空'})
  standard      = fields.String()
  unit          = fields.String()
  # 如果存在相互调用,必须使用exclude或only参数避免无限递归
  stocks        = fields.Nested('flaskr.models.materiel.Stock_schema', many=True, exclude=('materiel',))
