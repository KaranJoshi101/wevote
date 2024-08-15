from .database import db
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    registered=db.Column(db.Boolean,default=False)
    otp=db.Column(db.Integer)
    email=db.Column(db.String(),nullable=False,unique=True)
    pwd=db.Column(db.String())
    name=db.Column(db.String(),default='xyz')
    gender=db.Column(db.String(),default='x')
    school=db.Column(db.String(),default='x')
    batch=db.Column(db.String(),default='x')
    branch=db.Column(db.String(),default='x')
    events=db.relationship('Event',backref='user')
    votes=db.relationship('Vote',backref='user')    

class Vote(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    event_id=db.Column(db.Integer,db.ForeignKey('event.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    role=db.Column(db.String())
    vote=db.Column(db.Boolean,default=False)


class Event(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    user_id=db.Column(db.Integer(),db.ForeignKey('user.id'))
    time=db.Column(db.String(),default='x')
    date=db.Column(db.String(),default='x')
    votes=db.relationship('Vote',backref='event')