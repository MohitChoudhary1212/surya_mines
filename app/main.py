from flask import Flask, session, render_template, redirect, url_for, request
from odeta import localbase

# Database
db = localbase('my_database.db')

users = db('users')
tables = db('pa_table')
tabless = db('ca_table')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        title = request.form.get('title')
        gender = request.form.get('gender')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password and title and username and action == 'create':
            users.put({
                "username" : username,
                "password" : password,
                "title" : title,
                "mobile" : mobile,
                "email" : email,
                "gender" : gender
            })
            print("registration done")
            return render_template('register.html', msg = "registration successfull.")
        
        if username and action == 'delete':
            users.delete(username)
            return render_template('register.html', msg = "user deleted.")        

        if username and action == 'update':    

            id = users.fetch({ "username" : username, "password" : password })[0]["id"]        
            users.update({
                "username" : username,
                "password" : password,
                "title" : title,
                "mobile" : mobile,
                "email" : email,
                "gender" : gender
            },id)
            return render_template('register.html', msg = "user updated.")        

    return render_template('register.html', user = users.fetch())

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('password')
        
        if users.fetch({
            "username" : username,
            "password" : password
        }):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_pass():
    if 'username' not in session: return redirect(url_for('login'))

    pass
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

"""
Merge both functions to create a single endpoint which receives GET and POST requests and a variable which will differentiate.
"""


@app.route('/data', methods=['GET', 'POST'])
def data():
    if 'username' not in session: return redirect(url_for('login'))

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
    if 'username' not in session: return redirect(url_for('login'))
    
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

if __name__ == '__main__':
    app.run(debug=True)
