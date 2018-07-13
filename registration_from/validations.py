from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
from models import Database
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

mysql = connectToMySQL('regform_1')



@app.route("/register", methods=['POST'])
def register_page():
    session.clear()
    session['firstName']= request.form['firstName']
    session['lastName']= request.form['lastName']
    session['email']= request.form['email']

class Validator(object):
    def validate_registration(self, data):
    #name validations
    if data['firstName'].isalpha() == False or len(data['firstName']) < 2:
        flash('Invalid first name', 'firstName')

    if data['lastName'].isalpha() == False or len(data['lastName']) < 2:
        flash('Invalid last name', 'lastName')
    #email validations    
    if not EMAIL_REGEX.match(data['email']) or len(data['email']) < 1:
        flash("Invalid email address", "email")
    #duplicate email check
    else:
        duplicate_email = Database.check_for_duplicates(data)
        if duplicate_email:
            flash("Email address already registered", "duplicate")
    #password validations
    if len(data['password']) < 8:
        flash('Password should be more than 8 characters', 'password')

    if data['password'] != data['confirmPassword']:
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
            'password': request.form['password']
        }

        password_match_query = "SELECT id, first_name, password FROM users WHERE email = %(email)s;"
        password_match_query_result = mysql.query_db(password_match_query, login_sub)
        if password_match_query_result:
            check = bcrypt.check_password_hash(password_match_query_result[0]['password'], login_sub['password'])

        
            #user validation success    
            if check:
                session.clear()
                session["id"] = password_match_query_result[0]['id']
                session["firstName"] = password_match_query_result[0]['first_name']
                session["logged_in"] = True
                return redirect("/wall")

                
    #user validation fail
    if request.form['email']:
        session['login-email'] = request.form['email']
    flash("You could not be logged in", "login_error")
    return redirect('/') 





