from flask import Flask, render_template, request,session,redirect, url_for,flash,abort
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
import json
from datetime import datetime, timedelta, date
import os
import math
import time
import sched
import threading
from threading import Thread
import atexit
# from flask.exe.login  import LoginManager,LoginForm,login_user,bcrypt,login_required,current_user,logout_user
# login_manager = LoginManager()

with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
# login_manager.init_app(app)

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
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    phoneNo = db.Column(db.Integer, nullable=False)


# instance is created for sheduling
scheduler = sched.scheduler(time.time,time.sleep)






# Add Page
@app.route("/add" , methods=['GET', 'POST'])
def add():
     if (request.method=="POST"):
            billName = request.form.get('bill_name')
            billCategory = request.form.get('bill_category')
            amount = request.form.get('amount')
            dueDate = request.form.get('due_date')
            notificationReminder =int( request.form.get('notification_reminder'))
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

            
            def sendEmail():
                msg = Message(subject="Reminding Your Bill",sender='vermaapoorva0510@gmail.com',
                recipients=[params['gmail-user']])
                msg.html = render_template('mail.html')
                mail.send(msg)


            


            how_many_days_before_notification = timedelta(days=notificationReminder,hours=13,minutes=55)
            date_of_reminder = datetime.strptime(dueDate, '%Y-%m-%d') - how_many_days_before_notification
            print(date_of_reminder)  


            # e1 = scheduler.enter(sleep_time, 1, sendEmail, ())
            # scheduler.run()
            time.sleep(5)
            sendEmail()
            
            sleep_time= (date_of_reminder-date_of_add).total_seconds()
            print(sleep_time)
           
     return render_template('add.html', params=params)
    


# Home Page
@app.route("/")
def home():
    return render_template('index.html', params=params)


# login Page
@app.route("/login")
def login():
    return render_template('login.html', params=params)


# @app.route('/reports')
# @login_required
# def reports():
#     """Run and display various analytics reports."""
#     products = Product.query.all()
#     purchases = Purchase.query.all()
#     purchases_by_day = dict()
#     for purchase in purchases:
#         purchase_date = purchase.sold_at.date().strftime('%m-%d')
#         if purchase_date not in purchases_by_day:
#             purchases_by_day[purchase_date] = {'units': 0, 'sales': 0.0}
#         purchases_by_day[purchase_date]['units'] += 1
#         purchases_by_day[purchase_date]['sales'] += purchase.product.price
#     purchase_days = sorted(purchases_by_day.keys())
#     units = len(purchases)
#     total_sales = sum([p.product.price for p in purchases])

#     return render_template(
#         'reports.html',
#         products=products,
#         purchase_days=purchase_days,
#         purchases=purchases,
#         purchases_by_day=purchases_by_day,
#         units=units,
#         total_sales=total_sales)




# # login Page
# @app.route("/login")
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.get(form.email.data)
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 user.authenticated = True
#                 db.session.add(user)
#                 db.session.commit()
#                 login_user(user, remember=True)
#                 return redirect(url_for("bull.reports"))
#     return render_template("login.html", form=form)



# @app.route("/logout", methods=["GET"])
# @login_required
# def logout():
#     """Logout the current user."""
#     user = current_user
#     user.authenticated = False
#     db.session.add(user)
#     db.session.commit()
#     logout_user()
#     return render_template("logout.html")




# def is_active(self):
#         """True, as all users are active."""
#         return True

# def get_id(self):
#         """Return the email address to satisfy Flask-Login's requirements."""
#         return self.email

# def is_authenticated(self):
#         """Return True if the user is authenticated."""
#         return self.authenticated

# def is_anonymous(self):
#         """False, as anonymous users aren't supported."""
#         return False
        


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)






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



# Errr Handler Page   
# @app.errorhandler(404)
# def not_found(error):
#     resp = make_response(render_template('error.html'), 404)
#     resp.headers['X-Something'] = 'A value'
#     return resp



if __name__ =="__main__":
    app.run(debug=True)


