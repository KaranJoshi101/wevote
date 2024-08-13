#import flask module
from flask import Flask, render_template, redirect, request,url_for

#create flask object
app=Flask(__name__)

#home page
@app.route('/')
def home():
    return render_template('index.html')



#domain for login page
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.form.get('email')=='iamadmin@gmail.com' and request.form.get('pass')=='123':   #checking admin id credentials
            return redirect(url_for('admin'))   #takes to '/admin' page
        
        return redirect('/user')    #takes to '/user' page
    
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
@app.route('/user')
def user():
    return render_template('user_dash.html')


if __name__=='__main__':
    app.run(debug=True)