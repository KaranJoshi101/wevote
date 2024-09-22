#otp generating function
def Otp():
    import random
    k=0
    for i in range(6):
        k=k*10+random.randrange(0,9)
    return k

#separates username from email
def Username(e):
    if 'www.' in e:
        e=e[4:]
    newe=''
    for i in e:
        if i=='@':
            break
        newe+=i
    return newe

#delete event using event_id
def deleteEvent(event_id):
    e=Event.query.get(event_id)
    v=e.votes
    db.session.delete(e)
    for i in v:
        db.session.delete(i)
    db.session.commit()



#methods imported from flask module
from flask import Flask,render_template, redirect, request,url_for, flash
from werkzeug.utils import secure_filename
from flask import current_app as app
import uuid as uuid
import os

#models content imported in this file
from .models import *







#home page
@app.route('/')
def homePage():
    return render_template('index.html')



#url for login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        e=request.form.get('email')
        p=request.form.get('pass')
        
        if e=='iamadmin@gmail.com' and p=='123':   #checking admin id credentials
            return redirect('/admin')   #takes to '/admin' page
        rec=User.query.filter_by(email=e).first()
        if rec and rec.registered:
            if rec.pwd==p:
                return redirect(f'/{rec.id}/home') 
            else:
                flash("Wrong Password")
        else:
            return 'email does not exist register->'

           #takes to '/user' page
    
    return render_template('login.html') 


#url for register page
@app.route('/register',methods=['GET','POST'])
def userRegister():
    if request.method=='POST':
        email=request.form.get('email')
        check=User.query.filter_by(email=email,registered=True).first()
        if check:
            return 'email already exists go to login page'
        return redirect('/'+email+'/verification')
    return render_template('register1.html')

#url for verifying email
@app.route('/<email>/verification',methods=['GET','POST'])
def verifyEmail(email):
    if request.method=='POST':
        otp=request.form.get('one')+request.form.get('two')+request.form.get('three')+request.form.get('four')+request.form.get('five')+request.form.get('six')
        set=User.query.filter_by(email=email).first()
        if str(set.otp)==otp:
            return redirect('/'+email+'/setpassword')
        return 'wrong otp entered.Try again'
    o=Otp()
    user_rec=User.query.filter_by(email=email).first()
    if user_rec:
        user_rec.otp=o
    else:
        user_rec=User(email=email,otp=o)
        db.session.add(user_rec)
    db.session.commit()
    #otp sender
    from email.message import EmailMessage
    import ssl,smtplib
    sender='wevoteteam@gmail.com'
    pwd='bdsdenzmphtgrymb'
    rec=email
    sub='OTP for WeVote Application'
    body="""
    Dear """+Username(email)+""",

    Please use the OTP below to sign into the WeVote application.
    
    OTP: """+str(o)+"""
    Do not share the OTP with anyone.
    
    Kind regards,
    WeVote Team
    """
    em=EmailMessage()
    em['From']=sender
    em['To']=rec
    em['Subject']=sub
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(sender,pwd)
        smtp.sendmail(sender,rec,em.as_string())

    
    return render_template('register2.html',email=email)


#url for setting password after verification
@app.route('/<email>/setpassword',methods=['GET','POST'])
def setPassword(email):
    if request.method=='POST':
        p=request.form.get('pass')
        n=request.form.get('name')
        rec=User.query.filter_by(email=email).first()
        rec.pwd=p
        rec.name=n
        rec.registered=True
        db.session.commit()
        return redirect(f'/{rec.id}/home')

    return render_template('register3.html',email=email)

#url for admin dashboard
@app.route('/admin')
def adminDashboard():
    return render_template('admin_dash.html')

#url for admin review
@app.route('/admin/review')
def adminReview():
    events=Event.query.filter_by(isApproved=0).all()
    return render_template('admin_review.html',events=events)

#url for admin approved
@app.route('/admin/<int:event_id>/approve')
def adminApprove(event_id):
    record=Event.query.get(event_id)
    record.isApproved=True
    db.session.commit()
    return redirect('/admin/review')


#url for admin search of user
@app.route('/admin/<int:userId>/watchUser')
def adminWatchUser(userId):
    user=User.query.get(userId)
    return render_template('admin_watch_user.html',user=user)




@app.route('/admin/<event_id>/reject')
def adminRejects(event_id):
    deleteEvent(event_id)
    return redirect('/admin/review')

@app.route('/<userId>/<eventId>/delete')
def userDelete(userId,eventId):
    deleteEvent(eventId)
    return redirect(f'/{userId}/home')


