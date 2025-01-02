from flask import Flask, session, render_template, redirect, url_for, request
from odeta import database

# Machine database
ma = database('my_database.db')
table = ma('my_table')

# Parties database
pa = database('my_parties.db')
tables = pa('pa_table')

# Contact us database
ca = database('my_contact.db')
tabless = ca('ca_table')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  


@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('uname')
        email = request.form.get('email')
        password = request.form.get('password')
        if username == 'sachin' and password == '1234' and email == 'tech.sachinjpr@gmail.com':
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/data', methods=['GET', 'POST'])
def data():
    if 'username' in session:
        if request.method == 'POST':
            new_entry = {
                "machine_name": request.form.get('machine-name'),
                "machine_company": request.form.get('machine-company'),
                "operation_type": request.form.get('operation-type'),
                "trip_calculation": request.form.get('trip-calculation'),
                "usage_type": request.form.get('usage-type'),
                "service_interval": request.form.get('service-interval')
            }
            table.put(new_entry)
            return redirect(url_for('data'))
        
        data_all = table.fetchall()
        parties_all = tables.fetchall()
        return render_template('data.html', data=data_all, parties=parties_all)
    
    return redirect(url_for('login'))


@app.route('/parties', methods=['GET', 'POST'])
def parties():
    if 'username' in session:
        if request.method == 'POST':
            par_entry = {
                "party_name": request.form.get('party-name'),
                "party_address": request.form.get('party-address')
            }
            tables.put(par_entry)
            return redirect(url_for('data'))
        
        data_all = table.fetchall()
        parties_all = tables.fetchall()
        return render_template('data.html', data=data_all, parties=parties_all)
    
    return redirect(url_for('login'))


@app.route('/contactus', methods=['GET','POST'])
def contactus():
    if 'username' in session:
        if request.method == 'POST':
            con_entry = {
                "name": request.form.get('name'),
                "email": request.form.get('email'),
                "message": request.form.get('message')
            }
            tabless.put(con_entry)
            return redirect(url_for('contactus'))
        contact_all =tabless.fetchall()
        return render_template('contactus.html',cont = contact_all)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
