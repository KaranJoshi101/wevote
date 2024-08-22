from .database import db
class User(db.Model):
    #entered during registration
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String())
    registered=db.Column(db.Boolean,default=False)
    otp=db.Column(db.Integer)
    email=db.Column(db.String(),nullable=False,unique=True)
    pwd=db.Column(db.String())
    login=db.Column(db.Boolean,default=False)
   #entered during promotion as candidate
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
    title=db.Column(db.String(),default='x')
    desc=db.Column(db.String(),default='x')
    etime=db.Column(db.DateTime,nullable=False)
    stime=db.Column(db.DateTime,nullable=False)
    isapproved=db.Column(db.Boolean,default=False)
    votes=db.relationship('Vote',backref='event')
    