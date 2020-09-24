from datetime import datetime
from flaskr.extensions import db

# 用户
class user(db.Model):
  id       = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, unique=True, nullable=False)
  password = db.Column(db.Text, nullable=False)


# 物料种类表
class materiel(db.Model):
  id            = db.Column(db.Integer, primary_key=True)
  materiel_name = db.Column(db.String(30), nullable=False, comment='物料名称')
  standard      = db.Column(db.String(30), comment='规格')
  unit          = db.Column(db.String(10), comment='单位')
  # 关联 - stock
  stocks        = db.relationship('stock', back_populates='materiel')


# 库存表
class stock(db.Model):
  id          = db.Column(db.Integer, primary_key=True)
  amount      = db.Column(db.Numeric(6,1), nullable=False, comment='总价')
  gross       = db.Column(db.Numeric(6,1), nullable=False, comment='总量')
  comment     = db.Column(db.Text, comment='备注')
  # 关联 - materiel
  materiel_id = db.Column(db.Integer, db.ForeignKey('materiel.id'), nullable=False, comment='关联物料ID')
  materiel    = db.relationship('materiel', back_populates='stocks')
  # 关联 - batch_in
  batch_ins   = db.relationship('batch_in', back_populates='stock')


# 入库批次表
class batch_in(db.Model):
  id         = db.Column(db.Integer, primary_key=True)
  serial     = db.Column(db.Integer, nullable=False, comment='批次序列号')
  in_number  = db.Column(db.Numeric(6,1), nullable=False, comment='入库数量')
  in_time    = db.Column(db.DateTime, default=datetime.utcnow, index=True, comment='入库时间')
  price      = db.Column(db.Numeric(6,1), nullable=False, comment='进货单价')
  comment    = db.Column(db.Text, comment='备注')
  # 关联 - stock
  stock_id   = db.Column(db.Integer, db.ForeignKey('stock.id'), nullable=False, comment='关联库存ID')
  stock      = db.relationship('stock', back_populates='batch_ins')
  # 关联 - batch_out
  batch_outs = db.relationship('batch_out', back_populates='batch_in')


# 出库批次表
class batch_out(db.Model):
  id          = db.Column(db.Integer, primary_key=True)
  out_number  = db.Column(db.Numeric(6,1), nullable=False, comment='出库数量')
  out_time    = db.Column(db.DateTime, default=datetime.utcnow, index=True, comment='出库时间')
  price       = db.Column(db.Numeric(6,1), nullable=False, comment='出售单价')
  loss        = db.Column(db.Numeric(6,1), default=0, comment='损耗')
  document    = db.Column(db.String(20), comment='单据编号')
  code        = db.Column(db.String(20), comment='物料长代码')
  comment     = db.Column(db.Text, comment='备注')
  # 关联 - batch_in
  batch_in_id = db.Column(db.Integer, db.ForeignKey('batch_in.id'), nullable=False, comment='关联入库批次ID')
  batch_in    = db.relationship('batch_in', back_populates='batch_outs')
