from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///market.db'
app.config['SECRET_KEY'] = '47e0a2f1b4e87df9052f3323'
app.app_context().push()
db = SQLAlchemy(app)
bcrypt= Bcrypt(app) # This is to create hash passwords
login_manager = LoginManager(app)
login_manager.login_view= "Login_Page"
login_manager.login_message_category= "info"
from market import routes             