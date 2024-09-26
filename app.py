from flask import Flask, request, render_template, redirect, url_for, flash, session
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

def get_db_connection():
    db_config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'database': 'tdp',
        'raise_on_warnings': True
    }
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None
    
@app.route('/')
def home():
    
    return render_template('index.html')


#LOGIN BLOCK

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Use the existing get_db_connection function
        connection = get_db_connection()
        if connection is None:
            flash('Database connection could not be established.')
            return render_template('login.html')

        cursor = connection.cursor()
 
        # Retrieve form data
        username = request.form['usn']
        password_attempt = request.form['psw']
 
        # Query to check login credentials
        query = "SELECT user_id, password, role FROM users WHERE username=%s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
 
        # Check if user exists and password matches
        if user_data and user_data[1] == password_attempt:  # Assuming password is at index 1
            # Store user ID and role in session
            session['user_id'] = user_data[0]
        else:
            flash('Invalid username/password')
            return render_template('login.html')
 
        # Ensure the cursor and connection are closed
        cursor.close()
        connection.close()
    else:
        # If request method is GET or form submission failed, render the login page
        return render_template('login.html')


# BLOCK FOR SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['usn']
        password = request.form['psw']

        conn = get_db_connection()
        if conn is None:
            flash('Database connection could not be established.', 'danger')
            return render_template('signup.html')

        cursor = conn.cursor()

        # Check if the username is already taken
        cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            flash('Username already taken. Please choose a different one.', 'danger')
            return redirect(url_for('signup'))

        # Insert the new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))

        conn.commit()
        cursor.close()
        conn.close()

        flash('signup successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# Example protected route (dashboard)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('login'))
    
    return f"Welcome to your dashboard, User ID: {session['user_id']}"

# LOGOUT BLOCK
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
