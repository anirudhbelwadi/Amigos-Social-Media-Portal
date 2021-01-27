#importing dependecies
from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
from datetime import timedelta
import os

app=Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=1)
app.secret_key='amigos'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

#root route
@app.route('/')
def home():
    if "uname" in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
#login route
@app.route('/login')
def login():
    if "uname" in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

#register route
@app.route('/register')
def register():
    return render_template('register.html')

#registration confirm
@app.route('/confirmregister', methods=['POST'])
def confirmregister():
    #request data from form
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    mobile = request.form['mobile']
    #Make a connection
    myconnection = sqlite3.connect('assets/static/db/user.db')
    #Make a cursor which will perform certain actions
    mycursor = myconnection.cursor()
    #Execute Given action
    mycursor.execute("INSERT INTO users VALUES (:userName,:emailID,:password,:firstName,:lastName,:mobileNo)",
    {'userName':username,'emailID':email,'password':password,'firstName':firstname,'lastName':lastname,'mobileNo':mobile})
    #Take ackkonwledgement
    myconnection.commit()
    #Close Connection
    myconnection.close()
    return "1"

@app.route('/loginconfirm', methods=['POST'])
def loginconfirm():
    username=request.form['username']
    password=request.form['password']
    myconnection = sqlite3.connect('assets/static/db/user.db')
    #Make a cursor which will perform certain actions
    mycursor = myconnection.cursor()
    #Execute Given action
    a=mycursor.execute("SELECT password FROM users WHERE userName=:username", 
            {'username':username})
    for b in a:
        c=b
    if(password==c[0]):
        print(password)
        session.permanent=True
        session['uname'] = username
        myconnection.commit()
        myconnection.close()
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    if request.files['fileUpload']:
        f = request.files['fileUpload']
        f_name='assets/feed/uploads/'+f.filename
        uploadedIMG = os.path.join(f_name)
        f.save(uploadedIMG)
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop("uname",None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)