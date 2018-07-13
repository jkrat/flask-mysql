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
        flash("Email Address already exists")
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



# from flask import Flask, render_template, session, request, redirect, flash
# from mysqlconnection import connectToMySQL
# import re
# EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# app = Flask(__name__)
# app.secret_key = "ThisIsSecret!"
# @app.route("/")
# def index():
#     debugHelp("INDEX METHOD")
#     return render_template("index2.html")
   
# @app.route("/reserve", methods=['POST'])
# def reserve():
#     # Let's add validtion rules
#     if len(request.form['email']) < 1:
#         flash("Email cannot be blank!", 'email')
#     elif not EMAIL_REGEX.match(request.form['email']):
#         flash("Invalid Email Address!", 'email')
#     if len(request.form['name']) < 1:
#         flash("Name cannot be blank!", 'name')
#     elif len(request.form['name']) <= 3:
#         flash("Name must be 3+ characters", 'name')
    
#     if len(request.form['pin']) < 1:
#         flash("Pin cannot be blank!", 'pin')
#     elif request.form['pin'].isdigit() == False:
#         flash("Pin must be numeric", 'pin')
#     elif len(request.form['pin']) < 4 or len(request.form['pin'])>8:
#         flash("Pin must be 4-8 digits", 'pin')
            

#     # return "reserve"
#     if '_flashes' in session.keys():
#         return redirect("/")
#     else:
#         session["name"] = request.form['name']
#         return redirect("/success")
  
# @app.route("/success")
# def success():
#     return "Thank you " + session["name"] + ". Your seat is now reserved!"
  
# def debugHelp(message = ""):
#     print("\n\n-----------------------", message, "--------------------")
#     print('REQUEST.FORM:', request.form)
#     print('SESSION:', session)
# if __name__ == "__main__":
#     app.run(debug=True)