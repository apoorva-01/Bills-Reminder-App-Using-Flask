from flask import Flask, render_template, request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime, timedelta
import os
import math
import time

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
# For mail when someone sends you a message
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)
app.secret_key = 'super-secret-key'




# Connecting to local server
local_server = True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']
    
db = SQLAlchemy(app)
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    billName = db.Column(db.String(80), nullable=False)
    billCategory = db.Column(db.String(12), nullable=False)
    amount = db.Column(db.Integer)
    dueDate = db.Column(db.DateTime(3), nullable=False)
    dateOfAdd =  db.Column(db.String(120), nullable=False)
    notificationReminder= db.Column(db.Integer)
    answer = db.Column(db.String(12), nullable=False)
    repeatDays = db.Column(db.String(20), nullable=True)
    repeatTime = db.Column(db.String(20), nullable=True)
    note = db.Column(db.String(20), nullable=False)


# add Page
@app.route("/add" , methods=['GET', 'POST'])
def add():
     if (request.method=="POST"):
            billName = request.form.get('bill_name')
            billCategory = request.form.get('bill_category')
            amount = request.form.get('amount')
            dueDate = request.form.get('due_date')
            notificationReminder = request.form.get('notification_reminder')
            answer  = request.form.get('answer')
            repeatDays = request.form.get('repeat_days')
            repeatTime = request.form.get('repeat_time')
            note = request.form.get('note')   
            date_of_add=datetime.now()         
            entries = Entry(billName=billName, billCategory=billCategory, amount=amount, dueDate=dueDate, 
                notificationReminder=notificationReminder,answer =answer,repeatDays=repeatDays,repeatTime=repeatTime,
                note=note,dateOfAdd= date_of_add)
            db.session.add(entries)   
            db.session.commit()
            # delta = timedelta(days=0)
            # date_of_reminder = datetime.strptime(dueDate, '%Y-%m-%d') - delta
            # print(date_of_reminder)
            delta = timedelta(days=0,hours=8)
            date_of_reminder = datetime.strptime(dueDate, '%Y-%m-%d') - delta
            print(date_of_reminder)
            sleep_time= (date_of_reminder-date_of_add).total_seconds()
            print(sleep_time)
            time.sleep(sleep_time)
            mail.send_message('New message from ' + billName  ,
                            sender='vermaapoorva0510@gmail.com',
                            recipients = [params['gmail-user']],
                            body = "Your Note: "+note + "\n" 
                            + "Bill Nmae :" +billName+ "\n" 
                            +"Bill Category :"+billCategory+ "\n" 
                            +"Amount To Pay :"+amount+ "\n"
                            +"Due Date :"+dueDate+ "\n"
                          )


     return render_template('add.html', params=params)
    
        
# Home Page
@app.route("/")
def home():
    return render_template('index.html', params=params)


# login Page
@app.route("/login")
def login():
    return render_template('login.html', params=params)

# register Page
@app.route("/register")
def register():
    return render_template('register.html', params=params)

# search Page
@app.route("/search")
def search():
    return render_template('search.html', params=params)

# show_reminders Page
@app.route("/show_reminders")
def show_reminders():
    return render_template('show_reminders.html', params=params)

if __name__ =="__main__":
    app.run(debug=True)


