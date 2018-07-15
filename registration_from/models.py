from flask import Flask, flash, request, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'dortmund'
bcrypt = Bcrypt(app)

# connect to server -----------------------

def db_connection(db_name):
    global mysql
    mysql = connectToMySQL(db_name)

# database queries -----------------------

def check_for_duplicate_email(data):
    query = "SELECT email FROM users WHERE email = %(email)s;"
    return mysql.query_db(query, data)

def insert_user(data):
    query = "INSERT INTO users (first_name, last_name, email, password, users_level, created_at, updated_at) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, 1, NOW(), NOW());"
    return mysql.query_db(query, data)

def check_password_match(data):
    query = "SELECT id, first_name, password, user_level FROM users WHERE email = %(email)s;"
    return mysql.query_db(query, data)

def log_message(data):
    query = "INSERT INTO messages (content, created_at, updated_at, user_id, user_id2) VALUES ({}, NOW(), NOW(), {}, {});".format(data['content'], data['creator_id'], data['recipient_id'])
    return mysql.query_db(query, data)

def retrieve_messages(data):
    query = ""
    return mysql.query_db(query, data)

def retrieve_all_users():
    query = "SELECT * FROM users WHERE id <> {};".format(session['user_id'])
    users_for_dropdown = mysql.query_db(query, data)
    return users_for_dropdown

def delete_message(data):
    query = "DELETE FROM messages WHERE id = {};".format(data['message_id'])
    return mysql.query_db(query, data)

#validations --------------------------

def validate_registration(data):   
    #name validations
    if data['firstName'].isalpha() == False or len(data['firstName']) < 2:
        flash('Invalid first name', 'firstName')
        session['firstName_validation_error'] = 'is-invalid'
        # errors.append(['Invalid first name', 'firstName'])
    if data['lastName'].isalpha() == False or len(data['lastName']) < 2:
        flash('Invalid last name', 'lastName')
        session['lastName_validation_error'] = 'is-invalid'
    #email validations    
    if not EMAIL_REGEX.match(data['email']) or len(data['email']) < 1:
        flash("Invalid email address", "email")
        session['email_validation_error'] = 'is-invalid'
    #duplicate email check
    else:
        email_check_data = data
        duplicate_email = check_for_duplicate_email(email_check_data)
        if duplicate_email:
            flash("Email address already registered", "email")
            session['email_validation_error'] = 'is-invalid'
    #password validations
    if len(request.form['password']) < 8:
        flash('Password should be more than 8 characters', 'password')
        session['password_validation_error'] = 'is-invalid'
    if request.form['password'] != request.form['confirmPassword']:
        flash('Passwords should match', 'confirmPassword')
        session['confirmPassword_validation_error'] = 'is-invalid'
    # registration fail
    if '_flashes' in session.keys():
        return False
    #registration success
    else:
        user_insert_data= {
            'firstName' : request.form['firstName'], 
            'lastName' : request.form['lastName'], 
            'email' : request.form['email'], 
            'password' : bcrypt.generate_password_hash(request.form['password'])
        }
        insert_user(user_insert_data)
        return True

def validate_login(data):
    if data['password']:
        login_data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        password_match_result = check_password_match(login_data)
        if password_match_result:
            #user validation success 
            if bcrypt.check_password_hash(password_match_result[0]['password'], login_data['password']):
                session.clear()
                session["id"] = password_match_result[0]['id']
                session["firstName"] = password_match_result[0]['first_name']
                session["userLevel"] = password_match_result[0]['user_level']
                return True           
    #user validation fail
    if request.form['email']:
        session['login-email'] = request.form['email']
    flash("You could not be logged in", "login_error")
    return False

# page assemlby ----------------

def build_wall(data)
    #retrieve users messages
    #display messages
    retrieve_all_users()
    #disply all in dropdown

# classes ---------------------
class User_Obj(object):
    def create(self, data):
        session.clear()
        session['firstName']= data['firstName']
        session['lastName']= data['lastName']
        session['email']= data['email']
        if validate_registration(data):
            session.pop('email')
            session.pop('lastName')
            session['userid'] = data['id']
            session["logged_in"] = True
            return True
        else:
            return False
    def login(self, data):
        if validate_login(data):
            session["logged_in"] = True

            return True
        else: 
            return False
    def logout(self):
        flash('You have been logged out', 'logout')
        session.clear()  #OR session['count'] = 0 OR session.clear() OR session.pop('')

class Message_Obj(object):
    def create(self, data):
        log_message(data)
        return True
    def delete(self, data):
        if session['user_id'] == data
        delete_message(data)
        return True

        






# class Database(object):
#     def check_for_duplicate_email(self, data):
#         query = "SELECT email FROM users WHERE email = %(email)s;"
#         return mysql.query_db(query, data)

#     def insert_user(self, data):
#         query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW(), NOW());"
#         return mysql.query_db(query, data)
 
#     def check_password_match(self, data):
#         query = "SELECT id, first_name, password FROM users WHERE email = %(email)s;"
#         return mysql.query_db(query, data)
        

# class Validator(object):
#     def registration(self, data):   
#     #name validations
#         if data['firstName'].isalpha() == False or len(data['firstName']) < 2:
#             flash('Invalid first name', 'firstName')
#             session['firstName_validation_error'] = 'is-invalid'
#             # errors.append(['Invalid first name', 'firstName'])

#         if data['lastName'].isalpha() == False or len(data['lastName']) < 2:
#             flash('Invalid last name', 'lastName')
#             session['lastName_validation_error'] = 'is-invalid'
#         #email validations    
#         if not EMAIL_REGEX.match(data['email']) or len(data['email']) < 1:
#             flash("Invalid email address", "email")
#             session['email_validation_error'] = 'is-invalid'
#         #duplicate email check
#         else:
#             email_check_data = data
#             duplicate_email = Database.check_for_duplicates(email_check_data)
#             if duplicate_email:
#                 flash("Email address already registered", "duplicate")
#                 session['email_validation_error'] = 'is-invalid'
#         #password validations
#         if len(request.form['password']) < 8:
#             flash('Password should be more than 8 characters', 'password')
#             session['password_validation_error'] = 'is-invalid'

#         if request.form['password'] != request.form['confirmPassword']:
#             flash('Passwords should match', 'confirmPassword')
#             session['confirmPassword_validation_error'] = 'is-invalid'

#         # registration fail
#         if '_flashes' in session.keys():
#             return False
#         #registration success
#         else:
#             user_insert_data= {
#                 'firstName' : request.form['firstName'], 
#                 'lastName' : request.form['lastName'], 
#                 'email' : request.form['email'], 
#                 'password' : bcrypt.generate_password_hash(request.form['password'])
#             }
#             Database.insert_user(user_insert_data)
#             return True

#     def login(self, data):
#         if data['password']:
#             login_data = {
#                 'email': request.form['email'],
#                 'password': request.form['password']
#             }
#             password_match_result = Database.check_password_match(login_data)
#             if password_match_result:

#                 #user validation success 
#                 if bcrypt.check_password_hash(password_match_result[0]['password'], login_data['password']):
#                     return True
                
#         #user validation fail
#         if request.form['email']:
#             session['login-email'] = request.form['email']
#         flash("You could not be logged in", "login_error")
#         return True
       
       





