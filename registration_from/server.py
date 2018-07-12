from flask import Flask, flash, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'dortmund'

@app.route("/")
def user_form():   
    return render_template("index.html")

@app.route("/success")
def create_user():
    return render_template("success.html")

@app.route("/register", methods=['POST'])
def info_page():     

@app.route("/login", methods=["POST"])
def create_user():






def debugHelp(message = ""):
    print("\n\n-----------------------", message, "--------------------")
    print('REQUEST.FORM:', request.form)
    print('SESSION:', session)

if __name__=="__main__":
    app.run(debug=True)  



    #     #password validation
    # if len(request.form['Password']) <= 8:
    #     flash('Password should be more than 8 characters', 'password')

    # if request.form['Password'] != request.form['confirmPassword']:
    #     flash('Password and Password Confirmation should match', 'password')

    # #name validation
    # if request.form['firstName'].isalpha() == False:
    #     flash('Invalid first name provided', 'firstname')

    # if request.form['lastName'].isalpha() == False:
    #     flash('Invalid last name provided', 'lastname')

    # if not EMAIL_REGEX.match(request.form['email']) or len(request.form['email']) < 1:
    #     flash("Invalid Email Address", "email")
        
    # if '_flashes' in session.keys():
    #     return redirect('/')
    # else:
    #     return render_template('result.html', info=session['info'])