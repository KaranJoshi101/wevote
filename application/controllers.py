#otp function
def Otp():
    import random
    k=0
    for i in range(6):
        k=k*10+random.randrange(0,9)
    return k


#to get username from email
def Username(e):
    if 'www.' in e:
        t=e[4:]
    else:
        t=e
        
    username=''
    for i in t:
        if i=='@':
            break
        username+=i
    return username



from flask import Flask,render_template, redirect, request,url_for
from flask import current_app as app







#home page
@app.route('/')
def home():
    return render_template('index.html')



#domain for login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        e=request.form.get('email')
        username=Username(e)
        if e=='iamadmin@gmail.com' and request.form.get('pass')=='123':   #checking admin id credentials
            return redirect(url_for('admin'))   #takes to '/admin' page
        
        return redirect('/'+username+'/home')    #takes to '/user' page
    
    return render_template('login.html') 

#domain for register page
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        
        return redirect('/'+request.form.get('email')+'/verification')
    return render_template('register1.html')

@app.route('/<email>/verification',methods=['GET','POST'])
def verify(email):
    if request.method=='POST':
        otp=request.form.get('one')+request.form.get('two')+request.form.get('three')+request.form.get('four')+request.form.get('five')+request.form.get('six')
        if otp==o:
            return redirect('/'+email+'/setpassword')
    o=Otp()
    from email.message import EmailMessage
    import ssl,smtplib
    sender='www.joshikaran3424@gmail.com'
    pwd='fmoevzvxexghzjli'
    rec=email
    sub='OTP for WeVote Application'
    body="""
    Dear"""+Username(email)+""",


    Please use the OTP below to sign into the WeVote application.


    OTP:"""+str(o)+"""


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

    return render_template('register3.html')

#domain for admin dashboard
@app.route('/admin')
def admin():
    return render_template('admin_dash.html')

#domain for user dashboard
@app.route('/<username>/home')
def user(username):
    return render_template('user_dash.html')