#url for user dashboard
@app.route('/<userId>/home',methods=['GET','POST'])
def userDashboard(userId):
    if request.method=='POST':
        import datetime
        t=request.form.get('title')
        d=request.form.get('desc')
        ti=request.form.get('stime')
        checkNumWinners=request.form.get('checkNumWinners')
        if(checkNumWinners):
            numWinners=int(request.form.get('numWinners'))
        else:
            numWinners=1
        stime=datetime.datetime(int(request.form.get('year')),int(request.form.get('month')),int(request.form.get('date')),int(ti[:2]),int(ti[3:]))
        rec=User.query.get(userId)
        durh=request.form.get('flexRadioDefault')
        if durh=="durh":
            durHour=int(request.form.get("extendhour"))
            durMin=0
            etime=stime+datetime.timedelta(hours=durHour)
        else:
            durMin=int(request.form.get("extendminute"))
            durHour=0
            etime=stime+datetime.timedelta(minutes=durMin)
        
        voters=request.form.get('voters').split(',')
        e=Event(organizerId=userId,title=t,desc=d,endTime=etime,startTime=stime,createTime=datetime.datetime.now(),voterCount=len(voters),durHour=durHour,durMin=durMin,numWinners=numWinners)
        db.session.add(e)
        db.session.commit()

        allow=request.form.get('allowcand')
        organizerEmail=User.query.get(userId).email
        if allow=='on':
            candidates=request.form.get('candidates').split(',')
            for i in candidates:
                if i==organizerEmail:
                    continue
                check=User.query.filter_by(email=i).first()
                if not check:
                    newregistration=User(email=i)
                    db.session.add(newregistration)
                    db.session.commit()
                check=User.query.filter_by(email=i).first()
                r=Vote(eventId=e.id,userId=check.id,role='candidate')
                db.session.add(r)
                db.session.commit()
        
            
            for i in voters:
                if i==organizerEmail:
                    continue
                check=User.query.filter_by(email=i).first()
                if not check:
                    newregistration=User(email=i)
                    db.session.add(newregistration)
                    db.session.commit()
                check=User.query.filter_by(email=i).first()
                r=Vote(eventId=e.id,userId=check.id,role='voter')
                db.session.add(r)
                db.session.commit()
        else:
            
            for i in voters:
                if i==organizerEmail:
                    continue
                check=User.query.filter_by(email=i).first()
                if not check:
                    newregistration=User(email=i)
                    db.session.add(newregistration)
                    db.session.commit()
                check=User.query.filter_by(email=i).first()
                r=Vote(eventId=e.id,userId=check.id,role='candidate')
                db.session.add(r)
                db.session.commit()
        v=Vote(eventId=e.id,userId=userId,role='organizer')
        db.session.add(v)
        db.session.commit()
        return render_template('organize_thank_you.html',userId=userId)
    user=User.query.get(userId)
    events=[]
    for v in user.votes:
        events+=[Event.query.get(v.eventId)]
    return render_template('user_myevents.html',user=user,events=events)


@app.route('/<userId>/<eventId>/explore')
def exploreEvent(userId,eventId):
    event=Event.query.get(eventId)
    cand=[]
    user=User.query.get(userId)
    vote=event.votes
    for v in vote:
        if v.candidature==0:
            cand+=[User.query.get(v.userId)]
    return render_template('explore-events.html',event=event,user=user,vote=vote,cand=cand)

@app.route('/<userId>/<eventId>/register',methods=['GET','POST'])
def registerCandidate(userId,eventId):
    if request.method=='POST':
        v=Vote.query.filter_by(userId=userId,eventId=eventId).first()
        u=User.query.get(userId)
        v.motive=request.form.get("motive")
        v.branch=request.form.get("branch")
        v.gender=request.form.get("gender")
        
        u.candidateProfile=request.files["candidateProfile"]
        
        dp=secure_filename(u.candidateProfile.filename)
        candidateProfile=str(uuid.uuid1())+"_"+dp
        u.candidateProfile.save(os.path.join(app.config['UPLOAD_FOLDER'],candidateProfile))
        u.candidateProfile=candidateProfile
        v.candidature=0
        
        db.session.commit()
        return redirect(f'/{userId}/{eventId}/explore')
    u=User.query.get(userId)
    return render_template('register-candidate.html',user=u)

@app.route('/<userId>/<eventId>/vote',methods=['GET','POST'])
def vote(userId,eventId):
    if request.method=='POST':
        
        return
    v=Vote.query.filter_by(userId=userId,eventId=eventId).first()
    e=Event.query.get(eventId)
    registeredCandidates=[]
    for i in Vote.query.filter_by(eventId=eventId).all():
        if(i.role=='candidate' and i.candidature>=0):
            registeredCandidates+=[User.query.get(i.userId)]

      

    if(v.vote):
        return 'Already voted'
    return render_template('vote-now.html',event=e,registeredCandidates=registeredCandidates)

@app.route('/public')
def public():
    return render_template('public-events.html')
