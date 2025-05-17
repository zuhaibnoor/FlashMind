from flask import render_template, redirect
from flask_login import login_required, login_user, UserMixin, logout_user, current_user
from app import mongo, bcrypt, app, login_manager
from flask import request

@login_manager.user_loader
def load_user(email):
    # Find the user in the database by email
    user = mongo.db.FlashMind.find_one({'email': email})
    if user:
        # Return a simple user object with an id attribute (required by Flask-Login)
        return OurUser(user['email'], user['flashcards'])
    return None

# Define a simple user class
class OurUser(UserMixin):
    def __init__(self, email, flashcards=None):
        self.id = email  # Use email as the unique identifier
               
        self.flashcards = flashcards

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = mongo.db.FlashMind.find_one({'email': email})
        print(user)

        if user and bcrypt.check_password_hash(user['password'], password):
            # Log the user in using the SimpleUser class
            login_user(OurUser(user['email']), user['flashcards'])
            # flash('Login successful!', 'success')
            # return redirect(url_for('home'))
            return redirect('/home')

        # else:
        #     flash('Invalid email or password', 'danger')

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
                                        'flashcards': {} })
        
        return redirect('/login')
    return render_template('signup.html')


@app.route('/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/add_flashcard', methods = ['POST'])
@login_required
def add_flashcard():
    if request.method == "POST":
        
        new_flashcard = {
            'question': request.form.get('question'),
            'answer': request.form.get('answer')
        }

        current_user.flashcards[new_flashcard['question']] = new_flashcard['answer']

        mongo.db.FlashMind.update_one(
            {'email': current_user.id},
            {'$set': {'flashcards':current_user.flashcards} }
        )
        return redirect('/home')

@app.route('/edit_flashcard', methods = ['POST'])
@login_required
def edit_flashcard():
    if request.method == "POST":
        old_question = request.form.get('old_question')
        new_question = request.form.get('question')
        answer = request.form.get('answer')

        if old_question != new_question:     
            print(current_user.flashcards)       
            current_user.flashcards.pop(old_question)
            current_user.flashcards[new_question] = answer
        
        else:
            current_user.flashcards[new_question] = answer

        mongo.db.FlashMind.update_one(
            {"email":current_user.id},
            {'$set':{'flashcards': current_user.flashcards}}
        )

    return render_template('home.html', flashcards = current_user.flashcards)


@app.route('/delete_flashcard', methods = ['GET'])
@login_required
def delete_flashcard():
    if request.method == "GET":
        question = request.args.get('question')
        current_user.flashcards.pop(question)
        
        mongo.db.FlashMind.update_one(
            {'email': current_user.id},
            {'$set': {'flashcards': current_user.flashcards}}
        )
    
    return redirect('/home')


@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    flashcards = current_user.flashcards
    print(flashcards)
    return render_template('home.html', flashcards=flashcards)