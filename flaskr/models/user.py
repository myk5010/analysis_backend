from app import db

class user(db.Model):
  id = db.Column(db.integer, primary_key=True)
  username = db.Column(db.Text, unique=True, nullable=False)
  password = db.Column(db.Text, nullable=False)