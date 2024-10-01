from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import json


from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def home():   
    return render_template('index.html')

# @app.route('/dashboard')
# def dashboard():
#     with open('response.json', 'r') as f:
#         decks = json.load(f)
#     return render_template('dashboard.html', decks=decks)

@app.route('/flashcards/<topic>')
def flashcards(topic):
    with open('response.json', 'r') as f:
        deck = json.load(f)
    if deck['topic'] == topic:
        return render_template('flashcards.html', deck=deck)
    else:
        return "Deck not found", 404

@app.route('/api/deck/<topic>')
def get_deck(topic):
    with open('response.json', 'r') as f:
        deck = json.load(f)
    if deck['topic'] == topic:
        return jsonify(deck)
    else:
        return "Deck not found", 404
    

#___________________________________________________________________________________________#

#Signin/Signup

# MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['test_database']  # Use your database name
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
    app.run(host="0.0.0.0", port=8000, debug=True)