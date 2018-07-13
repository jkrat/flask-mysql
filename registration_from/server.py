from flask import Flask, flash, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'dortmund'

mysql = connectToMySQL('regform_1')

@app.route("/")
def user_form():  
     
    return render_template("index.html")

@app.route("/success")
def user_registered():
    return render_template("success.html")

@app.route("/register", methods=['POST'])
def register_page():
    user_sub = request.form

    #name validations
    if user_sub['firstName'].isalpha() == False or len(user_sub['firstName']) <= 2:
        flash('Invalid first name', 'firstName')

    if user_sub['lastName'].isalpha() == False or len(user_sub['lastName']) <= 2:
        flash('Invalid last name', 'lastName')

    #email validations    
    if not EMAIL_REGEX.match(user_sub['email']) or len(user_sub['email']) < 1:
        flash("Invalid Email Address", "email")

    #password validation
    if len(user_sub['password']) < 8:
        flash('Password should be more than 8 characters', 'password')

    if user_sub['password'] != user_sub['confirmPassword']:
        flash('Passwords should match', 'confirmPassword')

    # registration fail or success
    if '_flashes' in session.keys():
        return redirect('/')
    else:
        session["name"] = user_sub['firstName']
        flash("Invalid Email Address", "email")

        insert_query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW(), NOW());"
        mysql.query_db(insert_query, user_sub)
        
        return redirect("/success")     

@app.route("/login", methods=["POST"])
def login_user():
    login_sub = request.form
    password_match_query = "SELECT id, first_name, email, password FROM users WHERE email = %(email)s AND password = %(password)s;"
    password_match_query_result = mysql.query_db(password_match_query, login_sub)
    
    #user validation success    
    if password_match_query_result:
        session["id"] = password_match_query_result[0]['id']
        session["name"] = password_match_query_result[0]['first_name']
        session["logged_in"] = True
        debugHelp('check session')
        return redirect("/success")

    #user validation fail
    else:
        flash("You could not be logged in", "login_error")
        debugHelp('check session')
        return redirect('/')     

@app.route("/logout")
def logout_user():
    flash('You have been logged out', 'logout')
    return redirect("/")

def debugHelp(message = ""):
    print("\n\n-----------------------", message, "--------------------")
    print('REQUEST.FORM:', request.form)
    print('SESSION:', session)
    print("\n\n-------------------------------------------")

if __name__=="__main__":
    app.run(debug=True)  



