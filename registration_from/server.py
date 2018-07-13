from flask import Flask, flash, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'dortmund'
bcrypt = Bcrypt(app)

mysql = connectToMySQL('regform_1')

@app.route("/")
def user_form():  
    return render_template("index.html")

@app.route("/success")
def user_registered():
    return render_template("success.html")

@app.route("/wall")
def enter_sites():
    return render_template("success.html")

@app.route("/register", methods=['POST'])
def register_page():
    session.clear()
    session['firstName']= request.form['firstName']
    session['lastName']= request.form['lastName']
    session['email']= request.form['email']
    #name validations
    if request.form['firstName'].isalpha() == False or len(request.form['firstName']) < 2:
        flash('Invalid first name', 'firstName')

    if request.form['lastName'].isalpha() == False or len(request.form['lastName']) < 2:
        flash('Invalid last name', 'lastName')
    #email validations    
    if not EMAIL_REGEX.match(request.form['email']) or len(request.form['email']) < 1:
        flash("Invalid email address", "email")
    #duplicate email check
    else:
        email_duplicate_query = "SELECT email FROM users WHERE email = %(email)s;"
        email_duplicate_query_result = mysql.query_db(email_duplicate_query, request.form)
        if email_duplicate_query_result:
            flash("Email address already registered", "duplicate")
    #password validations
    if len(request.form['password']) < 8:
        flash('Password should be more than 8 characters', 'password')

    if request.form['password'] != request.form['confirmPassword']:
        flash('Passwords should match', 'confirmPassword')

    # registration fail
    if '_flashes' in session.keys():
        return redirect('/')
    #registration success
    else:
        user_sub = {
            'firstName' : request.form['firstName'], 
            'lastName' : request.form['lastName'], 
            'email' : request.form['email'], 
            'password' : bcrypt.generate_password_hash(request.form['password'])
    }
        insert_query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW(), NOW());"
        mysql.query_db(insert_query, user_sub)
        session["logged_in"] = True
        return redirect("/success")     

@app.route("/login", methods=["POST"])
def login_user():
    if request.form['password']:
        login_sub = {
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        password_match_query = "SELECT id, first_name, email FROM users WHERE email = %(email)s AND password = %(password)s;"
        password_match_query_result = mysql.query_db(password_match_query, login_sub)
        # bcrypt.check_password_hash(password_match_query_result['password'], request.form['password'])
        print("\n\n-------------------------------------------")
        print('SESSION:', login_sub['password'])
        print("\n\n-------------------------------------------")
        print('SESSION:', password_match_query_result)
        
        #user validation success    
        if password_match_query_result:
            session.clear()
            session["id"] = password_match_query_result[0]['id']
            session["firstName"] = password_match_query_result[0]['first_name']
            session["logged_in"] = True
            return redirect("/wall")

        #user validation fail
        else:
            session['login-email'] = request.form['email']
            flash("You could not be logged in", "login_error")
            return redirect('/') 
    else:
        if request.form['email']:
            session['login-email'] = request.form['email']
        flash("You could not be logged in", "login_error")
        return redirect('/') 


@app.route("/logout")
def logout_user():
    flash('You have been logged out', 'logout')
    session.clear()  #OR session['count'] = 0 OR session.clear() OR session.pop('')
    return redirect("/")

def debugHelp(message = ""):
    print("\n\n-----------------------", message, "--------------------")
    print('REQUEST.FORM:', request.form)
    print('SESSION:', session)
    print("\n\n-------------------------------------------")

if __name__=="__main__":
    app.run(debug=True)  



