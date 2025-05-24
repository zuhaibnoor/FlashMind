from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://zuhaib:zuhaib123@mycluster.sea773x.mongodb.net/FlashMind?retryWrites=true&w=majority&appName=mycluster"
# app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "1213"

mongo = PyMongo(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes



"""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"""