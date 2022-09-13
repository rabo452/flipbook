from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from .config import *


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./{}.db'.format(db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secret_key
app.config['MAIL_SERVER'] = EMAIL_SERVER
app.config['MAIL_PORT'] = EMAIL_PORT
app.config['MAIL_USERNAME'] = EMAIL_USERNAME
app.config['MAIL_PASSWORD'] = EMAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = EMAIL_USERNAME
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TSL'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'log_in_page'

mail = Mail(app)

from . import database
# add routes to app
from .routes import admin_routes, api_routes, front_routes

@login_manager.user_loader
def get_user_session(user_id):
    return database.admin_user.query.get(int(user_id))


# create directory for files if it doesn't have
if not os.path.exists(FLIP_BOOK_FILES_DIRECTORY):
    os.makedirs(FLIP_BOOK_FILES_DIRECTORY)
