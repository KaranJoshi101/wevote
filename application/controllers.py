def idGen(name=None):
    import uuid
    if(name):
        return name[:2].upper()+str(uuid.uuid4())[:4]
    else:
        return str(uuid.uuid4())[:6]
def allowed_orgfile(filename):
    ALLOWED_EXTENSIONS = {'pdf','doc'}
    name=''
    for i in filename:
        if i!=' ':
            name+=i
    print(name,'.' in name and name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    return '.' in name and name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#otp generating function
def Otp():
    import random
    k=0
    for i in range(6):
        k=k*10+random.randrange(1,9)
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

#check allowed image extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#methods imported from flask module
from flask import Flask,render_template, redirect, request,url_for, flash,send_file
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


#about us
@app.route('/about')
def aboutUs():
    return render_template('about-us.html')

#contributors page
@app.route('/contributor')
def countributorsPage():
    return render_template('contributor.html')
#url for login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        e=request.form.get('email')
        p=request.form.get('pass')
        
        if e=='iamadmin@gmail.com' and p=='123':   #checking admin id credentials
            return redirect('/admin')   #takes to '/admin' page
        rec=Organizer.query.filter_by(email=e).first()
        if rec:
            if rec.pwd==p:
                return redirect(f'/{rec.id}/organizer/dashboard')
            else:
                flash('incorrect password')
        else:
            rec=User.query.filter_by(email=e).first()
            if rec and rec.registered:
                if rec.pwd==p:
                    return redirect(f'/{rec.id}/home') 
                else:
                    flash("incorrect password")
            else:
                flash('invalid email. Register Now')

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
        user_rec=User(id=idGen('US'),email=email,otp=o)
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

#forgot password
# @app.route('/forgot')
# def forgot()

#url for admin dashboard
@app.route('/admin')
def adminDashboard():
    organizers=Organizer.query.all()
    return render_template('admin_dash.html',organizers=organizers)

#url for admin review
@app.route('/admin/review')
def adminReview():
    events=Event.query.filter_by(isApproved=0).all()
    return render_template('admin_review.html',events=events)

#url for admin approved
@app.route('/admin/<orgId>/approve')
def adminApprove(orgId):
    record=Organizer.query.get(orgId)
    record.status=1
    db.session.commit()
    return redirect('/admin')

@app.route('/admin/<orgId>/reject')
def adminReject(orgId):
    record=Organizer.query.get(orgId)
    record.status=-1
    db.session.commit()
    return redirect('/admin')


#url for admin search of user
@app.route('/admin/<int:userId>/watchUser')
def adminWatchUser(userId):
    user=User.query.get(userId)
    return render_template('admin_watch_user.html',user=user)




@app.route('/admin/<event_id>/event/reject')
def adminRejects(event_id):
    deleteEvent(event_id)
    return redirect('/admin/review')

@app.route('/<userId>/<eventId>/event/delete')
def userDelete(userId,eventId):
    deleteEvent(eventId)
    return redirect(f'/{userId}/home')


#url for user dashboard
@app.route('/<userId>/home',methods=['GET','POST'])
def userDashboard(userId):
    
    user=User.query.get(userId)
    events=[]
    for v in user.votes:
        events+=[Event.query.get(v.eventId)]
    return render_template('user_myevents.html',user=user,events=events)


@app.route('/<userId>/<eventId>/explore')
def exploreEvent(userId,eventId,org=None):
    event=Event.query.get(eventId)
    cand=[]
    user=User.query.get(userId)
    vote=event.votes
    
    for v in vote:
        if v.candidature==0:
            cand+=[User.query.get(v.userId)]
    vuser=Vote.query.filter_by(userId=userId,eventId=eventId).first()
    return render_template('explore-events.html',event=event,user=user,vote=vote,cand=cand,vuser=vuser)

@app.route('/<userId>/<eventId>/candidate/register',methods=['GET','POST'])
def registerCandidate(userId,eventId):
    if request.method=='POST':
        v=Vote.query.filter_by(userId=userId,eventId=eventId).first()
        u=User.query.get(userId)
        v.motive=request.form.get("motive")
        v.branch=request.form.get("branch")
        v.gender=request.form.get("gender")
        

        #check
        
        file=request.files["candidateProfile"]
        max_size = 1024 * 1024
   


        if file and allowed_file(file.filename):
            print(file)
            print(file.filename)
            # Process the file (e.g., save it)
            if len(file.read()) > max_size:
                flash('Image size too large!')
            else:
                file.seek(0)
                u.candidateProfile=file
                dp=secure_filename(u.candidateProfile.filename)
                candidateProfile=str(uuid.uuid1())+"_"+dp
                u.candidateProfile.save(os.path.join(app.config['UPLOAD_FOLDER'],candidateProfile))
                u.candidateProfile=candidateProfile
                v.candidature=0
                db.session.commit()
                return redirect(f'/{userId}/{eventId}/explore')
        else:
            flash('Invalid image type')
        
        
        
        
    u=User.query.get(userId)
    return render_template('register-candidate.html',user=u)

@app.route('/<userId>/<eventId>/vote',methods=['GET','POST'])
def vote(userId,eventId):
    if request.method=='POST':
        
        voted=request.form.get('voted')
      
        vList=(voted.lstrip(' ')).split(' ')
        print(vList)
        Vote.query.filter_by(userId=userId,eventId=eventId).first().vote=True
        for i in vList:
           
            if i:
                print(i)
                c=User.query.filter_by(email=i).first()
                print(c)
                Vote.query.filter_by(userId=c.id,eventId=eventId).first().vCount+=1
        db.session.commit()
        
        return redirect(f'/{userId}/{eventId}/explore')
    
    
    e=Event.query.get(eventId)
    registeredCandidates=[]
    for i in Vote.query.filter_by(eventId=eventId).all():
        if(i.role=='candidate' and i.candidature>=0):
            registeredCandidates+=[User.query.get(i.userId)]

    return render_template('vote-now.html',event=e,registeredCandidates=registeredCandidates,userId=userId,)

#result page
@app.route('/<eventId>/result')
def result(eventId):
    winners=[]
    losers=[]
    check=Vote.query.filter_by(eventId=eventId).all()
    e=Event.query.get(eventId)
    numWinners=e.numWinners
    mList=[]
    for i in check:
        if(i.role=='candidate' and i.candidature==0):
            j=User.query.get(i.userId)
            mList.append((j,i,i.vCount))
    mList.sort(reverse=True,key=lambda x:x[2])
    for i,j,k in mList[:numWinners]:
        winners.append((i,j))
    for i,j,k in mList[numWinners:]:
        losers.append((i,j))
    
    return render_template('result.html',eventId=eventId,winners=winners,losers=losers,voterCount=e.voterCount)

@app.route('/<userId>/org/register',methods=['GET','POST'])
def orgRegister(userId):
    user=User.query.get(userId)
    if request.method=='POST':
        u=Organizer(id=idGen('OG'),name=user.name,email=user.email,pwd=user.pwd,phone=request.form.get('phone'),org_type=request.form.get('org-type'),org_name=request.form.get('org-name'))
        db.session.add(u)
        db.session.delete(user)
        file=request.files["file"]
        
        max_size = 10*1024 * 1024

        if allowed_orgfile(file.filename):
                # Process the file (e.g., save it)
            if len(file.read()) > max_size:
                flash('File size too large!')
            else:
                file.seek(0)
                u.file=file
                dp=secure_filename(u.file.filename)
                file=str(uuid.uuid1())+"_"+dp
                u.file.save(os.path.join(app.config['UPLOAD_FOLDER'],file))
                u.file=file
                db.session.commit()
                return redirect(f'/{u.id}/organizer/dashboard')
        else:
            flash('Invalid file type')
        
        

    return render_template('reg-org.html',user=user)

@app.route('/<orgId>/organizer/dashboard',methods=['GET','POST'])
def orgDashboard(orgId):
    org=Organizer.query.get(orgId)
    if request.method=='POST':
        import datetime
        t=request.form.get('title')
        d=request.form.get('desc')
        checkNumWinners=request.form.get('checkNumWinners')
        if(checkNumWinners):
            numWinners=int(request.form.get('numWinners'))
        else:
            numWinners=1
        dateTime=request.form.get('dtpicker').split('T')
        date=dateTime[0].split('-')
        time=dateTime[1].split(':')

        stime=datetime.datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
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
        e=Event(id=idGen('EV'),organizerId=orgId,title=t,desc=d,endTime=etime,startTime=stime,createTime=datetime.datetime.now(),durHour=durHour,durMin=durMin,numWinners=numWinners)
        db.session.add(e)
        db.session.commit()

        allow=request.form.get('allowcand')
        organizerEmail=org.email
        voterCount=0
        if allow=='on':
            candidates=request.form.get('candidates').split(',')

            for i in candidates:
                if i==organizerEmail:
                    continue
                check=User.query.filter_by(email=i).first()
                if not check:
                    newregistration=User(id=idGen('US'),email=i)
                    db.session.add(newregistration)
                    db.session.commit()
                check=User.query.filter_by(email=i).first()
                r=Vote(id=idGen('VO'),eventId=e.id,userId=check.id,role='candidate')
                
                db.session.add(r)
                voterCount+=1
                db.session.commit()
        
            
            for i in voters:
                if i==organizerEmail:
                    continue
                check=User.query.filter_by(email=i).first()
                if not check:
                    newregistration=User(id=idGen('US'),email=i)
                    db.session.add(newregistration)
                    db.session.commit()
                check=User.query.filter_by(email=i).first()
                if(not Vote.query.filter_by(userId=check.id,eventId=e.id).first()):
                    r=Vote(id=idGen('VO'),eventId=e.id,userId=check.id,role='voter')
                    db.session.add(r)
                    voterCount+=1
                    db.session.commit()
        else:
            
            for i in voters:
                if i==organizerEmail:
                    continue
                check=User.query.filter_by(email=i).first()
                if not check:
                    newregistration=User(id=idGen('US'),email=i)
                    db.session.add(newregistration)
                    db.session.commit()
                check=User.query.filter_by(email=i).first()
                r=Vote(id=idGen('VO'),eventId=e.id,userId=check.id,role='candidate')
                voterCount+=1
                db.session.add(r)
                db.session.commit()
        v=Vote(id=idGen('VO'),eventId=e.id,userId=orgId,role='organizer')
        db.session.add(v)
        e.voterCount=voterCount
        db.session.commit()
        return render_template('organize_thank_you.html',orgId=orgId)
    events=Event.query.filter_by(organizerId=orgId).all()
    return render_template('org-dashboard.html',org=org,events=events)

@app.route('/public')
def public():
    return render_template('public-events.html')



# @app.route('/<eventId>/download')
# def return_files_tut(eventId):
#     import asyncio
#     from pyppeteer import launch

#     async def generate_pdf(url, pdf_path):
#         browser = await launch()
#         page = await browser.newPage()
    
#         await page.goto(url)
    
#         await page.pdf({'path': pdf_path, 'format': 'A4'})
    
#         await browser.close()

# # Run the function
#     asyncio.get_event_loop().run_until_complete(generate_pdf(f'/{eventId}/result', 'example.pdf'))

