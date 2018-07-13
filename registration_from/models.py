from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re 

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)

mysql = connectToMySQL('regform_1')


class Database(object):
    def check_for_duplicates(self, data):
        query = "SELECT email FROM users WHERE email = %(email)s;"
        return mysql.query_db(query, data)

    def insert_user(self, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(firstName)s, %(lastName)s, %(email)s, %(password)s, NOW(), NOW());"
        return mysql.query_db(query, data)
 
    def check_password_match(self, data):
        query = "SELECT id, first_name, password FROM users WHERE email = %(email)s;"
        return mysql.query_db(query, data)
        
        




