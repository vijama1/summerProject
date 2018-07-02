#!/usr/bin/python3
'''
IMPORTS :

 1. Flask from flask
 2. getting_label_file -----> to capture photo and get labels of th image
'''
import time
from flask import Flask,render_template,request
import mysql.connector as mysql
import cv2
import kairos_face as kf
import matplotlib.pyplot as plt
import json
from gtts import gTTS
import os
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import smtplib
import re
import socket
import dns.resolver

kf.settings.app_id = 'ed6e261d'
kf.settings.app_key = 'bfe71f59834f765f8b215a06e9861434'

conn = mysql.connect(user='root', password='password', database='flask', host='localhost')
cursor = conn.cursor()

app = Flask(__name__)

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

@app.route('/register')
def register():
    # speak message
    os.system("mpg321 register.wav")
    os.system("mpg321 pic_not.wav")

    # register page--->enter details---->that will be sent to image_cap
    return render_template('register.html')

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

@app.route('/image_cap', methods=['GET', 'POST'])
# to insert values obtained from register page to database
def image_cap():
    print('entered')
    if request.method == 'POST':

        name = request.form['name']
        number = int(request.form['number'])
        def isValid(s):
            Pattern = re.compile("(0/91)?[7-9][0-9]{9}")
            return Pattern.match(number)
        if (isValid(number)):
            email = request.form['email']
            password = request.form['password']
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
            records=""
            if match == None:
                print('Bad Syntax in ' + addressToVerify)
                raise ValueError('Bad Syntax')
            domain_name = email.split('@')[1]
            try:
                records = dns.resolver.query(domain_name, 'MX')
            except:
                #print(records[0])
                print("Invalid domain")
            str_domain_name=str(records)
            if 'object' in str_domain_name.split():
                print("Valid domain")
            #print(records)
            if records!="":

            #print(records[0])
                mxRecord = records[0].exchange
                #print(mxRecord)
                mxRecord = str(mxRecord)
                # # print(mxRecord)
                #print("=========")
                host = socket.gethostname()
                #print(host)
                server = smtplib.SMTP()
                server.connect(mxRecord)
                server.helo(host)
                server.mail('sample@qwerty.com')
                code, message = server.rcpt(str(email))
                server.quit()
                if code == 250:
                    cam = cv2.VideoCapture(0)
                    frame = cam.read()[1]
                    cv2.imwrite('face.jpg',frame)
                    cam.release()

                    enrolled_face = kf.enroll_face(file='face.jpg', subject_id=str(email), gallery_name='a-gallery')
                    face_id=enrolled_face['face_id']
                    status = enrolled_face['images'][0]['transaction']['status']
                    if status=="success":
                        # execute query to insert data
                        out = cursor.execute('insert into flask_use values("%s","%d","%s","%s","%s")'%(name,number,email,password,face_id))
                        conn.commit()
                        return render_template('image_cap.html')
                    else:
                        return '<h1>Non-Human detected</h1>'
                else:
                    return '<h1>Error</h1>'
            else:
                return '<h1>Invalid Email</h1>'
        else :
            print ("Invalid Number")
            return '<h1>Invalid Number</h1>'      








#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

@app.route('/login')
def login():

    # Playing the converted fil
    os.system("mpg321 login.wav")
    os.system("mpg321 pic_verf.wav")
    return render_template('login.html')

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if request.method == 'POST':
        print("<h1>in file</h1>")
        cam = cv2.VideoCapture(0)
        frame = cam.read()[1]
        cv2.imwrite('face2.jpg',frame)
        cam.release()

        emaill = request.form['email']
        passwordd = request.form['password']

        cursor.execute('select * from flask_use where email="%s" and password="%s"'%(emaill,passwordd))
        login_details = cursor.fetchall()

        recognized_faces = kf.recognize_face(file='face2.jpg', gallery_name='a-gallery')
        status = recognized_faces['images'][0]['transaction']['status']

        if len(login_details)==0:
            return '<h1>Unregistered E-mail or Password</h1>'
        else:
            if status=="success":
                os.system("mpg321 dash.wav")
                return render_template('dashboard.html')
            elif status=="failure":
                os.system("mpg321 not_reg.wav")
                return "<h1>Face not registered</h1>"
            else:
                return "Error please retry"
    else:
        return 'sss'
