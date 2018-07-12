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
    return render_template('index.html')

@app.route('/create_email', methods=['POST'])
def checkEmail():
    timestamp = datetime.strftime(datetime.now(), "%Y/%m/%d %I:%M%p")
    user = {
        'email': request.form['email'],
    }  
    duplicate_query = "SELECT * FROM emails WHERE email = %(email)s LIMIT 1;"
    user_list = mysql.query_db(duplicate_query, user)  
    if not EMAIL_REGEX.match(user['email']) or len(user['email']) < 1:
        flash("Invalid Email Address")
    elif len(user_list) > 0:   
        print("************ user list ********* \n", user['email'], user_list) 
        flash("Email Address already exists")
        print("duplicate")
    if '_flashes' in session.keys():
        return redirect('/')
    else:
        input_query = "INSERT INTO emails (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
        mysql.query_db(input_query, user)
        return redirect('/display_email')

@app.route('/display_email')
def displayEmail():
    all_emails = mysql.query_db("SELECT email, created_at FROM emails")
    return render_template('success.html', all_emails = all_emails)

@app.route('/delete', methods=['POST'])
def delete_email():
    entry_to_delete = {
        'entry': request.form['entry']
    }
    delete_query = "DELETE FROM `emailValidation`.`emails` WHERE `email`= %(entry)s;"
    mysql.query_db(delete_query, entry_to_delete)
    return redirect('/display_email')

@app.route('/return')
def return_to_main():
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)