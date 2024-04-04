from flask import Flask,render_template,request,redirect,session
from pymongo import MongoClient
import boto3
app = Flask(__name__)
import smtplib

server = smtplib.SMTP('smtp.gmail.com',587)
sender_email ='aasreethakamireddy@gmail.com'
sender_pass = 'tlkgxfjwxuvxebye'
ses = boto3.client('ses')

cluster = MongoClient('mongodb://127.0.0.1:27017')
db = cluster['massemail']
users = db['users']

app.secret_key="!@#$JHGF#$%^&ytgv"

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/login',methods=['get'])
def login():
    return render_template('signin.html')

@app.route('/signup',methods=['get'])
def signup():
    return render_template('signup.html')

@app.route('/dashboard',methods=['get'])
def dash():
    return render_template('dash.html')

@app.route('/compose',methods=['get'])
def com():
    email = request.args.get('emails')
    return render_template('subject.html',data=email)

@app.route('/sendemail',methods=['post'])
def send():
    msg = request.form['msg']
    email = request.form['email']
    emails = email.split(',')
    sub = request.form['subject']
    ses.send_email(
    Destination={
        'ToAddresses': emails
    },
    Message={
        'Body': {
            'Text': {
                'Charset': 'UTF-8',
                'Data': msg,
            }
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': sub,
        },
    },
    Source='aasreethakamireddy@gmail.com'
    ) 
    return render_template('subject.html',ack="mail sent")

@app.route('/login',methods=['post'])
def auth():
    email = request.form['email']
    password = request.form['password']
    user = users.find_one({"email":email,"password":password})
    if not user:
        return render_template('signin.html',status="user not found with detailsyo entered ")
    session['email'] = email
    return redirect('/dashboard')


@app.route('/signup',methods=['post'])
def sign():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    cpass = request.form['cpassword']
    if password != cpass:
        return render_template('signup.html',status="Password mismatch")
    user = users.find_one({"email":email})
    if user:
        return render_template('signup.html',status="User alreay exist with same email id")
    document = {"name":name,"email":email,"password":password}
    users.insert_one(document)
    return redirect('/login')

if __name__=="__main__":
    app.run()