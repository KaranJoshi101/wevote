#main py file for creating @
from flask import Flask, render_template, redirect, request,url_for
app=Flask(__name__)
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        if request.form.get('email')=='iamadmin@gmail.com' and request.form.get('pass')=='123':
            return redirect(url_for('admin'))
        
        return redirect('/user')
    
    return render_template('login.html')
@app.route('/register',methods=['GET','POST'])
def register():
    
    return render_template('register.html')

@app.route('/admin')
def admin():
    return render_template('admin_dash.html')
@app.route('/user')
def user():
    return render_template('user_dash.html')
if __name__=='__main__':
    app.run(debug=True)