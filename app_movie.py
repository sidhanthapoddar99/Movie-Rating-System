from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import sqlite3
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
import numpy as np
import Algorithmia

#to add the nltk corpora for heroku integration
#nltk.data.path.append('/nltk_data')

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('LandingPage.html')

#TO CONTROL ADMIN ACCSS RIGHTS AND LOGIN
@app.route('/admin', methods =['GET', 'POST'])
def admin():
        return render_template('adminlogin.html')

@app.route('/admincheck_cred', methods = ['GET', 'POST'])
def admin_check():
        username  = request.form['UserName']
        password = request.form['Password']


        if username == 'admin':
                if password == '123456789':
                        return render_template('adminportal.html')
                else:
                        return render_template('unsuccessfulloginattempt.html')
        else:
                return render_template('unsuccessfulloginattempt.html')

#ADMIN FUNCTION OPTIONS :
@app.route('/deluseracc', methods = ['GET', 'POST'])
def deluseracc():
        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('DELETE FROM User_Auth')
                con.commit
                
        return render_template('deleteaccountconf.html')

@app.route('/deluseractivity', methods = ['GET', 'POST'])
def deluseractivity():
        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('DELETE FROM User_Info')
                con.commit
                
        return render_template('deleteactivityconf.html')
        
        return

@app.route('/viewuseracc', methods = ['GET', 'POST'])
def viewuseracc():
        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('SELECT*FROM User_Auth')
                rows = cur.fetchall()
                
        return render_template('displayaccountinfo.html', items = rows)


@app.route('/viewuseractivity', methods = ['GET', 'POST'])
def viewuseractivity():
        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('SELECT*FROM User_Info')
                rows = cur.fetchall()
                
        return render_template('displayactivityinfo.html', items = rows)

#TO SIGNUP
@app.route('/sign_up', methods = ['GET', 'POST'])
def signup():
       return render_template('sign_up.html')

@app.route('/signup_input', methods = ['GET', 'POST'])
def signupinput():
        username = request.form['UserName']
        password = request.form['Password']
        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('''INSERT INTO User_Auth VALUES(?,?)''',(username, password))
                
        return render_template('signupconf.html')

#TO LOGIN
@app.route('/login', methods = ['GET','POST'])
def loginpagerender():
        return render_template('login.html')

@app.route('/login_input',methods = ['GET','POST'] )
def logincheck():
        username = request.form['UserName']
        password = request.form['Password']
        print(username)
        print(password)

        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('SELECT Password from User_Auth where UserId =?''',(username,))
                correct_pass = cur.fetchall()
        if(correct_pass[0][0] == password):
                #redirect to user profile portal to start again
                return render_template('successfullogin.html')
        else:
                #redirect to homepage to start process again
                return render_template('unsuccessfulloginattempt.html')

        
#AFTER SUCCESSFUL LOGIN - ACCESS USER PORTAL 
@app.route('/portal', methods = ['GET','POST'])
def portal_access():
        return render_template('portallandingpage.html')

#TO make a new prediction for logged in user : 
@app.route('/makepred', methods = ['GET','POST'])
def makepred():
        return render_template('makepreduser.html')
@app.route('/results_loggedin_users', methods =['GET', 'POST'])
#THIS FUNCTION IS RESPONSIBLE FOR ADDING ALL THE USER DETAILS WHENEVER ANY PREDICTION IS MADE BY A LOGGED IN USER
def results2():
        username = str(request.form['UserName'])
        sentence = str(request.form['review'])

        client = Algorithmia.client('simSZn2DdvecQYvltU1jrAhh2es1')
        algo = client.algo('nlp/ProfanityDetection/1.0.0')
        algo.set_options(timeout=300) # optional
        a= algo.pipe(sentence).result
        if len(a.keys()) == 0:
                
        
                sid = SentimentIntensityAnalyzer()
                ss = sid.polarity_scores(sentence)
                if ss['compound']<0:
                        score = 10-abs((ss['compound']*10))+0.5
                else:
                        score = (ss['compound']*10)-0.5

                #now we will add the above  details to the users info db so that he/she can view it in the history section

                with sqlite3.connect('softwareproject.db') as con:
                        cur = con.cursor()
                        cur.execute('SELECT Password from User_Auth where UserId =?''',(username,))
                        correct_pass = cur.fetchall()
                        user_pass = correct_pass[0][0]
                with sqlite3.connect('softwareproject.db') as con:
                        cur = con.cursor()
                        cur.execute('''INSERT INTO User_Info VALUES (?,?,?,?)''',(username, user_pass, sentence, score))
                        
                        
                return render_template('results.html', res=score)

        else:
                return render_template('profanity.html')


#TO view user history
@app.route('/viewhistory', methods =['GET', 'POST'])
def view_history():
        return render_template('history.html')

@app.route('/show_history', methods=['GET', 'POST'])
def show_history():
        username = request.form['UserName']
        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('SELECT Reviews, Ratings from User_Info where UserId =?''',(username,))
                rows = cur.fetchall()

        return render_template('display_history.html', items = rows, uname = username)


#TO DELETE LOGGED-IN USER'S HISTORY
@app.route('/deletehistory', methods=['GET', 'POST'])
def del_history():
        return render_template('deletehistory.html')
@app.route('/confirm_delete_user_info', methods = ['GET', 'POST'])
def conf_del_user_history():
        username = request.form['UserName']
        with sqlite3.connect('softwareproject.db') as con:
                cur = con.cursor()
                cur.execute('DELETE FROM User_Info where UserId =?''',(username,))
                con.commit
        return render_template('confuserinfodelete.html', uname=username)
#Separate rendering for rate now button
@app.route('/testresult', methods=['GET', 'POST'])
def testresult():
        return render_template('testresult.html')

#TO PLAY AROUND WITH MOVIE RATING WITHOUT LOGIN
@app.route('/results', methods=['POST'])
def predict():
        sentence = str(request.form['review'])

        client = Algorithmia.client('simSZn2DdvecQYvltU1jrAhh2es1')
        algo = client.algo('nlp/ProfanityDetection/1.0.0')
        algo.set_options(timeout=300) # optional
        a= algo.pipe(sentence).result
        if len(a.keys()) == 0:

                sid = SentimentIntensityAnalyzer()
                ss = sid.polarity_scores(sentence)
                
                if ss['compound']<0:
                        score = 10-abs((ss['compound']*10))+0.5
                else:
                        score = (ss['compound']*10)-0.5
                
                return render_template('results.html', res=score)
        else:
                return render_template('profanity.html')

@app.errorhandler(500)
def page_not_found(e):
        #in case of internal server error

        return render_template('error.html')

if __name__ == '__main__':
	app.run(debug=True)
