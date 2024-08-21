#otp function
def Otp():
    import random
    k=0
    for i in range(6):
        k=k*10+random.randrange(0,9)
    return k

def Username(e):
    if 'www.' in e:
        e=e[4:]
    newe=''
    for i in e:
        if i=='@':
            break
        newe+=i
    return newe


from flask import Flask,render_template, redirect, request,url_for
from flask import current_app as app
from .models import *







#home page
@app.route('/')
def home():
    return render_template('index.html')



#domain for login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        e=request.form.get('email')
        p=request.form.get('pass')
        
        if e=='iamadmin@gmail.com' and p=='123':   #checking admin id credentials
            return redirect(url_for('admin'))   #takes to '/admin' page
        rec=User.query.filter_by(email=e).first()
        if rec:
            if rec.pwd==p:
                return redirect('/'+e+'/home') 
            else:
                return render_template('login-wrong-pass.html')
        else:
            return 'email does not exist register->'

           #takes to '/user' page
    
    return render_template('login.html') 

#domain for register page
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        email=request.form.get('email')
        check=User.query.filter_by(email=email,registered=True).first()
        if check:
            return 'email already exists go to login page'
        return redirect('/'+email+'/verification')
    return render_template('register1.html')

@app.route('/<email>/verification',methods=['GET','POST'])
def verify(email):
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


@app.route('/<email>/setpassword',methods=['GET','POST'])
def setpassword(email):
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

#domain for admin dashboard
@app.route('/admin')
def admin():
    return render_template('admin_dash.html')

#domain for user dashboard
@app.route('/<email>/home')
def user(email):
    rec=User.query.filter_by(email=email).first()
    return render_template('user_dash.html',email=email,name=rec.name)


#domain for organize
@app.route('/<email>/organize',methods=['GET','POST'])
def org(email):
    if request.method=='POST':
        import datetime
        t=request.form.get('title')
        d=request.form.get('desc')
        ti=request.form.get('stime')
        print(ti,type(ti))
        sdate=datetime.datetime(int(request.form.get('syear')),int(request.form.get('smonth')),int(request.form.get('sdate')))
        stime=datetime.time(int(ti[:2]),int(ti[3:]))
        l=request.form.get('voters')
        c=request.form.get('cand')
        rec=User.query.filter_by(email=email).first()
        e=Event(user_id=rec.id,title=t,desc=d,time=stime,sdate=sdate)
        db.session.add(e)
        db.session.commit()
    return render_template('organize.html',email=email)


