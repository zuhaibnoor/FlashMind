from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, UserMixin
from app import mongo, bcrypt, app, login_manager
from flask import request, flash

@login_manager.user_loader
def load_user(email):
    # Find the user in the database by email
    user = mongo.db.FlashMind.find_one({'email': email})
    if user:
        # Return a simple user object with an id attribute (required by Flask-Login)
        return SimpleUser(user['email'])
    return None

# Define a simple user class
class SimpleUser(UserMixin):
    def __init__(self, email):
        self.id = email  # Use email as the unique identifier

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = mongo.db.FlashMind.find_one({'email': email})

        if user and bcrypt.check_password_hash(user['password'], password):
            # Log the user in using the SimpleUser class
            login_user(SimpleUser(user['email']))
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html')
        

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8') #.decode() converts byte string to normal string which is supported by mongodb
        print(mongo)
        mongo.db.FlashMind.insert_one({'email': email,
                                        'username': username,
                                        'password': hashed_password,
                                        'flashcards': [] })
        
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    return render_template('home.html')