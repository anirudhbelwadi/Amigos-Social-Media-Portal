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

#Home Page
@app.route('/')
def home():
    if "uname" in session:
        uname=session["uname"]
        return render_template('index.html',uname=uname)
    else:
        return redirect(url_for('login'))

#Feed
@app.route('/feed')
def feed():
    if "uname" in session:
        uname=session["uname"]
        return render_template('feed.html',uname=uname)
    else:
        return redirect(url_for('login'))
        
#login
@app.route('/login')
def login():
    if "uname" in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

#Reisteration
@app.route('/register')
def register():
    if "uname" in session:
        return redirect(url_for('home'))
    else:
        return render_template('register.html')

#Registration confirmation
@app.route('/confirmregister', methods=['POST','GET'])
def confirmregister():
    if(request.method == 'POST'):
        #request data from form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        mobile = request.form['mobile']
        #Make a connection
        myconnection = sqlite3.connect('static/assets/db/user.db')
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
    else:
        if "uname" in session:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

#Login confirmation
@app.route('/loginconfirm', methods=['POST','GET'])
def loginconfirm():
    if(request.method == 'POST'):
        username=request.form['username']
        password=request.form['password']
        myconnection = sqlite3.connect('static/assets/db/user.db')
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
    else:
        if "uname" in session:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

#Upload images/Add Feed
@app.route('/upload', methods=['POST','GET'])
def upload():
    if(request.method == 'POST'):
        if request.files['fileUpload']:
            f = request.files['fileUpload']
            f_name='assets/feed/uploads/'+f.filename
            uploadedIMG = os.path.join(f_name)
            f.save(uploadedIMG)
            return redirect(url_for('home'))
        return redirect(url_for('home'))
    else:
        if "uname" in session:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

#Logout
@app.route('/logout')
def logout():
    if "uname" in session:
        session.pop("uname",None)
    return redirect(url_for('login'))    

if __name__ == "__main__":
    app.run(debug=True)