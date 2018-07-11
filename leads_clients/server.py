from flask import Flask, flash, render_template, redirect, request, session
from mysqlconnection import connectToMySQL
import datetime

app = Flask(__name__)

mysql = connectToMySQL('lead_gen_business')

@app.route('/')
def index():
    all_clients = mysql.query_db("SELECT * FROM clients")
    print("FETCHED all clients", all_clients)
    return render_template('index.html', friends = all_friends)

@app.route('/create_friend', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s, NOW(), NOW());"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation']
           }
    mysql.query_db(query, data)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)