from .database import db
class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    email=db.Column(db.String(),nullable=False,unique=True)
    pwd=db.Column(db.String(),nullable=False)