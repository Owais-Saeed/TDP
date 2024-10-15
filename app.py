from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Connection
client = MongoClient('mongodb://mongodb:27017/')
db = client['mydatabase']  # Use your database name
users_collection = db['users']

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user already exists
        existing_user = users_collection.find_one({'username': username})
        if existing_user is None:
            # Insert the new user into the collection
            users_collection.insert_one({'username': username, 'password': password})
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'User already exists!'

    return render_template('signup.html')

# Signin Route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find the user in the collection
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password!'

    return render_template('signin.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f'Welcome, {session["username"]}!'
    return redirect(url_for('signin'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
