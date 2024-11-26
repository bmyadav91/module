from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

app = Flask(__name__)

# Set up the MongoDB URI (Update the URI for MongoDB Atlas if needed)
app.config['MONGO_URI'] = "mongodb+srv://admin:admin@pw-practice.ji9f6.mongodb.net/sample_mflix?retryWrites=true&w=majority"  # Replace with your MongoDB URI
app.secret_key = "your_secret_key"  # Used for session management

# Initialize MongoDB
mongo = PyMongo(app)

# Home Route (After login)
@app.route('/')
def home():
    if 'user' in session:
        return render_template('home.html', username=session['user'])
    return redirect(url_for('signin'))


# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username already exists
        user = mongo.db.users.find_one({'username': username})
        if user:
            flash('Username already exists', 'danger')
            return redirect(url_for('signup'))
        
        # Hash the password before storing it
        hashed_password = generate_password_hash(password)
        
        # Save the new user into the MongoDB
        mongo.db.users.insert_one({
            'username': username,
            'password': hashed_password
        })
        
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('signin'))
    
    return render_template('signup.html')

# Signin Route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Find user by username
        user = mongo.db.users.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            # Store user information in session
            session['user'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('signin'))
    
    return render_template('signin.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)  # Clear the session
    flash('Logged out successfully!', 'info')
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)
