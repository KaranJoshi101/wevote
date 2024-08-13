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
        if 'www.' in e:
            t=e[4:]
        else:
            t=e
        
        username=''
        for i in t:
            if i=='@':
                break
            username+=i
        if e=='iamadmin@gmail.com' and request.form.get('pass')=='123':   #checking admin id credentials
            return redirect(url_for('admin'))   #takes to '/admin' page
        
        return redirect('/'+username+'/home')    #takes to '/user' page
    
    return render_template('login.html') 

#domain for register page
@app.route('/register',methods=['GET','POST'])
def register():
    
    return render_template('register.html')

#domain for admin dashboard
@app.route('/admin')
def admin():
    return render_template('admin_dash.html')

#domain for user dashboard
@app.route('/<username>/home')
def user(username):
    return render_template('user_dash.html')

