from .database import db
class User(db.Model):
    #entered during registration
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String())
    registered=db.Column(db.Boolean,default=False)
    otp=db.Column(db.Integer)
    email=db.Column(db.String(),nullable=False,unique=True)
    pwd=db.Column(db.String())
   #entered during promotion as candidate
    candidateProfile=db.Column(db.String(120),nullable=True)
    votes=db.relationship('Vote',backref='user')    

class Organizer(db.Model):
    id=db.Column(db.String(),primary_key=True)
    name=db.Column(db.String())
    email=db.Column(db.String(),nullable=False,unique=True)
    status=db.Column(db.Integer,default=0)
    pwd=db.Column(db.String())
    phone=db.Column(db.Integer)
    org_name=db.Column(db.String())
    org_type=db.Column(db.String())
    file=db.Column(db.String())
    events=db.relationship('Event',backref='organizer')  

class Vote(db.Model):
    id=db.Column(db.String(),primary_key=True)
    eventId=db.Column(db.Integer,db.ForeignKey('event.id'))
    userId=db.Column(db.Integer,db.ForeignKey('user.id'))
    role=db.Column(db.String())
    candidature=db.Column(db.Integer,default=-1)
    motive=db.Column(db.String())
    branch=db.Column(db.String())
    gender=db.Column(db.String())
    vCount=db.Column(db.Integer,default=0)
    vote=db.Column(db.Boolean,default=False)

class Event(db.Model):
    id=db.Column(db.String(),primary_key=True)
    createTime=db.Column(db.DateTime)
    organizerId=db.Column(db.Integer(),db.ForeignKey('organizer.id'))
    title=db.Column(db.String(),default='x')
    desc=db.Column(db.String(),default='x')
    endTime=db.Column(db.DateTime,nullable=False)
    startTime=db.Column(db.DateTime,nullable=False)
    isApproved=db.Column(db.Boolean,default=False)
    voterCount=db.Column(db.Integer(),default=0)
    durHour=db.Column(db.Integer())
    durMin=db.Column(db.Integer())
    numWinners=db.Column(db.Integer(),default=1)
    votes=db.relationship('Vote',backref='event')
