from flaskr.extensions import db

# 用户
class user(db.Model):
  id = db.Column(db.integer, primary_key=True)
  username = db.Column(db.Text, unique=True, nullable=False)
  password = db.Column(db.Text, nullable=False)


# 物料种类表
class materiel(db.Model):
  id = db.Column(db.integer, primary_key=True)
  materiel_name = db.Column(db.String(30), nullable=False)
  standard = db.Column(db.String(30))
  unit = db.Column(db.String(10))
  stocks = db.relationship('stock', back_populates='materiel')


# 库存表
class stock(db.Model):
  id = db.Column(db.integer, primary_key=True)
  amount = db.Column(db.Numeric(6,1), nullable=False)
  gross = db.Column(db.Numeric(6,1), nullable=False)
  comment = db.Column(db.Text)
  materiel_id = db.Column(db.integer, db.ForeignKey('materiel.id'), nullable=False)
  materiel = db.relationship('materiel', back_populates='stocks')