@app.route('/result', methods=['GET','POST'])
def result():
    if request.method == 'POST':
        company = request.form['company']
        open = float(request.form['open'])
        high = float(request.form['high'])
        low = float(request.form['low'])
        adj = float(request.form['adj'])
        volume = float(request.form['volume'])

        def apple():
            df = pd.read_csv('Apple.csv')
            train_data = df[['Open','High','Low','Adj Close','Volume']]
            train_target = df[['Close']]

            # Create linear regression object
            regr = linear_model.LinearRegression()

            # Train the model using the training sets
            regr.fit(train_data,train_target)

            # Make predictions using the testing set-------2d required
            #y_pred = regr.predict(df[['Open','High','Low','Adj Close','Volume']])
            y_pred = regr.predict([[open,high,low,adj,volume]])
            return round(y_pred[0][0],3)


        def reliance():
            df = pd.read_csv('reliance.csv')
            df = df.dropna(subset=['Open','High','Low','Adj Close','Volume','Close'])
            train_data = df[['Open','High','Low','Adj Close','Volume']]
            train_target = df[['Close']]

            # Create linear regression object
            regr = linear_model.LinearRegression()

            # Train the model using the training sets
            regr.fit(train_data,train_target)

            # Make predictions using the testing set-------2d required
            #y_pred = regr.predict(df[['Open','High','Low','Adj Close','Volume']])
            y_pred = regr.predict([[open,high,low,adj,volume]])
            return round(y_pred[0][0],3)


        def infosis():
            df = pd.read_csv('infosis.csv')
            df = df.dropna(subset=['Open','High','Low','Adj Close','Volume','Close'])
            train_data = df[['Open','High','Low','Adj Close','Volume']]
            train_target = df[['Close']]

            # Create linear regression object
            regr = linear_model.LinearRegression()

            # Train the model using the training sets
            regr.fit(train_data,train_target)

            # Make predictions using the testing set-------2d required
            #y_pred = regr.predict(df[['Open','High','Low','Adj Close','Volume']])
            y_pred = regr.predict([[open,high,low,adj,volume]])
            return round(y_pred[0][0],3)


        def tcs():
            df = pd.read_csv('tcs.csv')
            df = df.dropna(subset=['Open','High','Low','Adj Close','Volume','Close'])
            train_data = df[['Open','High','Low','Adj Close','Volume']]
            train_target = df[['Close']]

            # Create linear regression object
            regr = linear_model.LinearRegression()

            # Train the model using the training sets
            regr.fit(train_data,train_target)

            # Make predictions using the testing set-------2d required
            #y_pred = regr.predict(df[['Open','High','Low','Adj Close','Volume']])
            y_pred = regr.predict([[open,high,low,adj,volume]])
            return round(y_pred[0][0],3)

        close_price = 0
        if company=='Apple':
            os.system("mpg321 apple.wav")
            close_price = apple()
            myobj = gTTS(text="the closing price should be "+str(close_price)+" US Dollars", lang='en', slow=True)
            myobj.save("res.wav")
            os.system("mpg321 res.wav")
            return render_template('result_apple.html', variable = "$ "+str(close_price))

        elif company=='Tcs':
            os.system("mpg321 tcs.wav")
            close_price = tcs()
            myobj = gTTS(text="the closing price should be "+str(close_price)+" US Dollars", lang='en', slow=True)
            myobj.save("res.wav")
            os.system("mpg321 res.wav")
            return render_template('result_tcs.html', variable = "$ "+str(close_price))

        elif company=='Infosis':
            os.system("mpg321 infosis.wav")
            close_price = infosis()
            myobj = gTTS(text="the closing price should be "+str(close_price)+" US Dollars", lang='en', slow=True)
            myobj.save("res.wav")
            os.system("mpg321 res.wav")
            return render_template('result_infosis.html', variable = "$ "+str(close_price))

        else:
            os.system("mpg321 reliance.wav")
            close_price = reliance()
            myobj = gTTS(text="the closing price should be "+str(close_price)+" US Dollars", lang='en', slow=True)
            myobj.save("res.wav")
            os.system("mpg321 res.wav")
            return render_template('result_reliance.html', variable = "$ "+str(close_price))

    else:
        return 'ERROR OCCURED'



#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

if __name__ == '__main__':

    app.run(host='0.0.0.0',port=9998)
