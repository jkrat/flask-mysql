from flask import Flask, flash, render_template, redirect, request, session
from mysqlconnection import connectToMySQL
from datetime import datetime
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'dortmund'

mysql = connectToMySQL('emailValidation')

@app.route('/')
def index():
    return render_template('index.html', all_emails = all_emails)

@app.route('/create_email', methods=['POST'])
def checkEmail():
    timestamp = datetime.strftime(datetime.now(), "%Y/%m/%d %I:%M%p")
    user = {
        'email': request.form['email'],
        'timestamp': timestamp
    }    
    if not EMAIL_REGEX.match(user['email']) or len(user['email']) < 1:
        flash("Invalid Email Address")
        print("invald")
    elif:
        matches = SELECT id FROM emails WHERE email = {user.email} LIMIT 1;
        if len(matches) > 0:    
            flash("Email Address already exists")
            print("duplicate")
    if '_flashes' in session.keys():
        return redirect('/')
    else:
        query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());""
        user_list = mysql.query_db(query, user)
        return redirect('/valid_email')

@app.route('/valid_email')
def createEmail():
    all_emails = mysql.query_db("SELECT email, created_at FROM emails")
    return render_template('success.html', all_emails = all_emails)

if __name__ == "__main__":
    app.run(debug=True)