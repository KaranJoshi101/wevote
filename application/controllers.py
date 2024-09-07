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


#methods imported from flask module
from flask import Flask,render_template, redirect, request,url_for
from flask import current_app as app

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
                return redirect('/'+e+'/home') 
            else:
                return render_template('login-wrong-pass.html')
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
    sender='www.joshikaran3424@gmail.com'
    pwd='fmoevzvxexghzjli'
    rec=email
    sub='OTP for WeVote Application'
    body="""
    Dear """+Username(email)+""",
    Please use the OTP below to sign into the WeVote application.


    OTP: """+str(o)+"""


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
        return redirect('/'+email+'/home')

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


@app.route('/event_id/delete')
def deleteEvent(event_id):
    db.session.delete(Event.query.get(event_id))
    db.session.commit()
@app.route('/<event_id>/reject')
def adminRejects(event_id):
    deleteEvent(event_id)
    return redirect('/admin/review')


#url for user dashboard
@app.route('/<email>/home')
def userDashboard(email):
    rec=User.query.filter_by(email=email).first()
    return render_template('user_dash.html',email=email,name=rec.name)


#url for organize
@app.route('/<email>/organize',methods=['GET','POST'])
def organizeEvents(email):
    if request.method=='POST':
        import datetime
        t=request.form.get('title')
        d=request.form.get('desc')
        ti=request.form.get('stime')
        stime=datetime.datetime(int(request.form.get('year')),int(request.form.get('month')),int(request.form.get('date')),int(ti[:2]),int(ti[3:]))
        rec=User.query.filter_by(email=email).first()
        durh=request.form.get("checkextendhour")
        durm=request.form.get("checkextendminute")
        if durh:
            durHour=int(request.form.get("extendhour"))
            durMin=0
            etime=stime+datetime.timedelta(hours=durHour)
        else:
            durMin=int(request.form.get("extendminute"))
            durHour=0
            etime=stime+datetime.timedelta(minutes=durMin)
        
        voters=request.form.get('voters').split(',')
        e=Event(organizerId=rec.id,title=t,desc=d,endTime=etime,startTime=stime,createTime=datetime.datetime.now(),voterCount=len(voters),durHour=durHour,durMin=durMin)
        db.session.add(e)
        db.session.commit()

        allow=request.form.get('allowcand')
        if allow=='on':
            candidates=request.form.get('candidates').split(',')
            for i in candidates:
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
                check=User.query.filter_by(email=i).first()
                if not check:
                    newregistration=User(email=i)
                    db.session.add(newregistration)
                    db.session.commit()
                check=User.query.filter_by(email=i).first()
                r=Vote(eventId=e.id,userId=check.id,role='candidate')
                db.session.add(r)
                db.session.commit()
        return render_template('organize_thank_you.html',email=email)
    return render_template('organize.html',email=email)

@app.route('/<email>/myevents')
def userEvents(email):
    user=User.query.filter_by(email=email).first()
    events=Event.query.filter_by(organizerId=user.id).all()
    return render_template('user_myevents.html',events=events,name=user.name,email=email)

