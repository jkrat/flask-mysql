from flask import Flask, flash, render_template, redirect, request, session
from mysqlconnection import connectToMySQL
import datetime

app = Flask(__name__)

mysql = connectToMySQL('friendsdb')

# Routes -------------

@app.route('/')
def index_route():
    return index()

@app.route('/create_friend', methods=['POST'])
def create_route():
    return create_friend()


# Views -------------

def index():
    friends = Friend.find_all()
    return render_template('index.html', friends = friends)

def create_friend():
    Friend.add(request.form)
    return redirect('/')

# Models -------------
class FriendFactory(object):
    def add(self, data):
        query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(occupation)s, NOW(), NOW());"
        return mysql.query_db(query, data)
    def find_all(self):
        return mysql.query_db("SELECT * FROM friends")
    # def find_by_first_name(self, firstName):
    #     return mysql.query_db("SELECT * FROM friends WHERE first_name = firstName")
    # def find_by_first_name(self, lastName):
    #     return mysql.query_db("SELECT * FROM friends WHERE last_name = lastName)
    # def find_by_first_name(self, occupation):
    #     return mysql.query_db("SELECT * FROM friends WHERE occupation = occupation")

Friend = FriendFactory()


if __name__ == "__main__":
    app.run(debug=True)


