from flask import Flask, flash, render_template, redirect, request, session
from mysqlconnection import connectToMySQL
import datetime

app = Flask(__name__)
app.secret_key = 'dortmund'

mysql = connectToMySQL('lead_gen_business')

@app.route('/')
def index():
    client_lead_count = mysql.query_db("SELECT COUNT(clients.client_id) AS leads, clients.first_name, clients.last_name FROM clients LEFT JOIN sites ON clients.client_id = sites.client_id LEFT JOIN leads ON sites.site_id = leads.site_id GROUP BY clients.client_id;")
    # print("FETCHED all clients", client_lead_count)
    return render_template('index.html', lead_count = client_lead_count)

@app.route('/daterange', methods=['POST'])
def date_search():
    data = {
             'start_date': request.form['start_date'].split("-"),
             'end_date':  request.form['end_date'].split("-"),
           }
    lead_count_with_date = mysql.query_db("SELECT clients.client_id, clients.first_name, clients.last_name, leads.registered_datetime FROM clients LEFT JOIN sites ON clients.client_id = sites.client_id LEFT JOIN leads ON sites.site_id = leads.site_id ORDER BY leads.registered_datetime DESC;")
    lead_count_with_date_split = []
    lead_count_in_range = []
    for lead in lead_count_with_date:
        lead['registered_datetime'] = (str(lead['registered_datetime'])).split("-")
        if len(lead['registered_datetime']) > 2:
            lead_count_with_date_split.append(lead)
    for lead in lead_count_with_date_split:
        # if lead['registered_datetime'][1] > data['start_date'][1] and lead['registered_datetime'][1] < data['end_date'][1]:
        lead_count_in_range.append(lead)
    session['table_data'] = {}
    for lead in lead_count_in_range:
        if lead['first_name'] not in session['table_data'].keys():
            session['table_data'][lead['first_name']] = 1
        else: 
            session['table_data'][lead['first_name']] += 1
    print(session['table_data'])
    return redirect('/')

@app.route('/search')
def display_search():
    
    return render_template('index.html', lead_count = session['table_data'])
    
    

if __name__ == "__main__":
    app.run(debug=True)